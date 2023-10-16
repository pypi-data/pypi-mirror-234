
import time
from pyrateshield import shared, labels
from pyrateshield.constants import CONSTANTS
from pyrateshield.pyshield import isotope, doserates

import math
import numpy as np
import timeit


CUT_OFF_KEV = 30

def add_dict(dict1, dict2):
    sum_dict = dict1.copy()
    for key, value in dict2.items():
        if key in sum_dict.keys():
            sum_dict[key] += value
        else:
            sum_dict[key] = value
    return sum_dict

class H10:
    _values = {}
    @classmethod
    def h10(cls, keV, abundance):
        if (keV, abundance) not in cls._values.keys():
            value = doserates.H10(keV, abundance=abundance)
            cls._values[(keV, abundance)] = value
        return cls._values[(keV, abundance)] 
        

class GammaRayOnGrid:
    _h10 = None
    _distance_map = None
    _dose_map = None
    
    def __init__(self, position, keV=0, abundance=0, grid=None):
        self.x, self.y = float(position[0]), float(position[1])
        self.keV = keV
        self.abundance = abundance
        self.grid = grid
        self._cache = {}
            
    @property
    def h10(self):
        # uSv/ h per MBq / m2
        return H10.h10(self.keV, abundance=self.abundance)
        

    def dose_at_point(self, point):
        # mSv
        x, y = point
        distance = np.sqrt((x-self.x)**2 + (y-self.y)**2) / 100 # cm --> m
        if distance == 0:
            return float('Inf')
        else:
            dose = self.h10 / (distance**2) / 1000 #uSv --> mSv
        return dose

    @property
    def dosemap(self):
        return self.get_dosemap()

    def get_dosemap(self):
        # mSv / h per MBq / m2
        distance_map = self.grid.distance_map_meters(self.x, self.y)
        return self.h10 /  distance_map**2 / 1000 # uSv --> mSv
    
    

class IsotopeOnGrid:
    _gammarays = None
    _cache = None
    def __init__(self, grid=None, position=None, isotope_name=None):
        self.isotope_name = isotope_name
        self.position = position
        self.grid = grid
       

    def dose_at_point(self, point):
        
        dose = 0
        for gammaray in self.gammarays():
            dose += gammaray.dose_at_point(point)
           
        return dose

    @property
    def isotope(self):
        return CONSTANTS.get_isotope_by_name(self.isotope_name)
    
    @property
    def decay_constant(self):
        return np.log(2) / self.isotope.half_life
    
    @property
    def keVs(self):
        return [item[0] for item in self.isotope.spectrum if item[0] > CUT_OFF_KEV]
    
    @property
    def abundance(self):
        return [item[1]/100 for item in self.isotope.spectrum if item[0] > CUT_OFF_KEV]
    
        
    @property
    def gammarays(self):
        if self._gammarays is None:
            self._gammarays = {}
            for ei, ai in zip(self.keVs, self.abundance):
                ray = GammaRayOnGrid(grid=self.grid, keV=ei, abundance=ai, 
                                     position=self.position)
                self._gammarays[ei] = ray
                                                   
        return self._gammarays

    
class SourceWallMap():
    _intersection_map = None
    _material_map = None
    _intersection_time = 0
    _counter = 0
    def __init__(self, source=None, wall=None, dosemap=None, shielding=None,
                 materials=None):
        self.materials = materials
        self.source = source
        self.wall = wall
        self.shielding = shielding
        self.dosemap = dosemap

    @property
    def intersection_map(self):
       
        start = time.time()
        if self._intersection_map is None:
            point = self.source.position
            vertices = self.wall.vertices
            poly = shared.get_polygon(point, vertices, self.dosemap.extent)
            
            points, mask = shared.grid_points_in_polygon(self.dosemap.grid,
                                                         poly)
            
            intersection_map = shared.get_intersection_map(points, point, 
                                              vertices, mask)
            
            self._intersection_map = intersection_map
        stop = time.time()
        self._intersection_time += (stop-start)
        return self._intersection_map
    
    @property
    def material_map(self):
       
        if self._material_map is None:
            material_map = {}
            for material_name, thickness in self.shielding.materials:
                material_map[material_name] = (thickness * self.intersection_map)             
            self._material_map = material_map
            
        return self._material_map
    
    def line_intersect(self, point):
       
        if shared.intersect(*self.wall.vertices, self.source.position, point):
            return shared.get_diagonal_intersection_factor(point, self.source.position, self.wall.vertices)
        else:
             return None
            
    def line_intersect_materials(self, point):
        diag_factor = self.line_intersect(point)
        intersection_materials = {}
        
        if diag_factor:
            for material_name, thickness in self.shielding.materials:                
                intersection_materials[material_name] = thickness * diag_factor
                
            intersection_materials.pop(labels.EMPTY_MATERIAL, None)        
            
        return intersection_materials

            
