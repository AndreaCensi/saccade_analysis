from reprep import Report
from  .utils import iterate_over_samples, attach_description

description = """
This figure displays the average number of saccades per second
over the whole sample. 
"""  

def group_saccade_density(group, configuration, saccades):
    r = Report()
    attach_description(r, description)
    stats = []
    for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
        T = saccades_for_sample['time_start']
        length = T[-1] - T[0]
        stat = len(saccades_for_sample) / length
        stats.append(stat)

    N = len(stats)
    with r.data_pylab('saccade_density') as pylab:
        R = range(N)
        pylab.bar(R, stats)
        pylab.ylabel('saccade density (saccades/s)')
        pylab.axis([0, N, 0, 3.0])
    return r

description = """
This figure displays the total number of detected saccades.
(note that this is an absolute count, and it is not normalized
by the sample length.) 
"""  

def group_saccade_count(group, configuration, saccades):
    r = Report()
    attach_description(r, description)
    
    stats = []
    for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
        stats.append(len(saccades_for_sample))

    N = len(stats)
    with r.data_pylab('saccade_count') as pylab:
        R = range(N)
        pylab.bar(R, stats)
        pylab.ylabel('number of saccades')
        
        pylab.axis([0, N, 0, 4000])
    return r
