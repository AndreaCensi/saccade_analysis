import numpy as np 
from contracts import contract, new_contract

def compute_visual_stimulus(stats, num_photoreceptors=180):
    ''' 
        Computes the simulated visual stimulus. 
    
        Returns the ``stats`` dictionary with the field 
        'visual_stimulus' added. For each cell, it recorded, 
        the 
    '''
    
    delta = 2 * np.pi / (num_photoreceptors - 1)
    directions = np.linspace(-np.pi + delta / 2,
                             np.pi - delta / 2, num_photoreceptors)
    
    stats['directions'] = directions
    cells = stats['cells']
    poses = stats['equiv_pose']  
    
    stimulus_dtype = [
        ('distance', ('float', num_photoreceptors)),
        ('retinal_velocities', ('float', num_photoreceptors)),
        ('optic_flow', ('float', num_photoreceptors)),
    ]
    stimulus = cells.zeros(stimulus_dtype)
    
    for c in cells.iterate():
        print('Cell %s/%s' % (c.k, poses.shape))
        pose = poses[c.k]
        distance = raytracing(x=pose['x'], y=pose['y'],
                                      theta=pose['theta'], radius=1,
                                      directions=directions)
        
        v0 = 1 # m/s
        #v = v0 * np.array([np.cos(theta), np.sin(theta)])
        v = v0 * np.array([1, 0])
        normal0 = +np.sin(directions)
        normal1 = -np.cos(directions)
        retinal_velocities = (v[0] * normal0 + v[1] * normal1) / distance
        optic_flow = retinal_velocities / distance
        stimulus[c.k]['distance'][:] = distance
        stimulus[c.k]['retinal_velocities'][:] = retinal_velocities
        stimulus[c.k]['optic_flow'][:] = optic_flow 

    stats['visual_stimulus'] = stimulus
    return stats

    

def raytracing(x, y, theta, radius, directions):
    n = directions.size
    readings = np.zeros(n)
    for i in range(n):
        direction = theta + directions[i]
        rho, coord = intersect_ray_and_circle([0, 0], radius, #@UnusedVariable
                                              eye=[x, y], eye_orientation=direction)
        readings[i] = rho
    return readings

new_contract('point2', 'seq[2](number)')

@contract(center='point2', radius='>0', eye='point2', eye_orientation='float',
          returns='tuple(>0,float)')
def intersect_ray_and_circle(center, radius, eye, eye_orientation):
    eye = np.array(eye)
    center = np.array(center)
    # First of all, translate coordinates such that the circle is at (0, 0)
    eye = eye - center
    center = np.array([0, 0])

    # next follows the algorithm from 
    # http: // mathworld.wolfram.com / Circle - LineIntersection.html    
    
    x_1 = eye[0];
    y_1 = eye[1];
    x_2 = eye[0] + np.cos(eye_orientation);
    y_2 = eye[1] + np.sin(eye_orientation);
    D = x_1 * y_2 - x_2 * y_1;
    d_x = x_2 - x_1;
    d_y = y_2 - y_1;
    d_r = np.sqrt(d_x * d_x + d_y * d_y);
    
    delta = radius * radius * d_r * d_r - D * D;
    if delta < 0:
        return None
    
    p1 = np.zeros(2)
    p2 = np.zeros(2)
    mysign = np.sign
    distance_d = lambda a, b: np.linalg.norm(a - b)
    p1[0] = (D * d_y + mysign(d_y) * d_x * np.sqrt(delta)) / (d_r * d_r);
    p2[0] = (D * d_y - mysign(d_y) * d_x * np.sqrt(delta)) / (d_r * d_r);
    p1[1] = (-D * d_x + np.abs(d_y) * np.sqrt(delta)) / (d_r * d_r);
    p2[1] = (-D * d_x - np.abs(d_y) * np.sqrt(delta)) / (d_r * d_r);
 

    # check they are on the circle
    tolerance = 1e-5
    assert(np.fabs(distance_d(p1, center) - radius) < tolerance);
    assert(np.fabs(distance_d(p2, center) - radius) < tolerance);
    
    # check that they are on the line as well
    direction = np.array([np.cos(eye_orientation), np.sin(eye_orientation)])
    normal = np.array([-direction[1], direction[0]])
    DOT = lambda a, b: (a * b).sum()
    assert(np.abs(DOT(eye, normal) - DOT(p1, normal)) < tolerance);
    assert(np.abs(DOT(eye, normal) - DOT(p2, normal)) < tolerance);
    
    # let's choose between the two
    d1 = distance_d(p1, eye);
    d2 = distance_d(p2, eye);
    # let's see if they are in front
    ok1 = DOT(direction, p1) > DOT(direction, eye);
    ok2 = DOT(direction, p2) > DOT(direction, eye);
    
    if not ok1 and not ok2:
        return None
    elif ok1 and not ok2:
        p = p1
    elif ok2 and not ok1:
        p = p2
    elif d1 < d2:
        p = p1
    else:
        p = p2
        
    coord = np.arctan2(p[1], p[0])
    
    reading = distance_d(p, eye)

    return reading, coord

