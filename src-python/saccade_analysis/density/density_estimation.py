from contracts import contract
import numpy as np 


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
    ''' 
        Returns a dictionary with the fields:
                
                cells
                total=count,
                num_left=num_left,
                num_right=num_right
    '''


    axis_angle = saccades['axis_angle']
    distance = saccades['distance_from_wall']
    velocity = saccades['linear_velocity_modulus']
  
    count = np.zeros(cells.shape, dtype='int') 
    num_left = np.zeros(cells.shape, dtype='int') 
    num_right = np.zeros(cells.shape, dtype='int') 
    mean_speed_start = cells.zeros()
    
    
    for c in cells.iterate(): 
        inside = c.inside(axis_angle=axis_angle, distance=distance)
          
        inside_saccades = saccades[inside]
            
        count[c.k] = len(inside_saccades)
        num_left[c.k] = (inside_saccades['sign'] == +1).sum()
        num_right[c.k] = (inside_saccades['sign'] == -1).sum()
        assert count[c.k] == num_left[c.k] + num_right[c.k]
            
        mean_speed_start[c.k] = np.mean(velocity[inside])
    
    return dict(cells=cells,
                total=count,
                num_left=num_left,
                num_right=num_right,
                mean_speed_sac_start=mean_speed_start)

