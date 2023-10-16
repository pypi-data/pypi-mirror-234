from PyQt5.QtCore import QObject, pyqtSignal
import inspect
import yaml
from pyrateshield import labels
import pyrateshield

#LOG_LEVEL = 10

def equal_position(position1, position2):
    if  [position1, position2].count(None) == 1:
        return False
    elif [position1, position2].count(None) == 2:
        return True
    else:
        return position1[0] == position2[0]\
            and position1[1] == position2[1]
        


def equal_materials(materials1, materials2):
    if  [materials1, materials2].count(None) == 1:
        return False
    elif [materials1, materials2].count(None) == 2:
        return True
    elif len(materials1) != len(materials2):
            return False
    else:
        eq = True
        for material1, material2 in zip(materials1, materials2):
            eq = eq and material1[0] == material2[0] and material1[1] == material2[1]
        return eq
    

### Base class
class ModelItem(QObject):
    label = 'ModelItem'
    
    update_event = pyqtSignal(object)
    
    
    _attr_dct = {}
    _attr_defaults = {}   


    def __init__(self, **kwargs):        
        
        QObject.__init__(self)

        
        init_values = self._get_default_values()
        init_values.update(kwargs)
        
        for attr_name, value in init_values.items():
        
            if attr_name in self._attr_dct.keys():
                # set by attribute name
                setattr(self, attr_name, value)
            elif attr_name in self._attr_dct.values():
                # set by label
                setattr(self, self.attr_name_from_label(attr_name), value)
            else:
                pass
                #raise AttributeError(f'Cannot set {attr_name} for class {self.__class__.__name__}')
    
    # Code to make objects pickable
    def __getstate__(self):
        dct = self.to_dict()
      
        return dct
        
    def __setstate__(self, dct):
        self.__init__(**dct)
        
    # end pickable
    

    def get_pixel_size_cm(self):
        psize = 1
        if hasattr(self, 'floorplan'):
            return self.floorplan.geometry.pixel_size_cm
        elif self.parent() is not None:
            if hasattr(self.parent(), 'floorplan'):
                psize = self.parent().floorplan.geometry.pixel_size_cm
            elif hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'floorplan'):
                psize = self.parent().parent().floorplan.geometry.pixel_size_cm                
        return psize
                                            
    def get_attr_from_label(self, label):
        return getattr(self, self.attr_name_from_label(label))
        
    def delete(self):
        self.delete.emit(self)
        

    def __copy__(self):
        return self.__class__.from_dict(self.to_dict())
    
    

    @classmethod
    def _get_default_value(cls, attr_name):
        if cls._attr_dct[attr_name] in cls._attr_defaults.keys():     
            # default value defined
            value = cls._attr_defaults[cls._attr_dct[attr_name]]

        elif attr_name in cls._attr_dct.keys(): 
            # No default value but is in the attribute dct
            value = None
        else:
            # Debug purpuses should not happen for a well defined ModelItem
            raise AttributeError(f'Unknown Attribute {attr_name}')
            
        if inspect.isclass(value) or inspect.isfunction(value):
            value = value() # call or create instance
        return value
    
    @classmethod
    def _get_default_values(self):
        values = {}
        for attr_name in self._attr_dct.keys():
            values[attr_name] = self._get_default_value(attr_name)
        return values
        
    def __setattr__(self, attr_name, value):
        if attr_name not in self._attr_dct.keys():
            return super().__setattr__(attr_name, value)
        

        if hasattr(self, attr_name):
            old_value = getattr(self, attr_name)
        else: 
            super().__setattr__(attr_name, None)
            old_value = None
            
        if hasattr(self, attr_name):
            pass
            #print(f'!! set attr {attr_name} to {str(value)} from {str(old_value)} with type {type(value)}')
       
        
        # Override None values to default values                
        if value is None:            
            value = self._get_default_value(attr_name)
           
        
        if attr_name == 'materials' and isinstance(value, list)\
            and equal_materials(old_value, value):            
            return # don't set and don't emit event
                
        elif attr_name == 'position':
            value = [float(value[0]), float(value[1])] # force list!
            if equal_position(old_value, value):
                return # don't set and don't emit event
                
        elif attr_name in ('vertices', 'vertices_pixels') :# force list!    
            
            if not pyrateshield.model_items.Wall.valid_vertices(value):
                msg =f'Invalid value for vertices, {type(value)} and value {value}'
                raise ValueError(msg)
            
                
            if pyrateshield.model_items.Wall.equal_vertices(old_value, value):
                return # don't set and don't emit event
            
                
        elif attr_name == 'image': 
            if old_value is value:
                return
        else:
            if old_value == value:
                return  # don't set and don't emit event

        super().__setattr__(attr_name, value)
        
        if isinstance(value, (ModelItem, 
                      pyrateshield.model_sequences.ModelItemSequence)):
            value.setParent(self)
            
        if attr_name in self._attr_dct.keys():
            # gather event_data and emit event
            value = getattr(self, attr_name)
            label = self._attr_dct[attr_name]
            event_data = self, label, old_value, value
            
           
            self.update_event.emit(event_data)
      
            
    def update_by_dict(self, dct):
        for key, value in dct.items():
            attr_name = self.attr_name_from_label(key)
            setattr(self, attr_name, value)
          
    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)
    
    def enable(self, value):
        if labels.ENABLED in self._attr_dct.values():
            self.enabled = value
        else:
            raise AttributeError

    def to_dict(self):
        dct = {label: getattr(self, var)\
               for var, label in self._attr_dct.items()}
        return dct
    
  
    @classmethod
    def attr_name_from_label(cls, label): 
        if label in cls._attr_dct.keys():
            return label
        else:
            index = list(cls._attr_dct.values()).index(label)
            return list(cls._attr_dct.keys())[index]
    
    
    def __str__(self):
        #return "\n".join([f"{k}: {v}" for k, v in self.to_dict().items()])
        return yaml.dump(self.to_dict())
    
    def __repr__(self):
        return self.__str__()
    
    def tooltip(self):
        return str(self)
    
    

