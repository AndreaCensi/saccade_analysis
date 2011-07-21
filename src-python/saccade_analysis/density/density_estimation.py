from contracts import contract
import numpy as np 
import itertools

class Cell:
    
    def __init__(self, a, d, a_min, a_max, d_min, d_max):
        self.a = a
        self.d = d
        self.a_min = a_min
        self.a_max = a_max
        self.d_min = d_min
        self.d_max = d_max
        self.k = (d, a)
        
    @contract(axis_angle='array[K](>=-180,<=180)', distance='array[K](>=0)')
    def inside(self, axis_angle, distance):
        And = np.logical_and
        inside_a = And(axis_angle >= self.a_min,
                        axis_angle <= self.a_max)
        inside_d = And(distance >= self.d_min,
                       distance <= self.d_max)
        return And(inside_a, inside_d)
    
    def __str__(self):
        return 'C(%.2f<=d<=%.2f;%3d<=a<=%3d)' % (self.d_min, self.d_max,
                                                 self.a_min, self.a_max)
        
        
class CellsDivision: 
    
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
            yield Cell(a=a, d=d,
                       a_min=a_min, a_max=a_max,
                       d_min=d_min, d_max=d_max)

@contract(arena_radius='>0', n='int,>2,N', returns='array[N+1](>=0)')
def get_distance_edges(arena_radius, n):
    ''' Returns n+1 edges for a division of the distance from the wall, 
        such that 
        each one has equal area.  
    '''
    R = arena_radius
    A = np.pi * R ** 2
    
    target_areas = np.linspace(A, 0, n + 1)
    
    edges = R - np.sqrt(target_areas / np.pi) 
    
    return edges


def compute_histogram(rows, cells, vel_threshold=0.05):
    axis_angle = rows['axis_angle']
    distance = rows['distance_from_wall']
    linear_velocity_modulus = rows['linear_velocity_modulus']

    count = np.zeros(cells.shape, dtype='int')
    mean_speed = np.zeros(cells.shape)
    time_spent = np.zeros(cells.shape)
    
    for c in cells.iterate():
        incell = c.inside(axis_angle=axis_angle,
                            distance=distance)
        fast = linear_velocity_modulus > vel_threshold
        
        inside = np.logical_and(incell, fast)
        
        inside_rows = rows[inside]
        speed = rows[inside]['linear_velocity_modulus']

        
        count[c.k] = len(inside_rows)
        
        if count[c.k] == 0:
            print('Warning, no data for %s' % str(c))
            mean_speed[c.k] = np.NaN
            time_spent[c.k] = 0 
        else:
            mean_speed[c.k] = speed.mean()
            time_spent[c.k] = (1.0 / speed).sum() 
            
    
    print('Length: %d; accounted: %d' % (len(rows), count.sum()))
    
    probability = time_spent * 1.0 / time_spent.sum() 
    
    return dict(count=count,
                probability=probability,
                time_spent=time_spent,
                mean_speed=mean_speed,
                cells=cells)


def compute_histogram_saccades(saccades, cells):
    ''' Returns a dictionary with the fields:
                
                cells
                total=count,
                num_left=num_left,
                num_right=num_right
    '''

    axis_angle = saccades['axis_angle']
    distance = saccades['distance_from_wall']
  
    count = np.zeros(cells.shape, dtype='int') 
    num_left = np.zeros(cells.shape, dtype='int') 
    num_right = np.zeros(cells.shape, dtype='int') 
     
    for c in cells.iterate(): 
        inside = c.inside(axis_angle=axis_angle, distance=distance)
          
        inside_saccades = saccades[inside]
            
        count[c.k] = len(inside_saccades)
        num_left[c.k] = (inside_saccades['sign'] == +1).sum()
        num_right[c.k] = (inside_saccades['sign'] == -1).sum()
        assert count[c.k] == num_left[c.k] + num_right[c.k]
            
    
    return dict(cells=cells,
                total=count,
                num_left=num_left,
                num_right=num_right)

