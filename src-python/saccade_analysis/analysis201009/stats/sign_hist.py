from saccade_analysis.analysis201009.stats.utils import iterate_over_samples, \
    attach_description
from reprep import Report
import numpy

description = """This figure shows the proportion of left (blue) vs right (pink) saccades. """

def group_sign_hist(group, configuration, saccades):
    r = Report()
    attach_description(r, description)

    left_percentage = []
    for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
        
        sign = saccades_for_sample['sign']
        left, = numpy.nonzero(sign == +1)
        
        perc = len(left) * 100.0 / len(sign)
        
        left_percentage.append(perc)

    left_percentage = numpy.array(left_percentage) 
    N = len(left_percentage)
    with r.data_pylab('sign_hist') as pylab:
        R = range(N)
         
        right_percentage = -left_percentage + 100
        
        pylab.bar(left=R, height=left_percentage, color='b')
        pylab.bar(left=R, height=right_percentage, bottom=left_percentage, 
                  color='#faacb6')
        
        pylab.plot([0],[0])
        pylab.ylabel('percentage of left turns')
        pylab.xlabel('sample')
        pylab.axis([0, N, 0, 100])
        
        
    return r
