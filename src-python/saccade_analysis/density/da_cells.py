from . import  np, contract
import itertools
from saccade_analysis.density.density_estimation import get_distance_edges


class DACell:
    ''' d = index
        a = index 
    '''
    
    def __init__(self, a, d, a_min, a_max, d_min, d_max):
        self.a = a
        self.d = d
        self.a_min = a_min
        self.a_max = a_max
        self.d_min = d_min
        self.d_max = d_max
        self.a_center = 0.5 * (a_min + a_max)
        self.d_center = 0.5 * (d_min + d_max)
        self.k = (d, a)
        
    @contract(axis_angle='array[K](>=-180,<=180)', distance='array[K](>=0)')
    def inside(self, axis_angle, distance):
        And = np.logical_and
        # TODO: check +- 180deg 
        inside_a = And(axis_angle >= self.a_min,
                       axis_angle <= self.a_max)
        inside_d = And(distance >= self.d_min,
                       distance <= self.d_max)
        return And(inside_a, inside_d)
    
    def __str__(self):
        return 'C(%.2f<=d<=%.2f;%3d<=a<=%3d)' % (self.d_min, self.d_max,
                                                 self.a_min, self.a_max)
        
        
class DACells: 
    
    def __init__(self, ncells_distance, ncells_axis_angle,
                        arena_radius, min_distance,
                        bin_enlarge_angle,
                        bin_enlarge_dist):
        self.ncells_distance = ncells_distance
        self.ncells_axis_angle = ncells_axis_angle
        self.min_distance = min_distance
        self.bin_enlarge_dist = bin_enlarge_dist
        self.bin_enlarge_angle = bin_enlarge_angle
        
        d_edges = get_distance_edges(arena_radius=arena_radius,
                                     n=ncells_distance)
        #print('At first:  %.3f <= d <= %.3f' % (d_edges[0], d_edges[-1]))
        m = np.min(np.nonzero(d_edges >= min_distance))
        d_edges = d_edges[m:]
        
        #print('Now edges: %.3f <= d <= %.3f' % (d_edges[0], d_edges[-1]))
        self.d_edges = d_edges
        self.a_edges = np.linspace(-180, 180, ncells_axis_angle + 1)
        self.nd = len(self.d_edges) - 1
        self.na = len(self.a_edges) - 1
        self.shape = ((self.nd, self.na))
                
    def zeros(self, dtype='float32'):
        ''' Returns a zero array with the same shape. '''
        return np.zeros(self.shape, dtype=dtype)
        
    def iterate(self):
        for a, d  in itertools.product(range(self.na), range(self.nd)):
            a_min = self.a_edges[a + 0] - self.bin_enlarge_angle
            a_max = self.a_edges[a + 1] + self.bin_enlarge_angle
            d_min = self.d_edges[d + 0] - self.bin_enlarge_dist
            d_max = self.d_edges[d + 1] + self.bin_enlarge_dist
            yield DACell(a=a, d=d,
                       a_min=a_min, a_max=a_max,
                       d_min=d_min, d_max=d_max)
            
    def closest_cell(self, distance, angle_deg):
        ''' Returns the index of the closest cell. '''
        d = closest_cell_in_edges(self.d_edges, distance)
        a = closest_cell_in_edges(self.a_edges, angle_deg)
        if d is None or a is None:
            return None
        return (d, a)
    
    @contract(field='array')
    def check_compatible_shape(self, field):
        ''' Raises an exception if the array is not of a compatible shape. '''
        if field.shape != self.shape:
            raise Exception("Not compatible shape: %r instead of %r." % 
                                (field.shape, self.shape))
        
    
@contract(edges='array[K]', v='float', returns='None|(>=0,<K)')
def closest_cell_in_edges(edges, v):
    ''' Returns the cell in which v falls. '''
    if v < edges[0] or v > edges[-1]: 
        return None
    return np.nonzero(edges >= v)[0][0] - 1
        

    
