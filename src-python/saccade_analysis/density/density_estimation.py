from . import contract, np


@contract(arena_radius='>0', n='int,>2,N', returns='array[N+1](>=0)')
def get_distance_edges(arena_radius, n):
    ''' 
        Returns n+1 edges for a division of the distance from the wall, 
        such that each one has equal area.  
    '''
    R = arena_radius
    A = np.pi * R ** 2
    
    target_areas = np.linspace(A, 0, n + 1)
    
    edges = R - np.sqrt(target_areas / np.pi) 
    
    return edges


def compute_histogram(rows, cells, vel_threshold=0.05):
    ''' 
        Computes global statistics of the trajectories.
        
        cells: DACell structure
        rows:  flydra rows + arena position annotations
    '''

    axis_angle = rows['axis_angle']
    distance = rows['distance_from_wall']
    linear_velocity_modulus = rows['linear_velocity_modulus']
    fast = linear_velocity_modulus > vel_threshold

    count = cells.zeros('int')
    mean_speed = cells.zeros()
    time_spent = cells.zeros()
  
    samples2interval = lambda N: N / 60.0
    print('Trajectory statistics')
    print('* number of rows: %5d  length: %5s seconds.' % 
            (len(rows), samples2interval(len(rows))))
    print('* selected  rows: %5d  length: %5s seconds.' % 
            (fast.sum(), samples2interval(fast.sum())))

    print('* mean x: %10f' % np.mean(rows['x']))
    print('* mean y: %10f' % np.mean(rows['y']))


    for c in cells.iterate():
        incell = c.inside(axis_angle=axis_angle,
                            distance=distance)
        
        inside = np.logical_and(incell, fast)
        
        inside_rows = rows[inside]
        speed = rows[inside]['linear_velocity_modulus']

        count[c.k] = len(inside_rows)
        
        if count[c.k] == 0:
            print('Warning, no data for cell %s' % str(c))
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
        Computes statistics for the saccades distribution.
    
        Returns a dictionary with the fields:
                
                cells
                total=count,
                num_left=num_left,
                num_right=num_right
    '''


    print('Saccade statistics')
    print('* number of saccades: %5d ' % len(saccades))

    print saccades['position']
    print('* mean position: %s' % np.mean(saccades['position'], axis=0))

    axis_angle = saccades['axis_angle']
    distance = saccades['distance_from_wall']
    velocity = saccades['linear_velocity_modulus']
  
    count = cells.zeros('int')
    num_left = cells.zeros('int')
    num_right = cells.zeros('int')
    mean_speed_start = cells.zeros()
    

    print('Intervals of axis_angle: %s - %s' % (np.min(axis_angle),
                                                np.max(axis_angle)))
              
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






