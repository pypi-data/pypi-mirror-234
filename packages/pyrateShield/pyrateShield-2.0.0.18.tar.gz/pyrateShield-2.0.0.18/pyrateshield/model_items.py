from pyrateshield import labels
from pyrateshield.modelitem import ModelItem
from pyrateshield.dosemapper import Dosemapper, get_critical_point

from pyrateshield.constants import CONSTANTS
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF

import math
def ZERO_VERTICES():
    return [[0, 0], [0, 0]]

def ZERO_POSITION():
   return [0, 0]      

def EMPTY_MATERIALS():
    # default for shielding
    return [[labels.EMPTY_MATERIAL, 0], 
            [labels.EMPTY_MATERIAL, 0]]

class PositionModelItem(ModelItem):
    def setPositionPixels(self, pos):
        pos *= self.get_pixel_size_cm()
        self.position = [pos.x(), pos.y()]
        
    def positionPixels(self):
        return QPointF(*self.position) / self.get_pixel_size_cm()
    
    def move_pixels(self, dx, dy):
        pos_pixels = self.positionPixels()
        new_pos = QPointF(pos_pixels.x() + dx, pos_pixels.y() + dy)
        self.setPositionPixels(new_pos)
    

class Ruler(ModelItem):
    default_name = 'ruler'
    label = labels.RULERS
    
    _attr_dct = {"vertices_pixels": labels.VERTICES_PIXELS}
    _attr_defaults = {labels.VERTICES_PIXELS: ZERO_VERTICES}
    
        
    def tooltip(self):
        return f'Distance: {self.length_cm} cm'
        
    @property
    def vertices(self):
        psize = self.get_pixel_size_cm()
        return [[vi*psize for vi in vii] for vii in self.vertices_pixels]
    
    @vertices.setter
    def vertices(self, vertices):
        psize = self.get_pixel_size_cm()
        vp =  [[vi/psize for vi in vii] for vii in vertices]
        self.vertices_pixels = vp
    
    @property
    def length_pixels(self):
        p1, p2 = self.vertices_pixels
        x1, y1 = p1
        x2, y2 = p2
        return ((x2-x1)**2 + (y2-y1)**2)**0.5
        
    @property
    def length_cm(self):
        return self.length_pixels * self.get_pixel_size_cm()
    
    def move_pixels(self, dx, dy):
        new_vp = []
        for vp in self.vertices_pixels:
            new_vp.append([vp[0]+dx, vp[1]+dy])
        self.vertices_pixels=new_vp
        
    @property
    def angle(self):
         vvp = self.vertices_pixels
         dx = vvp[1][0] - vvp[0][0]
         dy = vvp[1][1] - vvp[0][1]
         return math.degrees(math.atan2(dy, dx))
     
    def isClosed(self):
         return False
        

class Material(ModelItem):
    # buildup table and attenuation table are used by pyshield only
    default_name = 'material'
    label = labels.MATERIALS
    _attr_dct = {
        "name": labels.NAME,
        "density": labels.DENSITY,
        "attenuation_table": labels.ATTENUATION_TABLE,
        "buildup_table": labels.BUILDUP_TABLE,
        "radtracer_material": labels.RADTRACER_MATERIAL
    }
    
    _attr_defaults = {labels.NAME: default_name,
                      labels.DENSITY: 1,
                      labels.ATTENUATION_TABLE: labels.EMPTY_TABLE,
                      labels.BUILDUP_TABLE: labels.EMPTY_TABLE,
                      labels.RADTRACER_MATERIAL: labels.EMPTY_MATERIAL}
                      
    
class Shielding(ModelItem):
    default_name = 'shielding'
    label = labels.SHIELDINGS

    _attr_dct = {
        "name": labels.NAME,
        "color": labels.COLOR,
        "linewidth": labels.LINEWIDTH,
        "materials": labels.MATERIALS,
        
    }
    
    _attr_defaults = {labels.NAME: default_name,
                      labels.COLOR: 'black',
                      labels.LINEWIDTH: 2,
                      labels.MATERIALS: EMPTY_MATERIALS}
    
                 
   
    
    
class Clearance(ModelItem):
    default_name = 'clearance'
    label = labels.CLEARANCE
    
    _attr_dct = {
        "name": labels.NAME,
        'apply_fraction1': labels.APPLY_FRACTION1,
        'apply_fraction2': labels.APPLY_FRACTION2,
        "fraction1": labels.DECAY_FRACTION1,
        "fraction2": labels.DECAY_FRACTION2,
        "half_life1": labels.HALFLIFE1,
        'half_life2': labels.HALFLIFE2,    
        'apply_split_fractions': labels.ENABLE_SPLIT_FRACTIONS,
        'split_time': labels.SPLIT_FRACTION_TIME}
       
    
    
    _attr_defaults = {labels.NAME: default_name,
                      labels.APPLY_FRACTION1: False,
                      labels.DECAY_FRACTION1: 0,
                      labels.HALFLIFE2: float('Inf'),
                      labels.APPLY_FRACTION2: False,
                      labels.DECAY_FRACTION2: 0,
                      labels.HALFLIFE1: float('Inf'),          
                      labels.ENABLE_SPLIT_FRACTIONS: False,
                      labels.SPLIT_FRACTION_TIME: 24}
    
            
    
    def is_equal(self, other):
        if isinstance(other, Clearance):
            eq = True
            for attr in self._attr_dct.keys():
                if attr == 'name': continue
                eq = eq and (getattr(self, attr) == getattr(other, attr))
            return eq
        else:
            return False
        
    
    # LEGACY, Old psp files use single half_life
    @classmethod
    def from_half_life(cls, half_life):
        return cls(fraction1=1,
                   half_life1=half_life)
        