class SourceWallsMap():
    _gammarays = None
    _material_map = None
    _attenuation_map = None
    _buildup_map = None
    _isotope = None
    
    
    
    def __init__(self, dosemap=None, source=None, walls=None, shieldings=None, 
                 clearance=None, materials=None, parent=None):
        
        self.source = source
        self.clearance = clearance
        self.walls = walls
        self.shieldings = shieldings 
        self._items = []
        self.dosemap=dosemap
        self.materials = materials
        self.parent = parent
        self.intersections = {}
        
        

        for wall in walls:
            shielding = shieldings.itemByName(wall.shielding)
            sw_map = SourceWallMap(source=source, wall=wall, dosemap=dosemap,
                                   shielding=shielding)
            self._items += [sw_map]
    
    @property
    def self_shielding_materials(self):
        if self.source.self_shielding == 'Body':            
            material_name = CONSTANTS.self_shielding_pyshield[labels.MATERIAL]
            thickness = CONSTANTS.self_shielding_pyshield[labels.THICKNESS]            
            return {material_name: thickness}
                    
        else:
            return {}
        
    @property
    def self_shielding_map(self):
        material_map = {}
        shielding_map = np.ones(self.dosemap.grid.X.shape)
        for material, thickness in self.self_shielding_materials.items():
            
            material_map = add_dict(material_map, {material: thickness * shielding_map})
        return material_map
            
        
    def line_intersect_materials(self, point):
        if point not in self.intersections.keys():
            materials = {}
            for item in self._items:
                materials = add_dict(materials, item.line_intersect_materials(point))
                
            materials = add_dict(materials, self.self_shielding_materials) 
            
            materials = {k: v for k, v in materials.items()\
                         if k != labels.EMPTY_MATERIAL}
            self.intersections[point] = materials
        return self.intersections[point]
    
 
    def dose_at_point(self, point):
        point = tuple(point)
        # SourceWallsMap._time
        # start = time.time()
        materials = self.line_intersect_materials(point)
        # stop = time.time()
        # SourceWallsMap._time += (stop - start)
       
        
        sumdose = 0
        for gammaray in self.isotope.gammarays.values():
            
            dose = gammaray.dose_at_point(point)
           

            for material_name, thickness in materials.items():
                material = self.materials.itemByName(material_name)
                
                
                
                attenuation = isotope.AttenuationHelper.calculate(material,
                                                                  gammaray.keV,
                                                                  thickness)
                
                
                buildup = isotope.BuildupHelper.calculate(material,
                                                          gammaray.keV, 
                                                          thickness)
                
                

                dose = dose * attenuation * buildup
                
            
                
                                
            sumdose += dose


        sumdose *= shared.tiac(self.source, self.clearance)
    
            
        sumdose *= self.self_shielding_factor
        
        
        return sumdose
     
    @property
    def self_shielding_factor(self):
        try:
            self_shielding_factor = float(self.source.self_shielding)
        except ValueError:
            self_shielding_factor = 1
        return self_shielding_factor
        
    @property
    def isotope(self):
        if self._isotope is None:

            self._isotope = IsotopeOnGrid(grid=self.dosemap.grid,
                                          position=self.source.position,
                                          isotope_name=self.source.isotope)
        return self._isotope
    
    
    def get_dosemap(self):
        dosemap = np.zeros(self.dosemap.grid.X.shape)
        for keV, gammaray in self.isotope.gammarays.items():
            #time1 = time.time()
            dosemap_keV = gammaray.dosemap
            #time2 = time.time()
            dosemap_keV *= self.attenuation_map(gammaray.keV)
            #time3 = time.time()
            dosemap_keV *= self.buildup_map(gammaray.keV)
            #time4 = time.time()
            dosemap += dosemap_keV
            #time5 = time.time()
            
            #print(time2-time1, time3-time2, time4-time3, time5-time4)
        
        dosemap *= shared.tiac(self.source, self.clearance)
        dosemap *= self.self_shielding_factor
        return dosemap
            
   
    @property
    def material_map(self):
        if self._material_map is None:
            material_map = {}
            for item in self._items:
                material_map = add_dict(material_map, item.material_map)
            
            material_map = add_dict(material_map, self.self_shielding_map)
            
            material_map = {k: v for k,v in material_map.items()\
                            if k != labels.EMPTY_MATERIAL}
            self._material_map = material_map
        return self._material_map
    
    def attenuation_map(self, keV):
        return math.prod([self.material_attenuation_map(material_name, keV)\
                          for material_name in self.material_map.keys()])
            
    def buildup_map(self, keV):
        return math.prod([self.material_buildup_map(material_name, keV)\
                          for material_name in self.material_map.keys()])
            
        
    def material_attenuation_map(self, material_name, keV):
        keV = float(keV)
        if self._attenuation_map is None:
            self._attenuation_map = {}
        
        if (material_name, keV) not in self._attenuation_map.keys():
            attenuation_map = self.get_material_attenuation_map(material_name, keV)
            self._attenuation_map[(material_name, keV)] = attenuation_map            
        return self._attenuation_map[(material_name, keV)]
            
    def get_material_attenuation_map(self, material_name, keV):
        attenuation = None
        
        if material_name in self.material_map.keys():
            material = self.materials.itemByName(material_name)
            thickness_map = self.material_map[material_name]
            
            if material.attenuation_table != labels.EMPTY_TABLE:
                attenuation = isotope.AttenuationHelper.calculate( material, 
                                                                  keV,
                                                                  thickness_map)
            
        if attenuation is None:
            attenuation = np.ones(self.dosemap.grid.X.shape)
            
        return attenuation
    
    def material_buildup_map(self, material_name, keV):
        keV = float(keV)
        if self._buildup_map is None:
            self._buildup_map = {}
        
        if (material_name, keV) not in self._buildup_map.keys():
            buildup_map = self.get_material_buildup_map(material_name, keV)
            self._buildup_map[(material_name, keV)] = buildup_map
        
        return self._buildup_map[(material_name, keV)]
    
    
    def get_material_buildup_map(self, material_name, keV):
  
        thickness = self.material_map[material_name].flatten()
        material = self.materials.itemByName(material_name)
        if any(thickness>0) and material.buildup_table != labels.EMPTY_MATERIAL:

            buildup = isotope.BuildupHelper.calculate(material, keV, thickness)
           
            buildup = buildup.reshape(self.dosemap.grid.X.shape)
            
        else:
            buildup = np.ones(self.dosemap.grid.X.shape)
    
        return buildup

    
    
