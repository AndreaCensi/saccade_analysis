import numpy
from reprep import Report

from .utils import attach_description

v = 0.3

description = """
This figure shows the simulated
trajectories, considering only the turns detected as saccades,
assuming that the fly flies at constant velocity (v= %.2f m/s),
and that it flies completely straight between saccades.
""" % v

def plot_simulated_sample_trajectories(
                    sample, exp_data, configuration, saccades): #@UnusedVariable
    x = [0]
    y = [0]
    theta = 0 
    for saccade in saccades:
        dt = saccade['time_passed']
        xp = x[-1] + numpy.cos(theta) * dt * v
        yp = y[-1] + numpy.sin(theta) * dt * v
        
        x.append(xp)
        y.append(yp)
        
        theta += numpy.radians(saccade['amplitude']) * saccade['sign']
        
    r = Report()
    attach_description(r, description)
    
    with r.data_pylab('simulated_trajectory') as pylab:
        pylab.plot(x, y, 'b-')
        pylab.xlabel('x position (m)') 
        pylab.ylabel('y position (m)')
        pylab.axis('equal')
        
    return r
