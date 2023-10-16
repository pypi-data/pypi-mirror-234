"""
Generate dosemap, based on pre-simulated (MCNP6) transmission probabilities

Rob van Rooij
"""

import numpy as np
from skimage.draw import polygon
from scipy import interpolate
import os
import pickle

from pyrateshield.shared import time_integrated_activity_coefficient_mbqh


_folder = os.path.dirname(os.path.abspath(__file__))
MCNP_LOOKUP = pickle.load(open(os.path.join(_folder, "MCNP.pickle"), "rb"))

DEFAULT_DENSITY = { # The densities with which the MCNP simulations were run. Do not modify!
    "Water":           0.998207,
    "Lead":            11.35,
    "Concrete":        2.30,
    "Concrete-Barite": 3.35,
    "Gypsum":          1.0,
    "Brick":           1.8,
    "Tungsten":        19.3,
}


class TransmissionMCNP:
    def __init__(self, LUT):
        self.LUT = LUT
        self.interp = {}
        
    def get(self, material, thickness):
        if material not in self.LUT:
            return 1
        
        if material not in self.interp:
            x, y = self.LUT[material].T
            self.interp[material] = interpolate.interp1d(x, np.log(y), fill_value="extrapolate")
        
        return np.exp(self.interp[material](thickness))


class TransmissionArcher:
    _ALTERNATIVES = {
        "Water":  ("Concrete", 2.35, 1.0), # This makes little sense, but neither does a wall of water ;-)
        "Concrete-Barite":  ("Concrete", 2.35, 3.35),
        "Gypsum": ("Concrete", 2.35, 0.8),
        "Brick":  ("Concrete", 2.35, 1.6),
    }
    def __init__(self, archer_params):
        self.archer_params = archer_params
        
    def get(self, material, thickness):
        if material in self.archer_params:
            a, b, g = self.archer_params[material]
            
        elif material in self._ALTERNATIVES:
            alt = self._ALTERNATIVES[material]            
            print(f"No transmission parameters for {material} found. Using {alt[0]} with density {alt[2]}")
            a, b, g = self.archer_params[alt[0]]
            a *= alt[2]/alt[1]
            b *= alt[2]/alt[1]
        else:
            print(f"No transmission parameters for {material} found. Ignoring this shielding")
            return 1
            
        return ( (1 + b/a)*np.exp(a*g*thickness) - b/a )**(-1/g) 
        

def source_transmission(source, project):
    source_type = source.__class__.__name__
    
    if source_type == "SourceNM":
        name = source.isotope
        
        self_shielding_key = source.self_shielding if isinstance(source.self_shielding, str) else 'None'
        transmission = TransmissionMCNP(MCNP_LOOKUP[source.isotope][self_shielding_key])
        h_10 = MCNP_LOOKUP[source.isotope][self_shielding_key]["h(10) [uSv/h per MBq/m^2]"]
        
        clearance_model = project.clearances.itemByName(source.clearance)        
        
        source_dose = h_10 * time_integrated_activity_coefficient_mbqh(source, clearance_model=clearance_model)
        
        # Apply numeric self shielding factor here
        if isinstance(source.self_shielding, float):
            source_dose *= source.self_shielding
        
    elif source_type == "SourceCT":
        params = [x for x in project.constants.ct if x.kvp == source.kvp][0]
        transmission = TransmissionArcher(params.archer)
        scatter_frac = {
            "Body": params.scatter_fraction_body, 
            "Head": params.scatter_fraction_head}[source.body_part]
        source_dose = source.number_of_exams * source.dlp * scatter_frac
        
    elif source_type == "SourceXray":
        params = [x for x in project.constants.xray if x.kvp == source.kvp][0]
        transmission = TransmissionArcher(params.archer)
        source_dose = source.number_of_exams * source.dap * params.scatter_fraction
    else:
        raise ValueError("Source type unknown: {}".format(modality))

    return transmission, source_dose * 1E-3 #1E-3 to convert uSv to mSv


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def get_polygon(imshape, source, line):
    p1 = np.array(line[0])
    p2 = np.array(line[1])
    
    uv1 = unit_vector(p1-source)
    uv2 = unit_vector(p2-source)
    angle = np.arccos(np.clip(np.dot(uv1, uv2), -1.0, 1.0))
    
    min_dist = np.sqrt(imshape[0]**2 + imshape[1]**2)+1
    d = min_dist/np.cos(0.5*angle)

    p3 = source + d*uv1
    p4 = source + d*uv2

    poly = np.array((p1, p3, p4, p2)).T
    
    return polygon(poly[0], poly[1], imshape)


