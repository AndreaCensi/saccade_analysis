from contracts import contract
import numpy as np 
import itertools
from collections import namedtuple

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
        
        self.d_edges = get_distance_edges(arena_radius=arena_radius - min_distance,
                                     n=ncells_distance)
        self.a_edges = np.linspace(-180, 180, ncells_axis_angle + 1)

    Cell = namedtuple('Cell', 'a d a_min a_max d_min d_max')
    def iterate_cells(self):
        nd = len(self.d_edges) - 1
        na = len(self.a_edges) - 1

        for a, d  in itertools.product(range(na), range(nd)):
            a_min = self.a_edges[a + 0] - self.bin_enlarge_angle
            a_max = self.a_edges[a + 1] + self.bin_enlarge_angle
            d_min = self.d_edges[d + 0] - self.bin_enlarge_dist
            d_max = self.d_edges[d + 1] + self.bin_enlarge_dist
            yield CellsDivision.Cell(a=a, d=d, a_min=a_min, a_max=a_max,
                                     d_min=d_min, d_max=d_max)

@contract(arena_radius='>0', n='int,>2,N', returns='array[N+1]')
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


def compute_histogram(rows, ncells_distance, ncells_axis_angle,
                      bin_enlarge_dist=0, bin_enlarge_angle=0):

    d_edges = get_distance_edges(arena_radius=1, n=ncells_distance)
    a_edges = np.linspace(-180, 180, ncells_axis_angle + 1)
    
    nd = ncells_distance
    na = ncells_axis_angle
    
    axis_angle = rows['axis_angle']
    distance = rows['distance_from_wall']
    linear_velocity_modulus = rows['linear_velocity_modulus']

    
    count = np.zeros((nd, na)) 
    mean_speed = np.zeros((nd, na)) 
    time_spent = np.zeros((nd, na)) 
    
    for d in range(nd):
        for a in range(na):
            a_min = a_edges[a + 0] - bin_enlarge_angle
            a_max = a_edges[a + 1] + bin_enlarge_angle
            d_min = d_edges[d + 0]
            d_max = d_edges[d + 1]
            d_min -= bin_enlarge_dist
            d_max += bin_enlarge_dist
            
          
            inside = np.logical_and(
                        linear_velocity_modulus > 0.04,
                                    np.logical_and(
                                     np.logical_and(
                   axis_angle >= a_min,
                  axis_angle <= a_max),
                                      np.logical_and(
                  distance >= d_min,
                  distance <= d_max)
                ))
            inside_rows = rows[inside]
            speed = rows[inside]['linear_velocity_modulus']

            
            count[d, a] = len(inside_rows)
            
            if count[d, a] == 0:
                print('Warning, no data for [%g,%g], [%g, %g]' % 
                      (a_min, a_max, d_min, d_max))
                mean_speed[d, a] = np.NaN
                time_spent[d, a] = 0 
            
            else:
            
                mean_speed[d, a] = speed.mean()
                time_spent[d, a] = (1.0 / speed).sum() 
            
    
    print('Length: %d; accounted: %d' % (len(rows), count.sum()))
    
    probability = time_spent * 1.0 / time_spent.sum() 
    
    return dict(distance_edges=d_edges,
                axis_angle_edges=a_edges,
                count=count,
                probability=probability,
                time_spent=time_spent,
                mean_speed=mean_speed)


def compute_histogram_saccades(saccades, stats, bin_enlarge_dist=0, bin_enlarge_angle=0):
    ''' Returns a dictionary with the fields:
    
            distance_edges=d_edges,
                axis_angle_edges=a_edges,
                total=count,
                num_left=num_left,
                num_right=num_right
    '''
    d_edges = stats['distance_edges']
    a_edges = stats['axis_angle_edges']
    
    nd = len(d_edges) - 1
    na = len(a_edges) - 1
    
    axis_angle = saccades['axis_angle']
    distance = saccades['distance_from_wall']

    
    count = np.zeros((nd, na)) 
    num_left = np.zeros((nd, na)) 
    num_right = np.zeros((nd, na))  
     
    for d in range(nd):
        for a in range(na):
            a_min = a_edges[a + 0] - bin_enlarge_angle
            a_max = a_edges[a + 1] + bin_enlarge_angle
            d_min = d_edges[d + 0]
            d_max = d_edges[d + 1]
            d_min -= bin_enlarge_dist
            d_max += bin_enlarge_dist
            
            inside = np.logical_and(
                     np.logical_and(
                                    axis_angle >= a_min ,
                                    axis_angle <= a_max),
                     np.logical_and(
                  distance >= d_min ,
                  distance <= d_max)
                )
            inside_saccades = saccades[inside]

            
            count[d, a] = len(inside_saccades)
            num_left[d, a] = (inside_saccades['sign'] == +1).sum()
            num_right[d, a] = (inside_saccades['sign'] == -1).sum()
             
            
    
    return dict(distance_edges=d_edges,
                axis_angle_edges=a_edges,
                total=count,
                num_left=num_left,
                num_right=num_right)

