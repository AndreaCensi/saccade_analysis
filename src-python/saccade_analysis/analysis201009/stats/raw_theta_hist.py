import numpy
from reprep import Report

from .utils import attach_description

description = """This figure shows an histogram of the raw orientation values. """

def raw_theta_hist(sample, exp_data): #@UnusedVariable
    thetas = numpy.fmod(exp_data[:]['orientation'] + 360, 360)    
        
    r = Report()
    attach_description(r, description)
    with r.data_pylab('simulated_trajectory') as pylab:
        pylab.hist(thetas, bins=90, normed=True) 
        pylab.xlabel('orientation (degrees)') 
        pylab.ylabel('density')
        # TODO: choose ymax
        a = pylab.axis()
        pylab.axis([0, 360, 0, a[3]])

    return r
    
    
