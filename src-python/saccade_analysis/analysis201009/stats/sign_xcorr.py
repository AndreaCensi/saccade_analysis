from saccade_analysis.analysis201009.stats.utils import iterate_over_samples, \
    attach_description
from saccade_analysis.analysis201009.stats.math_utils import xcorr
from reprep import Report

description = """ This figures shows the autocorrelation of 
saccades direction (left/right) in time. Negative correlation
at lag 1 means that if the fly turned left, it is more likely to
turn right, and vice verse. """

def group_sign_xcorr(group, configuration, saccades):
    r = Report()
    attach_description(r, description)

    with r.data_pylab('sign_xcorr') as pylab:
        for sample, saccades_for_sample in iterate_over_samples(saccades):
            sign = saccades_for_sample['sign']
            sign = sign.astype('float32')
            xc, lags = xcorr(sign, maxlag=10)
            pylab.plot(lags, xc, 'x-')
        pylab.axis([-10, 10, -0.5, 1.1])
        pylab.ylabel('cross-correlation')
        pylab.xlabel('interval in sequence')
    
    return r
