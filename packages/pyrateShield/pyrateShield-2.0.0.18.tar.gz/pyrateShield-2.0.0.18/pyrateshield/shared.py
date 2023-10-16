import numpy as np
from pyrateshield.constants import CONSTANTS
from matplotlib.path import Path



def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def get_polygon(point, line, extent):
    p1 = np.asarray(line[0])
    p2 = np.asarray(line[1])

    uv1 = unit_vector(p1-point)
    uv2 = unit_vector(p2-point)

    angle = np.arccos(np.clip(np.dot(uv1, uv2), -1.0, 1.0))

    min_dist = np.sqrt((extent[3] - extent[2]) ** 2\
                      + (extent[1] - extent[0]) **2)


    d = min_dist/np.cos(0.5 * angle)

    p3 = point + d*uv1
    p4 = point + d*uv2

    poly = np.array((p1, p3, p4, p2))
    return poly


def grid_points_in_polygon(grid, poly):

    points = np.asarray([grid.X.flatten(), grid.Y.flatten()]).T

    path = Path(poly)

    inside =  path.contains_points(points)

    mask = inside.reshape(grid.X.shape)

    return points[inside], mask


def get_intersection_map(points, point, vertices, mask):
    intersection_thickness = get_diagonal_intersection_factor(points.T, point, vertices)
    intersection_map = np.zeros(mask.shape)
    intersection_map[mask] = intersection_thickness
    return intersection_map
    

# line intersections
def ccw(A,B,C):
    # Is counter-clockwise?
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A,B,C,D):
    # Return true if line segments AB and CD intersect
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def get_diagonal_intersection_factor(poly, source_ji, vertices_ji):
    """ 
    Get diagonal distance factor through wall for every point within polygon (head-on=1, 45deg=sqrt(2))
    """
    r = (poly[0]-source_ji[0], poly[1]-source_ji[1]) # Vectors from source to points in polygon
    w = (vertices_ji[1][1]-vertices_ji[0][1], -vertices_ji[1][0]+vertices_ji[0][0]) # Vector orthogonal to wall (vec=v1-v0, w=(vec_y,-vec_x))
    r_in_w = r[0]*w[0] + r[1]*w[1] # Inner product for every vector in r with w
    mag_r_w = np.linalg.norm(r, axis=0) * (w[0]**2 + w[1]**2)**0.5 # Multiplied magnitude of vectors
    return np.abs(mag_r_w / r_in_w) # 1 / Cos(th)     ( cos(th) = u.v / (|u| |v|) )



def effective_decay_constant(physical_half_life=None, biological_half_life=None):
    
    effective_decay_constant = 0
    
    if physical_half_life is not None and physical_half_life > 0:
        effective_decay_constant += np.log(2) / physical_half_life
        
    if biological_half_life is not None and biological_half_life > 0:
        effective_decay_constant += np.log(2) / biological_half_life
        
    return effective_decay_constant


def remainder(clearance_model):
    # remaining fraction decays with physical_decay
    remainder = 1
    if clearance_model.apply_fraction1:
        remainder -= clearance_model.fraction1
    if clearance_model.apply_fraction2:
        remainder -= clearance_model.fraction2
    
    return remainder


def _tiac(activity, decay_constant, start=0, end=float('inf')):
    
    if decay_constant > 0:
        tiac = activity / decay_constant * (np.exp(-decay_constant * start)\
                                            - np.exp(-decay_constant * end))
    else:
        tiac = activity * (end - start)
        
        
    return tiac
            
def tiac(source, clearance_model=None):
    return time_integrated_activity_coefficient_mbqh(source, 
                                                     clearance_model=clearance_model)


def time_integrated_activity_coefficient_mbqh(source, clearance_model=None):
    isotope = CONSTANTS.get_isotope_by_name(source.isotope)
    
    if source.apply_decay_correction:
        physical_half_life = isotope.half_life
    else:
        physical_half_life = float('inf')

    if clearance_model is not None:
        # check if one of the fractions is checked
        apply_clearance_model = clearance_model.apply_fraction1\
            or clearance_model.apply_fraction2
    else:
        apply_clearance_model = False
    
    if not apply_clearance_model:
        # just simple physical decay
        end = source.duration
        tiac =  _tiac(source.activity, np.log(2) / physical_half_life, end=end)
        
    else:
        
        tiac = 0
        
        if clearance_model.apply_fraction1:
            # first fraction 1
            decay_constant1 = effective_decay_constant(physical_half_life,
                                                      clearance_model.half_life1)
            
            # check if fractions are split in time. If split determine end
            # time either by the split time or by the duration
            if clearance_model.apply_split_fractions:                
                end1 = min(clearance_model.split_time, source.duration)
            else:
                end1 = source.duration
            
            # fraction of activity to consider
            activity = source.activity * clearance_model.fraction1
            
            # calculate tiac for the considered fraction of activity
            tiac += _tiac(activity, decay_constant1, end=end1) 
            
        if clearance_model.apply_fraction2:
            if clearance_model.apply_split_fractions\
                and clearance_model.apply_fraction1:
            
                # If split in time determine remaining activity after decay
                # of fraction 1
                activity = source.activity * np.exp(-decay_constant1 * end1)
                
                start = clearance_model.split_time
                
            else:
                # if not split in time integrate from 0
                activity = source.activity
                start = 0 
            
            # fraction of activity to consider
            activity *= clearance_model.fraction2
            
            
            decay_constant2 = effective_decay_constant(physical_half_life,
                                                       clearance_model.half_life2)
            # always integrate to the source duration for fraction 2
            end = source.duration
            
            if start >= end:
                pass
                # if start >= end the start time is later than source duration
                # tiac = 0 for fraction 2
            else:                
                tiac += _tiac(activity, decay_constant2, start=start, end=end) 
        
        
        # determine remaining fraction
        remaining_fraction = 1
        
        if clearance_model.apply_fraction1:
            remaining_fraction -= clearance_model.fraction1

        if clearance_model.apply_fraction2:
            remaining_fraction -= clearance_model.fraction2
        
        # not that remaining fraction == -2 when fractions are split in time
        if remaining_fraction > 0:             
            # activity that is remaining
            activity = source.activity * remaining_fraction
            
            # integrate from 0 to source duration for remaining fraction
            tiac += _tiac(activity,
                          np.log(2) / physical_half_life,
                          end=source.duration)
        
            
    tiac *= source.number_of_exams
    
    return tiac
            
    
    

    