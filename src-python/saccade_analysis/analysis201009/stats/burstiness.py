from reprep import Report


def group_var_joint(group, configuration, saccades,
                    var1, delay1, var2, delay2):    
    
    interval = saccades[:]['time_passed']

    r = Report()
    attach_description(r, description.format(var1=var1, var2=var2,
                            var1delay=var1delay, var2delay=var2delay))
    
    node_id = 'joint_%s%d_%s%d' % (var1.id, delay1, var2.id, delay2)
    with r.data_pylab(node_id) as pylab:
    
        colors = ['r', 'g', 'b', 'm', 'k'] * 50        
        for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
            x = saccades_for_sample[var1.field]
            y = saccades_for_sample[var2.field]
            x, y = get_delayed(x, delay1, y, delay2)
            
            color = colors.pop()            
            pylab.plot(x, y, "%s." % color, markersize=MS)
            
        pylab.axis([var1.interesting[0], var1.interesting[1],
                    var2.interesting[0], var2.interesting[1]]
                    )
         
        pylab.xlabel('%s (%s)' % (var1.name, var1.unit))
        pylab.ylabel('%s (%s)' % (var2.name, var2.unit))
        
    node_id += "_log"
    with r.data_pylab(node_id) as pylab:
    
        colors = ['r', 'g', 'b', 'm', 'k'] * 50        
        for sample, saccades_for_sample in iterate_over_samples(saccades): #@UnusedVariable
            x = saccades_for_sample[var1.field]
            y = saccades_for_sample[var2.field]
            x, y = get_delayed(x, delay1, y, delay2)
            
            color = colors.pop()            
            pylab.loglog(x, y, "%s." % color, markersize=MS)
            
        pylab.axis([var1.interesting[0], var1.interesting[1],
                    var2.interesting[0], var2.interesting[1]]
                    )
         
        pylab.xlabel('%s (%s)' % (var1.name, var1.unit))
        pylab.ylabel('%s (%s)' % (var2.name, var2.unit))
        
    
    return r

