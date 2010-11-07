import numpy
from reprep import Report

def plot_raw_trajectories(sample, exp_data):
    thetas = numpy.radians(exp_data['exp_orientation'])
    T = exp_data['exp_timestamps']
    
    x = [0]
    y = [0]
    v = 0.3
    dt = T[1] - T[0]  
    for i in range(len(thetas)):
        theta = thetas[i]
        xp = x[-1] + numpy. cos(theta) * dt * v
        yp = y[-1] + numpy.sin(theta) * dt * v
        
        x.append(xp)
        y.append(yp)
        
        
    r = Report()
    
    with r.data_pylab('simulated_trajectory') as pylab:
        pylab.plot(x,y,'b-') 
        pylab.xlabel('x position (m)') 
        pylab.ylabel('y position (m)')
        pylab.axis('equal')

    return r
    
    
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

def plot_sample_hist_group(group, configuration,  saccades):        
    r = Report()
    with r.data_pylab('sample_hist') as pylab:
        pylab.hist(saccades['time_passed'] )
    return r

def plot_sample_hist_sample(sample, exp_data, configuration,  saccades):        
    r = Report()
    with r.data_pylab('sample_hist') as pylab:
        pylab.hist(saccades['time_passed'] )
    return r