def get_diagonal_intersection_factor(poly, source_ji, vertices_ji):
    """ 
    Get diagonal distance factor through wall for every point within polygon (head-on=1, 45deg=sqrt(2))
    """
    r = (poly[0]-source_ji[0], poly[1]-source_ji[1]) # Vectors from source to points in polygon
    w = (vertices_ji[1][1]-vertices_ji[0][1], -vertices_ji[1][0]+vertices_ji[0][0]) # Vector orthogonal to wall (vec=v1-v0, w=(vec_y,-vec_x))
    r_in_w = r[0]*w[0] + r[1]*w[1] # Inner product for every vector in r with w
    mag_r_w = np.linalg.norm(r, axis=0) * (w[0]**2 + w[1]**2)**0.5 # Multiplied magnitude of vectors
    return np.abs(mag_r_w / r_in_w) # 1 / Cos(th)     ( cos(th) = u.v / (|u| |v|) )


def grid_coords(coords_cm, extent, gridshape):
    x, y = coords_cm
    x0, x1, y0, y1 = extent
    j = (y1-y)/(y1-y0) * gridshape[0] - 0.5
    i = (x-x0)/(x1-x0) * gridshape[1] - 0.5
    return np.array((j, i))

def ccw(A,B,C):
    # Is counter-clockwise?
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    # Return true if line segments AB and CD intersect
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def get_walls_by_material(project):
    wall_dict = {}    
    shielding_dict = {s.name: s for s in project.shieldings}
    for wall in project.walls.simplifiedWalls():
        shielding = shielding_dict[wall.shielding]
        
        for material_name, thickness in shielding.materials:
            material_item = project.materials.itemByName(material_name)
        
            material = material_item.radtracer_material
            density = material_item.density
            
            #Allow user-defined densities by modifying the wall thickness instead
            default_density = DEFAULT_DENSITY.get(material, 1)            
            thickness *= density/default_density
            
            entry = wall_dict.setdefault(material, [])
            entry.append( (wall.vertices, thickness) )
    return wall_dict


def pointdose_single_source(point, source, project):        
    transmission, source_dose = source_transmission(source, project)    
    total_transmission = 1
    wall_dict = get_walls_by_material(project)
    for material, wall_list in wall_dict.items():        
        cumul_thickness = 0
        for vertices, thickness in wall_list:        
            if not intersect(point, source.position, vertices[0], vertices[1]):
                continue
            diag_factor = get_diagonal_intersection_factor(point, source.position, vertices)
            cumul_thickness += thickness*diag_factor
        
        total_transmission *= transmission.get(material, cumul_thickness)

    r_squared = (point[0] - source.position[0])**2 + \
                (point[1] - source.position[1])**2
    return source_dose * total_transmission * 100**2 / r_squared


def dosemap_single_source(source, project):
    transmission, source_dose = source_transmission(source, project)
    source_ji = project.dosemap.to_grid_coords(source.position)
    transmission_map = np.ones(project.dosemap.shape)
    wall_dict = get_walls_by_material(project)
    for material, wall_list in wall_dict.items():        
        cumul_thickness_map = np.zeros(project.dosemap.shape)
        for vertices, thickness in wall_list:
            vertices_ji = [project.dosemap.to_grid_coords(vert) for vert in vertices]            
            poly = get_polygon(cumul_thickness_map.shape, source_ji, vertices_ji)
            diag_factors = get_diagonal_intersection_factor(poly, source_ji, vertices_ji)
            cumul_thickness_map[poly] += thickness*diag_factors

        if 0: # For debugging: show the cumulative thickness maps per source per material
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.imshow(cumul_thickness_map, cmap="jet")
            fig.suptitle(f"{source.name}: {material}")
            plt.show()

        transmission_map *= transmission.get(material, cumul_thickness_map)
        
    r_squared = (project.dosemap.grid.X - source.position[0])**2 + \
                (project.dosemap.grid.Y - source.position[1])**2
    return source_dose * transmission_map * 100**2 / r_squared