class Engine:
    _source_dose_map = None
    _sources = None
    _calc_attenuation = None
    
    def __init__(self, dosemap=None, walls=None, shieldings=None,
                 sources=None, clearances=None, materials=None):
       
       
        self.dosemap=dosemap
     
        
        self.walls = walls
        self.shieldings = shieldings
        self.clearances = clearances
        self.materials = materials
    
    @property
    def calc_attenuation(self):
        if self._calc_attenuation is None:
            self._calc_attenuation = isotope.Attenuation()
        return self._calc_attenuation
        
   
        
    def dose_at_point(self, point, sources=None):
  
        self.sources = sources
        
        dose = 0
        
        for item in self._items:
            #calc = lambda: item.dose_at_point(point)
            #print('item', timeit.timeit(calc, number=1))
            dose += item.dose_at_point(point)
        
        
        return dose
    
    @property
    def sources(self):
        if self._sources is None:
            self._sources = []
        return self._sources
    
    @sources.setter
    def sources(self, sources):
        self._items = []
        self._sources = sources
        for source in self.sources:
            if not source.enabled: continue
            clearance = self.clearances.itemByName(source.clearance)
            item = SourceWallsMap(dosemap=self.dosemap,
                                  source=source,
                                  walls=self.walls,
                                  shieldings=self.shieldings,                                 
                                  clearance=clearance,
                                  materials=self.materials,
                                  parent=self)
            
            self._items += [item]
            
    def source_dosemap(self, source):
        self.sources = [source]
        # item = [item for item in self._items if item.source is source][0]
        return self._items[0].get_dosemap()
        
    
    @classmethod
    def from_pyrateshield(cls, model, sources=None):
        #grid = Grid(model.dosemap.extent, model.dosemap.shape)
        return cls(dosemap=model.dosemap, 
                   sources=sources, 
                   walls=model.walls.simplifiedWalls(),
                   shieldings=model.shieldings,
                   clearances=model.clearances,
                   materials=model.materials)
    

        
        
    
    
    
if __name__ == "__main__":
    from pyrateshield.model import Model
    import matplotlib.pyplot as plt
    
    model = Model.load_from_project_file('../../example_projects/LargeProject/project.zip')
    #model = Model.load_from_project_file('../../example_projects/SmallProject/projectTb161.zip')
    #model = Model.load_from_project_file('C:/Users/Marcel/Desktop/test.zip')
   
    
    engine = Engine.from_pyrateshield(model, sources=model.sources_nm)#[model.sources_nm[0]])
    dosemap = lambda: [engine.source_dosemap(source) for source in model.sources_nm]
    #print(timeit.timeit(dosemap, number=1))
    start = time.time()
    for i, point in enumerate(model.critical_points):
        engine.dose_at_point(point.position, sources=model.sources_nm)
        
    stop = time.time()
    
    print(stop-start)
    
       
    

    
    
        
        