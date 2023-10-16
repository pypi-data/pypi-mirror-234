import os
import zipfile
import io
import yaml
import pickle
import imageio


from pyrateshield.constants import CONSTANTS
from pyrateshield.modelitem import ModelItem

from pyrateshield.model_sequences import (Walls,
                                          SourcesNM,
                                          SourcesCT,
                                          SourcesXray,
                                          CriticalPoints,
                                          Shieldings,
                                          Materials,
                                          Clearances,
                                          Rulers)
                                        
from functools import partial

from pyrateshield.floorplan_and_dosemap import (Dosemap, Floorplan, 
                                                DosemapStyle, MeasuredGeometry)
from pyrateshield import labels

try:
    wdir = os.path.split(__file__)[0] 
except:
    wdir = os.getcwd()
    
filename = os.path.join(wdir, 'defaults.yml')
    
DEFAULTS = yaml.safe_load(open(filename))


class PauseHistoryRecording:
    def __init__(self, history):
        self.history = history
    def __enter__(self):
        self.history.block_recording(True)
    def __exit__(self, *args):
        self.history.block_recording(False)

class PauseHistoryCleanup:
    def __init__(self, history):
        self.history = history
    def __enter__(self):
        self.history.block_cleanup(True)
    def __exit__(self, *args):
        self.history.block_cleanup(False)


