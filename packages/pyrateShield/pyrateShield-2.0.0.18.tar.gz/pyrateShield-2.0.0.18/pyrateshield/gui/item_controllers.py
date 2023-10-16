from pyrateshield.floorplan_and_dosemap import MeasuredGeometry, Geometry
from pyrateshield.model_items import  Wall
from pyrateshield.gui.graphics_items import RulerLine
from pyrateshield import labels
from pyrateshield.constants import CONSTANTS
from pyrateshield.gui.item_views import BlockValueChangedSignal



class EditModelItemsController():
    model = None
    _parent = None
    def __init__(self, model=None, view=None, parent=None):
       
        self._parent = parent
        self.view = view
        self.set_model(model)
        
        self.set_callbacks()
        
                
    def parent(self):
        return self._parent

    def set_callbacks(self):
        if self.view.list is not None:
            self.view.list.currentIndexChanged.connect(self.list_selection)
        self.view.valueChanged.connect(self.value_changed)
        if hasattr(self.view, 'new_button'):            
            self.view.new_button.clicked.connect(self.new)
        if hasattr(self.view, 'delete_button'):
            self.view.delete_button.clicked.connect(self.delete)
        self.parent().view.focusSet.connect(self.focus_set)
        
    def focus_set(self, label):
        if label == self.model.item_class.label:
            self.refresh()
    
    def refresh(self):       
        index = self.view.list.currentIndex()
        self.list_selection(index)
            
    
    def value_changed(self, label, value):    
        item = self.item_in_view()
        if item is not None:
            item.update_by_dict({label: value})
    
    def list_selection(self, index):             
        item = self.model.itemAtIndex(index)
        self.item_to_view(item)

    def item_in_view(self):
        return self.model.itemByName(self.view.list.currentText())
        
    def item_to_view(self, item):
        with BlockValueChangedSignal(self.view):
            if item is None:            
                self.view.clear()
                
            elif self.view.list is not None:
                if self.view.list.currentText() != item.name:
                   
                    self.view.list.setCurrentText(item.name)
                   
                else:
                    self.view.setValues(item.to_dict())  
                    
            elif isinstance(item, Wall):
                dct = item.to_dict()
                dct.pop(labels.VERTICES)
                dct.pop(labels.CLOSED)
                self.view.setValues(dct)  
        

        self.view.setEnabled(len(self.model) > 0)

    def delete(self):
        item = self.item_in_view()
        self.model.deleteItem(item)
   
            
    def new(self):

        item = self.item_in_view()
        new_item = self.model.item_class.from_dict(item.to_dict())
        new_item.name = self.model.item_class.default_name
   
        self.model.addItem(new_item)

        #self.view.list.setCurrentText(new_item.name)
       
        
    def disconnect_model(self):        
        if self.model is not None:
            self.model.dataChanged.disconnect()
                     
    def set_model(self, model):  
        self.model = model
        if self.view.list is not None:
            with BlockValueChangedSignal(self.view):
                self.view.list.setModel(self.model)
            
        # if len(self.model) > 0:
        #     self.item_to_view(self.model[0])
            
        self.model.dataChanged.connect(self.item_updated)
        self.model.rowsRemoved.connect(self.item_deleted)
        self.model.rowsInserted.connect(self.item_added)
        

    def item_deleted(self, index, **kwargs):
   
        if len(self.model) == 0:            
            self.view.clear()
            self.view.setEnabled(False)
        else:
            row = index.row()
            if row >= len(self.model):
                row -= 1
            self.item_to_view(self.model.itemAtIndex(row))
    
    def item_added(self, index, **kwargs):
        self.index = index
        self.view.setEnabled(True)
        item = self.model.itemAtIndex(index)
        self.item_to_view(item)
        
        
    def item_updated(self, index, _=None):    
        
        item = self.model.itemAtIndex(index)
 
        if item is self.item_in_view():
            self.item_to_view(item)
       
        
            

class EditSourcesNMController(EditModelItemsController):
    def clearances(self):
        return self.model.parent().clearances
    
    def item_to_view(self, item):
        
        super().item_to_view(item)
        with BlockValueChangedSignal(self.view):
            if self.parent() is None or item is None: return
            self.parent().controllers[labels.CLEARANCE].set_item_by_name(item.clearance)
            
    
    def set_model(self, model):
        super().set_model(model)
        with BlockValueChangedSignal(self.view):
            self.view.clearance_list.setModel(self.clearances())
        
