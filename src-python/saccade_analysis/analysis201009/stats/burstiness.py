from reprep import Report
import numpy

from .utils import attach_description
description = "Histogram of intervals over geometric bins"


def interval_histogram(group, configuration, saccades):    
    interval = saccades[:]['time_passed']

    edges = (2.0 ** numpy.array(range(1,21))) / 1000
    # centers = (edges[1:]+edges[:-1])/2
    h, edges_ = numpy.histogram(interval, bins=edges, normed=True) #@UnusedVariable
    
    bin_width = numpy.diff(edges);
    hn = h / bin_width;
    
    print 'h', h
    print 'hn', hn
    print 'edges', edges
    print 'width', bin_width
                                
    r = Report()
    attach_description(r, description)
    
    node_id = 'inthist'
    with r.data_pylab(node_id) as pylab:
        pylab.loglog(bin_width, h, 'x-')
        pylab.title('not normalized')
        pylab.xlabel('interval bin width (s)')
        pylab.ylabel('density (s)')
        
    node_id = 'inthistn'
    with r.data_pylab(node_id) as pylab:
        pylab.loglog(bin_width, hn, 'x-')
        pylab.title('normalized by bin width')
        pylab.xlabel('interval bin width (s)')
        pylab.ylabel('density (s)')
        
        
    return r