class ModelHistory:
    ATTRIBUTE_VALUE_CHANGE      = 'attribute_value_change'
    MODEL_ITEM_DELETED          = 'model_item_deleted'
    MODEL_ITEM_ADDED            = 'model_item_added'
    
    _block_recording = False
    _undo_records = None
    _stack = None
    _block_cleanup = False
    
    def __init__(self, parent=None):
        self.parent = parent
        self.set_callbacks()
        
    def stack(self):
        if self._stack is None:
            self._stack = {}
        return self._stack
    
    def undo_records(self):
        if self._undo_records is None:
            self._undo_records = []
        return self._undo_records
    
    def redo_records(self):
        if self._redo_records is None:
            self._redo_records = []
        return self._redo_records
        
    def add_to_stack(self, record):
        # stack can only collect a list of change that are the same type
        type_of_change, _ = record
        if type_of_change not in self.stack().keys():
            if len(self.stack()) > 0:
                self.clean(force=True)
            self.stack()[type_of_change] = []
        self.stack()[type_of_change].append(record)
      

    def set_callbacks(self):
        # listen to changes in the model
        for attr in self.parent._attr_dct.keys():
            item = getattr(self.parent, attr)
            cbk = partial(self.add_undo_record, self.ATTRIBUTE_VALUE_CHANGE, item)
            if isinstance(item, ModelItem):
                # Non model sequences, like floorplan and dosemap
                pass
            else:
                # model sequences
                item.valueChanged.connect(cbk)
                cbk = partial(self.add_undo_record, self.MODEL_ITEM_DELETED, item)
                item.rowsAboutToBeRemoved.connect(cbk)
                cbk = partial(self.add_undo_record, self.MODEL_ITEM_ADDED, item)
                item.rowsInserted.connect(cbk)
                
    def add_undo_record(self, type_of_change, sequence, event_data):
         if self.isBlockedRecording(): return
         self._redo_records = None
         if type_of_change == self.ATTRIBUTE_VALUE_CHANGE:  
             item, label, old_value, new_value = event_data
             if label == labels.CLOSED:
                 self.clean()
             elif label in (labels.VERTICES, labels.VERTICES_PIXELS):
                 
                 if old_value == new_value:
                     return
                 if len(old_value) != len(new_value):
                     self.clean()

             self.add_to_stack([type_of_change, event_data])
                 
         elif type_of_change in (self.MODEL_ITEM_DELETED,
                                 self.MODEL_ITEM_ADDED):
             model_item = sequence.itemAtIndex(event_data)
             self.add_to_stack([type_of_change, (sequence, model_item)])   
             
    def items_to_clean(self):
        if len(self.stack()) == 0: 
            return []
        else:
            key = list(self.stack().keys())[0]
            return self.stack()[key]
        
    def clean(self, force=False):    
        # Tricky implementation. All model changes are recorded in stack.
        # When the selection in the UI changes or undo is called all entries
        # stored in stack and stored in records. Except for position changes.
        # For position changes only the first record is stored to records. So
        # when items are moved by the mouse the original location is kept and 
        # all other locations are ignored. Undo will then restore the location
        # where the movement initiated.
        
        if self._block_cleanup and not force: return
      
        items_with_position_changes = {}
        records = []
        pos_labels = (labels.VERTICES_PIXELS, labels.POSITION, labels.VERTICES)
        
        for record in self.items_to_clean(): 
            type_of_change, data = record
            data = list(data)
            record = [type_of_change, data]
            if type_of_change != self.ATTRIBUTE_VALUE_CHANGE:
                records.append(record)
            else:
                item, label, old_value, new_value = data
                if label not in pos_labels:
                    records.append(record)
                else:
                    if item not in items_with_position_changes.keys():
                        items_with_position_changes[item] = record
                        records.append(record)
                    else:
                        _, data = items_with_position_changes[item]
                        data[-1] = new_value
                        if len(data) != 4:
                            raise

        if len(records) > 0:
            self.undo_records().append(records)
        
        self._stack = None
        
    def block_cleanup(self, block):
        self._block_cleanup = block

    def get_entries_to_undo(self):
        self.clean(force=True)
        return self.undo_records().pop(-1) if len(self.undo_records()) > 0 else []
    
    def get_entries_to_redo(self):
        return self.redo_records().pop(-1) if len(self.redo_records()) > 0 else []
                     
    def block_recording(self, block):
        self._block_recording = block
        
    def isBlockedRecording(self):
        return self._block_recording
                
    def undo(self):
        undo_items = self.get_entries_to_undo()
        for entry in undo_items:
            self.undo_entry(entry)
        self.redo_records().append(undo_items)
            
    
    def redo(self):
        
        redo_items = self.get_entries_to_redo()
     
        for entry in redo_items:
            self.redo_entry(entry)
        self.undo_records().append(redo_items)
        
    def redo_entry(self, record):
        type_of_change, data = record
       
        if type_of_change == self.ATTRIBUTE_VALUE_CHANGE:
            item, label, _, new_value = data
            attr = item.attr_name_from_label(label)
            with PauseHistoryRecording(self):
                setattr(item, attr, new_value)
        elif type_of_change == self.MODEL_ITEM_DELETED:     
            sequence, item = data
            with PauseHistoryRecording(self):
                self.parent.delete_item(item)
        elif type_of_change == self.MODEL_ITEM_ADDED:
            sequence, item = data
            with PauseHistoryRecording(self):
                sequence.addItem(item)
        
                
        
        
    def undo_entry(self, record):
        type_of_change, data = record
       
        if type_of_change == self.ATTRIBUTE_VALUE_CHANGE:
            item, label, old_value, _ = data
            attr = item.attr_name_from_label(label)
            with PauseHistoryRecording(self):
                setattr(item, attr, old_value)
        elif type_of_change == self.MODEL_ITEM_DELETED:     
            sequence, item = data
            with PauseHistoryRecording(self):
                sequence.addItem(item)
        elif type_of_change == self.MODEL_ITEM_ADDED:
            _, item = data
            with PauseHistoryRecording(self):
                self.parent.delete_item(item)
                
        
                
    def reset(self):      
        self._records = None
        self._stack = None
    
    
            