class EditWallsController(EditModelItemsController):
    def disconnect_model(self):
        super().disconnect_model()
        if self.model is not None:
            try:
                self.model.layoutChanged.disconnect()
            except:
                pass
            
    def value_changed(self, label, value):
        super().value_changed(label, value)

            
    def set_callbacks(self):
        super().set_callbacks()
        self.view.scroll_widget.valueChanged.connect(self.sliderMoved)
        self.view.vertex_list.currentIndexChanged.connect(self.vertex_to_view)
        self.view.vertices.valueChanged.connect(self.vertex_to_model)
        
    def sliderMoved(self, index):
        item = self.model.itemAtIndex(index)
        self.item_to_view(item)
        # pixel_item = self.parent().graphics().pixel_item_for_model_item(item)
        # if pixel_item is not None:
        #     pixel_item.marker1.setSelected(True)
        #     pixel_item.marker2.setSelected(True)
            
        
    def refresh(self):
        index = self.view.scroll_widget.value()
        item = self.model.itemAtIndex(index)
        self.item_to_view(item)
    
    def set_model(self, model):        
        super().set_model(model)

        combobox_model = self.shieldings()
        with BlockValueChangedSignal(self.view):
            self.view.shielding_list.setModel(combobox_model)

        self.model.rowsInserted.connect(self.setSliderSize)
        self.model.rowsRemoved.connect(self.setSliderSize)
        self.setSliderSize()
        
    def setSliderSize(self):
        self.view.scroll_widget.setMinimum(0)
        self.view.scroll_widget.setMaximum(self.model.rowCount(0)-1)
    
    def shieldings(self):
        return self.model.parent().shieldings
    
    def item_in_view(self):
        index = self.view.scroll_widget.sliderPosition()
        return self.model.itemAtIndex(index)
    
    def item_to_view(self, item):
        super().item_to_view(item)
        if item is None: return
        
        with BlockValueChangedSignal(self.view):
            if item is not None:
                shielding = self.shieldings().itemByName(item.shielding)
                self.parent().controllers[labels.SHIELDINGS].item_to_view(shielding)
    
            index = self.model.indexForItem(item)
            
            if index is not None:
                self.view.scroll_widget.setSliderPosition(index.row())
            self.update_vertex_list()
    
    def update_vertex_list(self):
     
        item = self.item_in_view()
        current_index = self.view.vertex_list.currentIndex()
        self.view.vertex_list.clear()
        items = [f'Vertex {i}' for i in range(0, len(item.vertices))]
        self.view.vertex_list.addItems(items)
        if len(items) < current_index or current_index is None:
            current_index = 0
        self.view.vertex_list.setCurrentIndex(current_index)
        
    def vertex_to_model(self, value):
      
        item = self.item_in_view()
        index = self.view.vertex_list.currentIndex()
        if index is None or item is None: return
        item.setVertex(index, value)
    
    def marker_to_view(self, marker):
       
        if marker.parentItem() is not self.item_in_view():
            self.item_to_view(marker.parentItem())
        index = marker.parentItem().markers().index(marker)
        self.view.vertex_list.setCurrentIndex(index)
                              
    def set_vertex_index(self, index):
        if index != self.view.vertex_list.currentIndex():
            self.view.vertex_list.setCurrentIndex(index)
            
    
    def vertex_to_view(self):
       
        item = self.item_in_view()
        index = self.view.vertex_list.currentIndex()
        if index is None or index < 0 or item is None: return
        
        vertex = item.vertices[index]
        self.view.vertices.setValue(vertex)
        
        
       
        
        
class EditMaterialsController(EditModelItemsController):
    
    def edit_allowed(self, item):
        return item is not None and item.name != labels.EMPTY_MATERIAL and item.name not in CONSTANTS.base_materials
    
    def disconnect_model(self):
        super().disconnect_model()
        if self.model is not None:
            self.model.nameChanged.disconnect()
            
    def delete_allowed(self, item):
        return item is not None\
            and item not in self.model.items_in_use()\
                and item.name != labels.EMPTY_MATERIAL
    
    def set_model(self, model):        
        super().set_model(model)
        self.model.nameChanged.connect(self.name_changed)
    
    def name_changed(self, old_name, new_name):      
        for shielding in self.model.parent().shieldings:
            if shielding.materials[0][0] == old_name:
                shielding.materials[0][0] = new_name
            elif len(shielding.materials) > 1: 
                if shielding.materials[1][0] == old_name:
                    shielding.materials[1][0] = new_name
                    
                    
    def item_to_view(self, item):
        super().item_to_view(item)
        with BlockValueChangedSignal(self.view):
            self.view.delete_button.setEnabled(self.delete_allowed(item))
            self.view.setEnabled(self.edit_allowed(item))

        
        
