from saccade_analysis.analysis201009.stats.utils import iterate_over_samples
from reprep import Report


description = """ 

This plot shows the joint distribution for ${name1} and ${name2}.

"""

# markersize
MS = 3
    
# note delay1 -> chop var2
# [x0 x1 x2 ]
# [ * x0 x1 ]
# [y0 y1 y2 ]

def get_delayed(x,delay1, y,delay2):
    assert delay1 >= 0
    assert delay2 >= 0
    assert len(x) == len(y)
    y = y[delay1:]
    x = x[delay2:]
    n = min(len(x), len(y))
    x = x[:n]
    y = y[:n]
    
    return x, y

def group_var_joint(group, configuration, saccades, var1, delay1, var2, delay2):
    
     
    r = Report()
    node_id = 'joint_%s%d_%s%d' % (var1.id, delay1, var2.id, delay2)
    with r.data_pylab(node_id) as pylab:
    
        colors = ['r','g','b','m','k'] * 50        
        for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
            x = saccades_for_sample[var1.field]
            y = saccades_for_sample[var2.field]
            x,y = get_delayed(x,delay1,y,delay2)
            
            color = colors.pop()            
            pylab.plot(x, y, "%s." % color, markersize=MS)
            
        pylab.axis([var1.interesting[0], var1.interesting[1],
                    var2.interesting[0], var2.interesting[1]]
                    )
         
        pylab.xlabel('%s (%s)' % (var1.name, var1.unit))
        pylab.ylabel('%s (%s)' % (var2.name, var2.unit))
        
    node_id += "_log"
    with r.data_pylab(node_id) as pylab:
    
        colors = ['r','g','b','m','k'] * 50        
        for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
            x = saccades_for_sample[var1.field]
            y = saccades_for_sample[var2.field]
            x,y = get_delayed(x,delay1,y,delay2)
            
            color = colors.pop()            
            pylab.loglog(x, y, "%s." % color, markersize=MS)
            
        pylab.axis([var1.interesting[0], var1.interesting[1],
                    var2.interesting[0], var2.interesting[1]]
                    )
         
        pylab.xlabel('%s (%s)' % (var1.name, var1.unit))
        pylab.ylabel('%s (%s)' % (var2.name, var2.unit))
        
    
    return r


def sample_var_joint(sample, expdata, configuration, saccades, 
                     var1, delay1, var2, delay2):
    x = saccades[var1.field]
    y = saccades[var2.field]
    x,y = get_delayed(x,delay1,y,delay2)

    r = Report()
    node_id = 'joint_%s%d_%s%d' % (var1.id, delay1, var2.id, delay2)
    with r.data_pylab(node_id) as pylab:
            
        pylab.plot(x, y, "b.", markersize=MS)
            
        pylab.axis([var1.interesting[0], var1.interesting[1],
                    var2.interesting[0], var2.interesting[1]]
                    )
         
        pylab.xlabel('%s (%s)' % (var1.name, var1.unit))
        pylab.ylabel('%s (%s)' % (var2.name, var2.unit))
        
    node_id += '_log'
    with r.data_pylab(node_id) as pylab:
            
        pylab.loglog(x, y, "b.", markersize=MS)
            
        pylab.axis([var1.interesting[0], var1.interesting[1],
                    var2.interesting[0], var2.interesting[1]]
                    )
         
        pylab.xlabel('%s (%s)' % (var1.name, var1.unit))
        pylab.ylabel('%s (%s)' % (var2.name, var2.unit))
    
    return r
