import numpy
from reprep import Report
 
    
    

def plot_sample_hist_group(group, configuration,  saccades):        
    r = Report()
    with r.data_pylab('sample_hist') as pylab:
        pylab.hist(saccades['time_passed'] )
    return r

def plot_sample_hist_sample(sample, exp_data, configuration,  saccades):        
    r = Report()
    with r.data_pylab('sample_hist') as pylab:
        pylab.hist(saccades['time_passed'] )
    return r
