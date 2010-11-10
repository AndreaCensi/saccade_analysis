from reprep import Report
import numpy
from saccade_analysis.analysis201009.stats.utils import attach_description
 
description = """
This figure shows the distribution of the values of {var.name}.
The interval [{lb:.3f}, {ub:.3f}] is divided in {var.density_bins:d}.
""" 
 

def sample_var_hist(sample, expdata, configuration, saccades, variable):
    lb = variable.interesting[0]
    ub = variable.interesting[1]
    
    x = saccades[variable.field]
    if variable.mod:
        M = variable.interesting[1]
        x = numpy.fmod(x + M, M)
    
    # TODO: we don't strictly enforce the bounds and we do not compute
    # how many are left out
    hist, bin_edges = numpy.histogram(x, bins=variable.density_bins,
                range=variable.interesting, normed=True)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
     
    r = Report()
    attach_description(r, description.format(var=variable, ub=ub, lb=lb))
    with r.data_pylab('histogram') as pylab:
        pylab.plot(bin_centers, hist, 'b-')
        
        pylab.ylabel('density')
        pylab.xlabel('%s (%s)' % (variable.name, variable.unit))
        
        pylab.axis([lb, ub, 0, variable.density_max_y])
    return r
 

def group_var_hist(group, configuration, saccades, variable):
    lb = variable.interesting[0]
    ub = variable.interesting[1]
    
    x = saccades[variable.field]
    
    if variable.mod:
        M = variable.interesting[1]
        x = numpy.fmod(x + M, M)


    hist, bin_edges = numpy.histogram(x, bins=variable.density_bins,
                range=variable.interesting, normed=True)

    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    r = Report()
    attach_description(r, description.format(var=variable, ub=ub, lb=lb))

    with r.data_pylab('histogram') as pylab:
        pylab.plot(bin_centers, hist, 'b-')
        
        pylab.ylabel('density')
        pylab.xlabel('%s (%s)' % (variable.name, variable.unit))
        
        pylab.axis([lb, ub, 0, variable.density_max_y])
    return r

