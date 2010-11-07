from reprep import Report
import numpy

def plot_simulated_sample_trajectories(sample, exp_data, configuration,  saccades):
    x = [0]
    y = [0]
    theta = 0
    v = 0.3
    for saccade in saccades:
        dt = saccade['time_passed']
        xp = x[-1] + numpy. cos(theta) * dt * v
        yp = y[-1] + numpy.sin(theta) * dt * v
        
        x.append(xp)
        y.append(yp)
        
        theta += numpy.radians(saccade['amplitude']) * saccade['sign']
        
    r = Report()
    
    with r.data_pylab('simulated_trajectory') as pylab:
        pylab.plot(x,y,'b-')
        pylab.xlabel('x position (m)') 
        pylab.ylabel('y position (m)')
        pylab.axis('equal')
        
    return r