class Model(ModelItem):
    
    filename            = None

    _attr_defaults = {labels.SOURCES_NM:        SourcesNM,
                      labels.SOURCES_CT:        SourcesCT,
                      labels.SOURCES_XRAY:      SourcesXray,
                      labels.CRITICAL_POINTS:   CriticalPoints,
                      labels.WALLS:             Walls,
                      labels.CLEARANCE:         Clearances,
                      labels.MATERIALS:         Materials,
                      labels.SHIELDINGS:        Shieldings,
                      labels.FLOORPLAN:         Floorplan,
                      labels.DOSEMAP:           Dosemap,
                      labels.DOSEMAP_STYLE:     DosemapStyle,
                      labels.RULERS:            Rulers}
    
    _attr_dct = {
        "sources_nm":       labels.SOURCES_NM,
        "sources_ct":       labels.SOURCES_CT,
        "sources_xray":     labels.SOURCES_XRAY,
        "critical_points":  labels.CRITICAL_POINTS,
        "clearances":       labels.CLEARANCE,
        "materials":        labels.MATERIALS,
        "shieldings":       labels.SHIELDINGS,
        "floorplan":        labels.FLOORPLAN,
        "dosemap":          labels.DOSEMAP,
        "dosemap_style":    labels.DOSEMAP_STYLE,
        "walls":            labels.WALLS,
        "rulers":           labels.RULERS
        }
    
    
   
   
    
    
    def __init__(self, **kwargs):
        self.constants = CONSTANTS
        
        kwargs = self.prepare_init(**kwargs)
        
  
        ModelItem.__init__(self, **kwargs)
        
        self.set_defaults()
        
        # for attr in self._attr_dct.keys():
        #     getattr(self, attr).setParent(self)
        
        

        if self.floorplan.geometry.origin == labels.BOTTOM_LEFT:
            # PyQt5 has top left as (0, 0), matplotlib bottom left
            # Flip all items in y if model is saved with matplotlib
            self.set_legacy_y()

        self.fix_none_entries()
        self.history = ModelHistory(parent=self)
    
    # Code to make objects pickable
    def __getstate__(self):
        dct = self.to_dict()
        # floorplan not in dict (!)
        dct[labels.FLOORPLAN][labels.IMAGE] = self.floorplan.image
        return dct
        
    def __setstate__(self, dct):
        self.__init__(**dct)
        # restore floorplan
        self.floorplan.image = dct[labels.FLOORPLAN][labels.IMAGE]
    # end pickable
    
    
    def set_defaults(self):
        if len(self.clearances) == 1:
            self.clearances = Clearances.from_list(DEFAULTS[labels.CLEARANCE])
        if len(self.materials) == 1:           
            self.materials = Materials.from_list(DEFAULTS[labels.MATERIALS])
        if len(self.shieldings) == 1:
            self.shieldings = Shieldings.from_list(DEFAULTS[labels.SHIELDINGS])
    
    def get_attr_from_label(self, label):
        if label in (labels.PIXEL_SIZE_CM, labels.GEOMETRY):
            return self.floorplan.geometry
        else:
            return super().get_attr_from_label(label)
                
    def prepare_init(self, **kwargs):
        for key, value in kwargs.items():
            if key in self._attr_dct.keys():
                label = self._attr_dct[key]
            else:
                label = key
            if isinstance(value, list):
                kwargs[key] = self._attr_defaults[label].from_list(value)
            elif isinstance(value, dict):
                kwargs[key] = self._attr_defaults[label].from_dict(value)
        return kwargs
        
    def to_dict(self):
        dct = {}
        for attr in self._attr_dct.keys():
            value  = getattr(self, attr)
            if hasattr(value, 'to_dict'):
                value = value.to_dict()
            elif hasattr(value, 'to_list'):
                value = value.to_list()
            else:
                raise AttributeError('Cannot serialize {attr}')
            dct[self._attr_dct[attr]] = value
        return dct
    
    def __str__(self):
        return yaml.dump(self.to_dict())

    def delete_item(self, item):
        sequence = self.sequence_for_item(item)
        if item in sequence:
            sequence.deleteItem(item)
    
    def delete_items(self, items):
        with PauseHistoryCleanup(self.history):
            for item in items:
                self.delete_item(item)
        self.history.clean()

    def add_item(self, item):
        # add a item of any type used by gui
        sequence = self.sequence_for_item(item)
        sequence.addItem(item)
 
    def sequence_for_item(self, item):
        return self.get_attr_from_label(item.label)
    
    def sort_model_items(self, items):
        # Used by UI to sort a bunch of selected items
        sorted_items = {}
        
        for item in items:
            if item.label not in sorted_items.keys():
                sorted_items[item.label] = []
            sorted_items[item.label] += [item]        
        return sorted_items
    
    def item_class_for_label(self, label):
        sequences = {label: item for label, item in self._attr_defaults.items()\
                     if hasattr(item, 'item_class')}
       
        
        if label in sequences.keys():
            return sequences[label].item_class
        
        else:
            raise KeyError(f'No sequence defined for label {label}')

    def save_to_project_file(self, filename):    
        file, ext = os.path.splitext(filename)
        if ext.lower() != '.zip':
            filename = file + '.zip' # force saving old projects to ext zip
        
        self.filename = filename
                        
        project_dict = self.to_dict()
        image = self.floorplan.image
        
        temp_yml = io.StringIO()
        yaml.dump(project_dict, temp_yml, default_flow_style=None)
        
        temp_img = io.BytesIO()
        imageio.imwrite(temp_img, image, format=".png")

        with zipfile.ZipFile(filename, "w") as zf:
            zf.writestr("project.yml", temp_yml.getvalue())
            zf.writestr("floorplan.png", temp_img.getvalue())
    
    
    @classmethod
    def load_from_project_file(cls, filename):
        try:
            with zipfile.ZipFile(filename) as zf:
                with zf.open("floorplan.png", "r") as f:
                    image = imageio.imread(f)
                with zf.open("project.yml", "r") as f:
                    dct = yaml.safe_load(f)
                 
                
                dct[labels.FLOORPLAN][labels.IMAGE] = image
                model = cls.from_dict(dct)
                
        
        except zipfile.BadZipFile:
            ### For backwards compatibility:
            success = False
            if filename.endswith(".psp"):
                try:
                    model = cls.load_old_psp_file(filename)
                    success = True
                except:
                    pass
                
            if not success:
                # IOError is picked up by GUI to show error dlg
                raise IOError(f'Could not read {filename}')
    
        model.filename = filename
        return model
    
    
