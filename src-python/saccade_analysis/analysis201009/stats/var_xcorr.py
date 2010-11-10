from reprep import Report
from saccade_analysis.analysis201009.stats.utils import iterate_over_samples, \
    attach_description
from saccade_analysis.analysis201009.stats.math_utils import xcorr

description = """
This figure shows the autocorrelation of {var.name}. 
"""

def group_var_xcorr(group, configuration, saccades, variable):
    r = Report()
    attach_description(r, description.format(var=variable))

    with r.data_pylab('%s_xcorr' % variable.id) as pylab:
        for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
            x = saccades_for_sample[variable.field]
            x = x.astype('float32')
            xc, lags = xcorr(x, maxlag=10)
            pylab.plot(lags, xc, 'x-')
        pylab.axis([-10, 10, -0.5, 1.1])
        pylab.ylabel('cross-correlation')
        pylab.xlabel('interval in sequence')
    
    return r