class Wall(PositionModelItem):
    label = labels.WALLS

    _attr_dct = {
        "vertices": labels.VERTICES, 
        "shielding": labels.SHIELDING,
        "closed": labels.CLOSED
    }
    
    _attr_defaults = {
        labels.VERTICES: ZERO_VERTICES,
        labels.SHIELDING: labels.EMPTY_SHIELDING,
        labels.CLOSED: False
    }
    
    def __len__(self):
        return len(self.vertices)
    
    def isClosed(self):
        return self.closed and len(self) > 2
    
    def isClosable(self):
        return not self.closed and len(self) > 2
    
    def close(self):
        self.closed=True
        
        
    def open(self, index):
       
        if index < 0 or index < len(self.vertices) - 1:
            self.vertices = self.vertices[index+1:] + self.vertices[0:index+1]
            
        self.closed = False
        
    def positionPixels(self):                
        return self.vertices2poly(self.vertices, self.get_pixel_size_cm())
    def setPositionPixels(self, poly):
        self.vertices = self.poly2vertices(poly, self.get_pixel_size_cm())
        
    def insertVertexPixelPoint(self, index, vertex):
        self.insertVertex(index, [vertex.x()*self.get_pixel_size_cm(),
                                  vertex.y()*self.get_pixel_size_cm()])
        
    def move_pixels(self, dx, dy):
        poly = self.positionPixels()
        moved_poly = QPolygonF()
        for i in range(poly.size()):
            moved_poly.append(poly[i]+QPointF(dx, dy))
            
        self.setPositionPixels(moved_poly)
            
        
    def insertVertex(self, index, vertex):
        self.valid_vertex(vertex)
        old_value = [[vi for vi in vii] for vii in self.vertices]
        self.vertices.insert(index, vertex)
        
        self.update_event.emit([self, labels.VERTICES, old_value, self.vertices])
        
    def deleteVertex(self, index):  
        if len(self) == 2:
            raise IndexError()
        old_value = [[vi for vi in vii] for vii in self.vertices]
        self.vertices.pop(index)
        if len(self) == 2:
            self.closed = False            
        self.update_event.emit([self, labels.VERTICES, old_value, self.vertices])
        
    def setVertexPixelPoint(self, index, vertex):
        self.setVertex(index, [vertex.x()*self.get_pixel_size_cm(),
                               vertex.y()*self.get_pixel_size_cm()])
        
    def closestVertexToPixelPoint(self, point):
        distance = [((pi.x() - point.x())**2 + (pi.y() - point.y())**2)** 0.5\
                    for pi in self.positionPixels()]
        index = distance.index(min(distance))
        return index, self.positionPixels()[index], min(distance)
            
        
    def setVertex(self, index, vertex):
        old_value = [[vi for vi in vii] for vii in self.vertices]
        self.valid_vertex(vertex)            
        self.vertices[index] = vertex 
        self.update_event.emit([self, labels.VERTICES, old_value, self.vertices])
        
    def equal_vertices(vertices1, vertices2):
        if vertices1 is None and vertices2 is None:
            return True
        elif vertices1 is None or vertices2 is None:
            return False
        
        
        Wall.valid_vertices(vertices1)
        Wall.valid_vertices(vertices2)
        
        equal = True
        
        if len(vertices1) != len(vertices2):
            return False
        
        for vi, vii in zip(vertices1, vertices2):
            if vi[0] != vii[0] or vi[1] != vii[1]:
                equal = False
        return equal
    
    def get_shielding(self):
        if self.parent() is None:
            return None
        else:
            return self.parent().parent().shieldings.itemByName(self.shielding)
    
    @staticmethod
    def poly2vertices(poly, pixel_size_cm=1):
        return [[point.x()*pixel_size_cm, point.y()*pixel_size_cm] for point in poly]
    
    @staticmethod
    def vertices2poly(vertices, pixel_size_cm=1):
        return QPolygonF([QPointF(vi[0], vi[1])/pixel_size_cm for vi in vertices])
    
    @staticmethod
    def valid_vertex(vertex, raise_error=True):
        if isinstance(vertex, list) and len(vertex) == 2\
            and all([isinstance(value, (int, float)) for value in vertex]):
                return True   

        
        return False
    
    @staticmethod
    def valid_vertices(vertices, raise_error=True):
        if isinstance(vertices, list) and\
            all([Wall.valid_vertex(vi, raise_error=False) for vi in vertices]):
                return True
            
        if raise_error:
            msg = f'Invalid vertices of type {type(vertices)} and value {vertices}'
            raise ValueError(msg)
            
        return False
                

        