class EditClearancesController(EditModelItemsController):
    def disconnect_model(self):
        super().disconnect_model()
        if self.model is not None:
            self.model.nameChanged.disconnect()
            
    def set_model(self, model):
        
        super().set_model(model)
        self.model.nameChanged.connect(self.name_changed)
        
    def name_changed(self, old_name, new_name):
        for source in self.model.parent().sources_nm:
            if source.clearance == old_name:
                source.clearance = new_name
                
    def edit_allowed(self, item):
        return item is not None and item.name != labels.EMPTY_CLEARANCE
                
    def delete_allowed(self, item):
        return item is not None\
            and item not in self.model.items_in_use()\
                and item.name != labels.EMPTY_CLEARANCE
                
    def set_item_by_name(self, name):
        if name in self.model.itemNames():
            self.view.list.setCurrentText(name)
           
                
    def item_to_view(self, item):      
        super().item_to_view(item)      
        with BlockValueChangedSignal(self.view):
            if self.edit_allowed(item):
                self.view.update_available_widgets()
                self.view.delete_button.setEnabled(self.delete_allowed(item))
            else:
                self.view.setEnabled(False)
        
                
class EditShieldingsController(EditModelItemsController):
    
    
        
    def edit_allowed(self, item):
        return item is not None and item.name != labels.EMPTY_SHIELDING 
    
    def disconnect_model(self):
        super().disconnect_model()
        if self.model is not None:
            self.model.nameChanged.disconnect()
    
    def delete_allowed(self, item):
        return item is not None\
            and item not in self.model.items_in_use()\
                and item.name != labels.EMPTY_SHIELDING
                
          
    def set_model(self, model):
        
            
        super().set_model(model)
       
        materials = self.model.parent().materials
        with BlockValueChangedSignal(self.view):
            self.view.materials.material1_list.setModel(materials)
            self.view.materials.material2_list.setModel(materials)
        self.model.nameChanged.connect(self.name_changed)
        
    def name_changed(self, old_name, new_name):        
        for wall in self.model.parent().walls:
            if wall.shielding == old_name:
                wall.shielding = new_name
                
    def item_to_view(self, item):  
        super().item_to_view(item)   
       
        
        self.view.setEnabled(self.edit_allowed(item))
        self.view.delete_button.setEnabled(self.delete_allowed(item))
        
       
            
                


