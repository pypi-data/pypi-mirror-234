# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 14:41:18 2022

@author: 757021
"""
from PyQt5.QtCore import pyqtSignal, QAbstractListModel, Qt, QModelIndex
from pyrateshield import model_items, labels
import qtawesome as qta

import yaml


class ModelItemSequence(QAbstractListModel):
    nameChanged = pyqtSignal(str, str)
    valueChanged = pyqtSignal(object)
    
    default_item_name = None
    empty_item_name = None
    
    def __init__(self, *args, items=None,  **kwargs):
        QAbstractListModel.__init__(self, *args, **kwargs)
        
        items = items or []
        
        if self.empty_item_name is not None:
            names = [item.name for item in items]
            if self.empty_item_name not in names:
                items = [self.item_class(name=self.empty_item_name), *items]
       
        self.items = []
        for item in items:
            self.addItem(item)
    
    # Tricky stuff to make the object pickable
    def __getstate__(self):
        return {'items': [item.to_dict() for item in self.items]}
    
    def __setstate__(self, dct):        
        self.__dict__ = dct
        self.items = [self.item_class.from_dict(item) for item in self.items]
    # End tricky stuff
        
    def __getitem__(self, index):
        return self.items[index]
    
    def __len__(self):
        return len(self.items)
    
    def __str__(self):
        return yaml.dump(self.to_list())
    
    def __repr__(self):
        return self.__str__()
    
    
    def data(self, index, role):

        row = index.row()
        nrows = len(self)
        
        
        if row >= nrows:
            row = nrows - 1
            
        if role == Qt.DisplayRole:

            if row >= 0:
                item = self[row]
            else:
                item = None
                
            
            if hasattr(item, 'name'):
                return item.name
            elif item is not None:
                return row
            
    def deleteItem(self, item):
        if hasattr(item, 'name') and item.name == self.empty_item_name:
            return False
       
        index = self.items.index(item)
        index = self.createIndex(self.items.index(item), 0)
        
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return False

        item = self.itemAtIndex(index)
      
        self.beginRemoveRows( self.createIndex(index.row(), 0), index.row(), 
                             index.row())

        del self.items[index.row()]
     
        self.endRemoveRows()
        
        

        return True
    
    def addItem(self, item):
    
        self.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
        item = self.checkName(item)
        self.items.append(item)     
        item.setParent(self)
        item.update_event.connect(self.emitDataChanged)
        self.endInsertRows()
        
    def addItems(self, items):
        self.beginInsertRows(QModelIndex(), len(self.items), len(self.items))
        for item in self.items:
            item.setParent(self)
            item.update_event.connect(self.emitDataChanged)
            self.items.append(item)
        self.endInsertRows()
          
    def emitDataChanged(self, event_data):
        item, label, old_value, value = event_data
        if label == labels.NAME:
            self.nameChanged.emit(old_value, value)
        self.valueChanged.emit(event_data)
        index = self.indexForItem(item)
        if index is not None:
            self.dataChanged.emit(index, index)
        
    def itemByName(self, name):
        if name not in self.itemNames():
            return None
        else:
            return self.items[self.itemNames().index(name)]
        
    def itemNames(self):
        return [item.name for item in self.items]
        
        
    def indexForItem(self, item):
        if item not in self.items:
            return None
        else:
            index = self.items.index(item)
            return self.createIndex(index, index)

    def rowCount(self, index):
        return len(self.items)
    
    def itemAtIndex(self, index):
        row = index if isinstance(index, int) else index.row()
        if len(self) == 0 or row >= len(self):
            return None
        if isinstance(index, int):
            return self.items[index]        
        elif isinstance(index, QModelIndex):
            return self.items[index.row()]
    
    def checkName(self, item):
        if hasattr(item, 'name'):
            names = [item.name for item in self.items]
            if item.name in names:
                item.name = self.get_new_name()
        return item
    
    def get_new_name(self):
        # Just add a counter to the defualt name for the new name. If new name 
        # already in self.names then the counter is increased until the
        # new name is not already in self.names
        new_name =  self.item_class.default_name + ' 1'
        i = 1
        while new_name in [item.name for item in self.items]:
            i += 1
            new_name = self.item_class.default_name + ' ' + str(i)
        return new_name  
    
    @classmethod
    def from_list(cls, items):
        return cls(items=[cls.item_class.from_dict(item) for item in items])
    
    
    def to_list(self):
        return [item.to_dict() for item in self.items]

class CriticalPoints(ModelItemSequence):
    item_class = model_items.CriticalPoint
    default_item_name = 'critical point'

class Walls(ModelItemSequence):
    item_class = model_items.Wall
    shieldingChanged = pyqtSignal(object)
        
    def closestVertexToPixelPoint(self, position, exclude_wall=None):
        distance = float('Inf')
        closest_wall = None
        closest_index = None
        for wall in self:
            if wall is exclude_wall: continue
            index, vertex, di = wall.closestVertexToPixelPoint(position)
            if di < distance:
                closest_wall = wall
                closest_index = index
                distance = di
        return closest_wall, closest_index, distance
                
    def emitDataChanged(self, event_data):     
        super().emitDataChanged(event_data)
        item, label, old_value, value = event_data
        if label == labels.SHIELDING:                     
            self.shieldingChanged.emit(item)
            
    def simplifiedWalls(self):
        walls = []
        for item in self:            
            for i in range(0, len(item.vertices)-1):
                wall = item.from_dict(item.to_dict()) # copy 
                wall.vertices = item.vertices[i: i + 2]
                walls += [wall]
            if item.isClosed():
                wall = item.from_dict(item.to_dict())
                wall.vertices = [wall.vertices[-1], wall.vertices[0]]
                walls += [wall]
        return walls
                                                
            
class SourcesNM(ModelItemSequence):
    item_class = model_items.SourceNM

class SourcesXray(ModelItemSequence):
    item_class = model_items.SourceXray

class SourcesCT(ModelItemSequence):
    item_class = model_items.SourceCT
 
class Clearances(ModelItemSequence):
    item_class = model_items.Clearance
    
    empty_item_name = labels.EMPTY_CLEARANCE
    
    def items_in_use(self):
        item_names = [source.clearance for source in self.parent().sources_nm]
        items =  [self.itemByName(name) for name in item_names]
        return items
        
    
class Materials(ModelItemSequence):
    item_class = model_items.Material
    empty_item_name = labels.EMPTY_MATERIAL
    
    def items_in_use(self):
    
        item_names = []
        for shielding in self.parent().shieldings:
            item_names += [shielding.materials[0][0]]
            if len(shielding.materials) > 1:
                item_names += [shielding.materials[1][0]]
        item_names = list(set(item_names))
        items = [self.itemByName(name) for name in item_names]
        return items
    
class Shieldings(ModelItemSequence):
    item_class = model_items.Shielding
    styleChanged = pyqtSignal(object)
    empty_item_name = labels.EMPTY_SHIELDING

    def emitDataChanged(self, event_data):
        super().emitDataChanged(event_data)
        item, label, old_value, value = event_data
        if label in (labels.COLOR, labels.LINEWIDTH):                     
            self.styleChanged.emit(item)
            
    def items_in_use(self):    
        item_names = [wall.shielding for wall in self.parent().walls]
        items =  [self.itemByName(name) for name in item_names]
        return items
    
    def data(self, index, role):
        if role == Qt.DecorationRole:
            item = self.itemAtIndex(index)
            if item is not None:
                return qta.icon('mdi.wall', color=item.color)
        else:
            return super().data(index, role)
        
    
    
class Rulers(ModelItemSequence):
    item_class = model_items.Ruler