class CriticalPoint(PositionModelItem):
    default_name = 'critical point'
    label = labels.CRITICAL_POINTS

    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION, 
        "occupancy_factor": labels.OCCUPANCY_FACTOR,
        'enabled': labels.ENABLED
    }
    
    _attr_defaults = {
        labels.NAME: default_name,
        labels.POSITION: ZERO_POSITION,
        labels.OCCUPANCY_FACTOR: 1,
        labels.ENABLED: True
    }
    
    def tooltip(self):
        dose_pyshield = round(self.dose_pyshield(), 3)
        dose_radtracer = round(self.dose_radtracer(), 3)
        of = self.occupancy_factor
        dose_pyshield_of = round(dose_pyshield*of, 3)
        dose_radtracer_of = round(dose_radtracer*of, 3)
        
        if dose_pyshield == 0:
            dose_pyshield = "<1E-3"
            
        if dose_radtracer == 0:
            dose_radtracer = "<1E-3"
            
        if dose_radtracer_of == 0:
            dose_radtracer_of = "<1E-3"
            
        if dose_pyshield_of == 0:
            dose_pyshield_of = "<1E-3"

        text = super().tooltip()
        text += "Dose [mSv]:\n"
        text += f"\tpyshield: {dose_pyshield}\n"
        text += f"\tradtracer: {dose_radtracer}\n"
        text += "Dose corrected for occupancy [mSv]:\n"
        text += f"\tpyshield: {dose_pyshield_of}\n"
        text += f"\tradtracer: {dose_radtracer_of}"
        return text
    
    def dose_pyshield(self, occupancy_correction=False):
        dose = get_critical_point(self.parent().parent(), self,
                                  engine=labels.PYSHIELD, 
                                  sum_dose=True)
        if occupancy_correction:
            dose *= self.occupancy_factor
        return dose
    
    def dose_radtracer(self, occupancy_correction=False):
        dose = get_critical_point(self.parent().parent(), self,
                                  engine=labels.RADTRACER, 
                                  sum_dose=True)
        if occupancy_correction:
            dose *= self.occupancy_factor
        return dose
    

class SourceNM(PositionModelItem):
    default_name = 'source NM'
    label = labels.SOURCES_NM
    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION,  
        "number_of_exams": labels.NUMBER_OF_EXAMS,
        "isotope": labels.ISOTOPE,
        "self_shielding": labels.SELF_SHIELDING,
        "activity": labels.ACTIVITY,
        "duration": labels.DURATION,
        "apply_decay_correction": labels.APPLY_DECAY_CORRECTION,
        'clearance': labels.CLEARANCE,
        'enabled': labels.ENABLED
    }
    
    
    _attr_defaults = {
        labels.NAME: default_name,
        labels.POSITION: ZERO_POSITION,
        labels.NUMBER_OF_EXAMS: 1,
        labels.ISOTOPE: 'F-18',
        labels.SELF_SHIELDING: 'None', # must be str 'None' or 'Body' 
        labels.ACTIVITY: 1,
        labels.DURATION: 1,
        labels.APPLY_DECAY_CORRECTION: True,
        labels.CLEARANCE: labels.EMPTY_CLEARANCE,
        labels.ENABLED: True}
                

    
    @property
    def tiac(self):
        return self.time_integrated_activity_coefficient_mbqh

class SourceXray(PositionModelItem):
    default_name = 'source Xray'
    label = labels.SOURCES_XRAY
    _kvp = None
    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION, 
        "number_of_exams": labels.NUMBER_OF_EXAMS,
        "kvp": labels.KVP,
        "dap": labels.DAP,
        "enabled": labels.ENABLED,
    }
    
    _attr_defaults = {
        labels.NAME: default_name,
        labels.POSITION: ZERO_POSITION,
        labels.DAP: 1,
        labels.NUMBER_OF_EXAMS: 1,
        labels.ENABLED: True,
        labels.KVP: 100 #CONSTANTS.xray[0].kvp
        }

        

class SourceCT(PositionModelItem):
    default_name = 'source CT'
    label = labels.SOURCES_CT
    _attr_dct = {
        "name": labels.NAME,
        "position": labels.POSITION, 
        "number_of_exams": labels.NUMBER_OF_EXAMS,
        "body_part": labels.CT_BODY_PART,
        "kvp": labels.KVP,
        "dlp": labels.DLP,
        'enabled': labels.ENABLED
    }
    
    
    _attr_defaults = {
        labels.NAME: default_name,
        labels.POSITION: ZERO_POSITION,
        labels.DLP: 1,
        labels.NUMBER_OF_EXAMS: 1,
        labels.CT_BODY_PART: 'Body',
        labels.KVP: 120, #CONSTANTS.ct[0].kvp,
        labels.ENABLED: True}
        
    
    @property
    def available_kvp(self):
        return list(set([item.kvp for item in CONSTANTS.ct]))
    
   
