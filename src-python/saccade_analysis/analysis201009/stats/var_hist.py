from reprep import Report
import numpy
 

def sample_var_hist(sample, expdata, configuration, saccades, variable):
    x = saccades[variable.field]
    if variable.mod:
        M = variable.interesting[1]
        x = numpy.fmod(x,M)
    
    hist, bin_edges = numpy.histogram(x, bins=variable.density_bins, 
                range=variable.interesting, normed=True)

    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
     
    r = Report()
    with r.data_pylab('histogram') as pylab:
        pylab.plot(bin_centers, hist, 'b-')
        
        pylab.ylabel('density')
        pylab.xlabel('%s (%s)' % (variable.name, variable.unit))
        
        pylab.axis([variable.interesting[0],variable.interesting[1],
                    0, variable.density_max_y])
    return r


def group_var_hist(group, configuration, saccades, variable):
    x = saccades[variable.field]
    
    # TODO: add mod()

    hist, bin_edges = numpy.histogram(x, bins=variable.density_bins, 
                range=variable.interesting, normed=True)

    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
    
    r = Report()
    with r.data_pylab('histogram') as pylab:
        pylab.plot(bin_centers, hist, 'b-')
        
        pylab.ylabel('density')
        pylab.xlabel('%s (%s)' % (variable.name, variable.unit))
        
        
        pylab.axis([variable.interesting[0],variable.interesting[1],
                    0, variable.density_max_y])
    return r

