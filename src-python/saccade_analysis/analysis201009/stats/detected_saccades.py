import numpy
from reprep import Report
from .utils import attach_description

description = """
This is a plot of the detected saccades
superimposed to the raw orientation data. Each saccade is 
represented by two vertical lines: blue for start and green for the end. 
"""

def plot_detected_saccades(sample, exp_data, configuration, saccades):
    thetas = exp_data[:]['orientation']
    T = exp_data[:]['timestamp']
    
    r = Report()
    attach_description(r, description)
    
    f = r.figure(cols=2, caption='Detected saccades')
    
    dt = T[1] - T[0]
    chunk_length = 15 # seconds
    
    
    chunk_size = numpy.ceil(chunk_length / dt)
    num_chunks = int(numpy.ceil(len(T) / chunk_size))

    # oopsi, we start from 0 in the saccades
    # FIXME: detect this
    if len(saccades) and saccades[0]['time_start'] < 100000:
        print "Fixing saccades timestamp for sample %r, configuration %r" % (sample, configuration)
        saccades = numpy.array(saccades, dtype=saccades.dtype)
        for i in range(len(saccades)):
            saccades[i]['time_start'] += T[0]
            saccades[i]['time_stop'] += T[0]

    for i in range(num_chunks):
        start = i * chunk_size
        stop = min(start + chunk_size, len(T))
        
        if stop - start < 10:
            continue 
        
        theta_i = thetas[start:stop]
        T_i = T[start:stop]
        
        T_norm = T_i - T[0]
        
        caption = 'Chunk %d (from time %.1f to %.1f)' % (i, T_norm[0], T_norm[-1])
        node_id = 'chunk%d' % i
        
        s = 2.5
        with r.data_pylab(node_id, figsize=(8 * s, 1.5 * s)) as pylab:
            pylab.plot(T_norm, theta_i, 'k-')
            
            pylab.xlabel('time (s)')
            pylab.ylabel('orientation (deg)')
            #a = pylab.axis()
                       
            interval = 90 # deg
            ub = int(numpy.ceil(max(theta_i) / interval))
            lb = int(numpy.floor(min(theta_i) / interval))
            if ub == lb:
                lb = ub - 1
            a = [T_norm[0], T_norm[-1], lb * interval - 15, ub * interval + 15]
            
            for k in range(lb, ub + 1):
                line_theta = k * interval
                pylab.plot([a[0], a[1]], [line_theta, line_theta], 'k--')
    
    
    
    
            in_range = numpy.logical_and(saccades[:]['time_start'] >= T_i[0],
                                         saccades[:]['time_start'] <= T_i[-1])
            
            for saccade in saccades[in_range]: 
                tstart = saccade['time_start'] - T[0]
                tstop = saccade['time_stop'] - T[0]
                
                pylab.plot([tstart, tstart], [a[2], a[3]], 'b-')
                pylab.plot([tstop, tstop], [a[2], a[3]], 'g-')
                 
    
            
            pylab.axis(a)
        
        f.sub(node_id, caption=caption)
    
    
    # r.table('saccades', saccades)
    
    return r
