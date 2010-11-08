from saccade_analysis.analysis201009.stats.utils import iterate_over_samples
from saccade_analysis.analysis201009.stats.math_utils import xcorr
from reprep import Report
import numpy

def group_sign_hist(group, configuration, saccades):
    r = Report()

    left_percentage = []
    for sample, saccades_for_sample in iterate_over_samples(saccades):
        
        sign = saccades_for_sample['sign']
        left, = numpy.nonzero(sign==+1)
        
        perc = len(left) * 100.0 / len(sign)
        
        left_percentage.append(perc)

    N = len(left_percentage)
    with r.data_pylab('sign_hist') as pylab:
        R = range(N)
        pylab.bar(R, left_percentage)
        pylab.ylabel('percentage of left turns')
        pylab.axis([0,N,0,100])
    return r