class EditPixelSizeController():
    model = None
    _measured_geometry = None
    _fixed_geometry = None
    _line = None
    
    click_connection = None
    release_connection = None
    move_connection = None
    
    def __init__(self, model=None, view=None, parent=None):
        self.model = model 
        self.view = view
        self.parent = parent
        self.set_callbacks()
        
    def set_callbacks(self):        
        self.view.measure_button.clicked.connect(self.measure_in_view)
        self.view.confirm_button.clicked.connect(self.confirm)
        self.view.valueChanged.connect(self.value_changed)
       
        
        self.parent.view.focusSet.connect(self.focus_set)
        
        
    def line(self):        
        if self._line is None:
         
            self._line = RulerLine(self.geometry(), show_text=False)    
            if self._line.model.distance_pixels == 0:
                self._line.setVisible(False)                              
        return self._line
        
    
    def showLine(self):
        if not isinstance(self.geometry(), MeasuredGeometry):
            self.removeLine()
        else:
            self.graphics().scene().addItem(self.line())                
                                         
    def removeLine(self):
      
        self.graphics().scene().removeItem(self._line)
        self._line = None
        
    def view_geometry_type_changed(self):
        self.showLine()
            
            
    def value_changed(self, label, value):
        if label == labels.GEOMETRY:
            self.view_geometry_type_changed()
        elif label == labels.REAL_WORLD_DISTANCE_CM:
            self.measuredGeometry().distance_cm = value
        elif label == labels.PIXEL_SIZE_CM:            
            self.fixedGeometry().pixel_size_cm = value
        elif label == labels.VERTICES_PIXELS:
            self.measuredGeometry().vertices_pixels = value

    def disconnect_model(self):
        self._measured_geometry = None
        self._fixed_geometry = None
    
    def set_model(self, model):
        self.model = model
        self.item_to_view(self.model)
  

    def confirm(self):        
        self.model.parent().geometry = self.geometry_in_view()        
        self.set_model(self.model.parent().geometry)
        self._line = None
        self.focus_set(labels.PIXEL_SIZE_CM)
    
        
        
    def graphics(self):
        return self.parent.graphics()
    
    def geometry(self):
        if self.view.choose_fixed.isChecked():
            return self.fixedGeometry()
        else:
            return self.measuredGeometry()
                        
    def geometry_in_view(self):
        values = self.view.values()
      
        if self.view.choose_fixed.isChecked():
            geometry = Geometry(pixel_size_cm=values[labels.PIXEL_SIZE_CM],
                                origin=labels.TOP_LEFT)
        elif self.view.choose_measured.isChecked():
            if values[labels.REAL_WORLD_DISTANCE_CM] == 0:
                values[labels.REAL_WORLD_DISTANCE_CM] = 1
            geometry = MeasuredGeometry(vertices_pixels=values[labels.VERTICES_PIXELS],
                                        distance_cm=values[labels.REAL_WORLD_DISTANCE_CM],
                                        origin=labels.TOP_LEFT)
            
        # geometry.setParent(self.model.parent())
        return geometry
    
    def geometry_updated(self, event_data):       
        src, label, old_value, value = event_data
                
        self.view.setValue(label, value)
        
        if isinstance(self.geometry(), MeasuredGeometry):
            self.view.setValue(labels.PIXEL_SIZE_CM, self.geometry().pixel_size_cm)
        

    def item_to_view(self, item):
        with BlockValueChangedSignal(self.view):
            if isinstance(item, MeasuredGeometry):
                self.view.set_choose_measured()
            else:
                self.view.set_choose_fixed()
            
            if item is not None:
                dct = item.to_dict()
                dct.pop(labels.ORIGIN, None)
                self.view.setValues(dct)
           

    def measuredGeometry(self):
        if self._measured_geometry is None:
            if isinstance(self.model, MeasuredGeometry):
                geometry = MeasuredGeometry.from_dict(self.model.to_dict())
                self._measured_geometry = geometry
            else:
                self._measured_geometry = MeasuredGeometry(origin=labels.TOP_LEFT)
            self._measured_geometry.update_event.connect(self.geometry_updated)
        return self._measured_geometry
    
    def fixedGeometry(self):
        if self._fixed_geometry is None:
            if not isinstance(self.model, MeasuredGeometry):
                geometry = Geometry.from_dict(self.model.to_dict())
                self._fixed_geometry = geometry
            else:
                self._fixed_geometry = Geometry(origin=labels.TOP_LEFT)
            self._fixed_geometry.update_event.connect(self.geometry_updated)
        return self._fixed_geometry
    
    
    def focus_set(self, label):    
        if label == labels.PIXEL_SIZE_CM:
            self.graphics().scene().setVisibleGraphicsModelItems(False)
            self.item_to_view(self.model)
            self.view_geometry_type_changed()
            self.parent.view.toolbar.setEnabled(False)
            self.parent.view.result_container.setTabEnabled(1, False)
            self.showLine()
        else:
            self.graphics().scene().setVisibleGraphicsModelItems(True)
            
            self.parent.view.toolbar.setEnabled(True)
            self.parent.view.result_container.setTabEnabled(1, True)
            self._measured_geometry = None
            self._fixed_geometry = None
            self.removeLine()
            
        
              
    def measure_in_view(self):    

        def start(event):
           
            
            pos = self.graphics().mapToScene(event.pos())
            vertices_pixels = [[pos.x(), pos.y()], [pos.x(), pos.y()]]           
            self.line().model.vertices_pixels = vertices_pixels
            self.move_connection = self.graphics().mouseMove.connect(update)
            self.line().setVisible(True)

        def update(event):
            #print('update')
            pos = self.graphics().mapToScene(event.pos())                     
            self._line.model.set_vertex_pixels(1, [pos.x(), pos.y()])
         
        def disconnect():
            if self.click_connection is not None:
                self.graphics().leftMouseClick.disconnect(self.click_connection)
            if self.release_connection is not None:
                self.graphics().mouseRelease.disconnect(self.release_connection)
            if self.move_connection is not None:            
                self.graphics().mouseMove.disconnect(self.move_connection)
            
            self.click_connection = None
            self.release_connection = None
            self.move_connection = None
        
        def end(event):
            update(event)
            disconnect()
            
                        
        self.click_connection = self.graphics().leftMouseClick.connect(start)        
        self.release_connection = self.graphics().mouseRelease.connect(end)
        
        
            
        
        
        
        
    

        
