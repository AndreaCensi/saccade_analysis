from reprep import Report
from saccade_analysis.analysis201009.stats.utils import iterate_over_samples , \
    attach_description
import numpy


description = """ 

This plot shows the percentiles for ${var.name}, for each sample.
The percentiles shown are ${percentiles}.

The samples are ordered left-to-right by increasing median value.
"""
 
    
def group_var_percentiles(group, configuration, saccades, variable):
     
    
    percentiles = [1, 5, 25, 50, 75, 95, 99]
    colors = [ 'k', 'r', 'b', 'g', 'b', 'r', 'k']
    vcolors = ['k', 'r', 'b', 'b', 'r', 'k']
    scores = {}
    for p in percentiles:
        scores[p] = []
        
    scores_for_sample = []
    
    for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
        x = saccades_for_sample[variable.field]
        sc = numpy.percentile(x, percentiles)
        #print sample, sc
        scores_for_sample.append(sc)
        for i, p in enumerate(percentiles): 
            scores[p].append(sc[i]) 
    
    for p in percentiles:
        scores[p] = numpy.array(scores[p])
    
    order = numpy.argsort(scores[50])
    
    
    r = Report()
    attach_description(r, description.format(var=variable, percentiles=",".join(percentiles)))
    with r.data_pylab('%s_percentiles' % variable.id) as pylab:
        #print percentiles
        # plot horizontal 
        for i, p in enumerate(percentiles):
            #print p, scores[p][order]
            pylab.plot(scores[p][order], '%sx--' % colors[i])
            
        # plot vertical for each sample
        for x, index in enumerate(order):            
            sample_scores = scores_for_sample[index]
            
            for i in range(0, len(sample_scores) - 1):
                y0 = sample_scores[i]
                y1 = sample_scores[i + 1]
                col = "%s-" % vcolors[i]
                #print x, y0, y1
                pylab.plot([x, x], [y0, y1], col)
        
        pylab.axis([-0.5, len(order) - 0.5, variable.interesting[0],
                    variable.interesting[1]])
         
        pylab.ylabel('%s (%s)' % (variable.name, variable.unit))
        
        pylab.xlabel('sample')
        
    
    return r
