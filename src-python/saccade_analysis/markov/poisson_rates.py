from contracts import contract
import numpy as np

@contract(T='float,>0', refractory='>=0', count='array[K](int32),K>0',
          returns='array[K](>=0)')
def estimate_rates_dep(T, refractory, count):
    ''' 
        Estimates the rates of a group of poisson processes
        that inhibit each other with a fixed refractory rate,
        given only the counting statistics.
        
        :param T: the total observation time.
        :param refractory: the refractory period after each event.
        :param count: an array with the number of events observed for each process.
    '''
    
    # First estimate total rate
    total_count = count.sum() 
    n = len(count)
    res = np.zeros(n)
    for i in range(n):
        res[i] = float(count[i]) / (T - refractory * total_count) 
    return res