# =============================================================================
#     LEGACY STUFF
# =============================================================================
    
    @classmethod
    def load_old_psp_file(cls, filename):
        ### For backwards compatibility:
        with open(filename, 'rb') as fp:
            dct = pickle.load(fp)
        
        image = dct.pop("IMAGE_DATA")   
        dct[labels.FLOORPLAN][labels.IMAGE] = image
        dct[labels.FLOORPLAN].pop('Filename', None)
        
        # ugly code to remove invalid key from older versions
        dct[labels.FLOORPLAN][labels.GEOMETRY].pop(False, False)
        
        return cls.from_dict(dct)

    # def zero_origin(self):
    #      # old psp files had an origin option, origin is now always at (0, 0)
         
    #      origin = self.floorplan.geometry.origin_cm
         
    #      if origin[0] != 0 or origin[1] != 0:
    #          self.shift_cm(origin[0], origin[1])
    #          self.floorplan.geometry.origin_cm = [0, 0]  
    
    
    def fix_none_entries(self):
        for shielding in self.shieldings:
            materials = shielding.materials
            if materials[0][0] in (None, ''):
                materials[0][0] = Materials.empty_item_name
            if len(materials) > 1:
                if materials[1][0] in (None, ''):
                    materials[1][0] = Materials.empty_item_name
        
        for wall in self.walls:
            if wall.shielding in (None, ''):
                wall.shielding = Shieldings.empty_item_name
                
        # for sources in self.sources_nm:
        #     if source.
        
    
    def set_legacy_y(self):
        print('SET LEGACY Y COORDS')
        psize = self.get_pixel_size_cm()
        height = self.floorplan.image.shape[0]  
        for wall in self.walls:
            
            wall.vertices[0][1] = height* psize - wall.vertices[0][1]
            wall.vertices[1][1] = height* psize - wall.vertices[1][1]
        
        
        for point in [*self.sources_ct,
                      *self.sources_xray,
                      *self.sources_nm,
                      *self.critical_points]:
           
            point.position[1] = height* psize - point.position[1]
        
        
        
        if isinstance(self.floorplan.geometry, MeasuredGeometry):
            vvp = self.floorplan.geometry.vertices_pixels
            vvp[0][1] = height - vvp[0][1]
            vvp[1][1] = height - vvp[1][1]
        
        self.floorplan.geometry.origin = labels.TOP_LEFT

if __name__ == "__main__":
    # import yaml
    # with open('test_model_in.yml') as file:
    #     dct = yaml.safe_load(file)
    # model = Model.from_dict(dct)
    file = '../example_projects/SmallProject/project.zip'
    file = '../example_projects/LargeProject/project.zip'
    # file = 'C:/Users/757021/git/pyrateshield/example_projects/Nucleaire Geneeskunde.psp'
    #file = 'C:/Users/r757021/Desktop/test.zip'
    model = Model.load_from_project_file(file)
    # model = Model()
    
