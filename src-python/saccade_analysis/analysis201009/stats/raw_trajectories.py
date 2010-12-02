import numpy
from reprep import Report

from .utils import attach_description

v = 0.3

description = """
This figure shows the simulated
trajectories assuming that the fly flies at constant velocity (v= %.2f m/s).
""" % v

def plot_raw_trajectories(sample, exp_data):
    thetas = numpy.radians(exp_data[:]['orientation'])
    T = exp_data[:]['timestamp']
    
    x = [0]
    y = [0]
    
    dt = T[1] - T[0]  
    for i in range(len(thetas)):
        theta = thetas[i]
        xp = x[-1] + numpy.cos(theta) * dt * v
        yp = y[-1] + numpy.sin(theta) * dt * v
        
        x.append(xp)
        y.append(yp)        
        
    r = Report()
    attach_description(r, description)
    with r.data_pylab('simulated_trajectory') as pylab:
        pylab.plot(x, y, 'b-') 
        pylab.xlabel('x position (m)') 
        pylab.ylabel('y position (m)')
        pylab.axis('equal')

    return r
    
