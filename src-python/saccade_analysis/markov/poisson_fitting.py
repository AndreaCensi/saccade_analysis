from . import contract, np, fit_dtype

@contract(num_events='>=0,int', interval='float,>0')
def fit_poisson(num_events, interval):
    ''' Returns 95% confidence intervals.

V. Guerriero, A. Iannace, S. Mazzoli, M. Parente, S. Vitale, M. Giorgioni
 (2009). "Quantifying uncertainties in multi-scale studies of fractured
 reservoir analogues: Implemented statistical analysis of scan line data 
from carbonate rocks". Journal of Structural Geology (Elsevier).
doi:10.1016/j.jsg.2009.04.016.
'''
    # length of interval
    L = interval
    N = float(num_events)
    
    # maximum likelihood (also unbiased mean)
    if N <= 1:
        ml = N / L 
        upper = np.NaN
        lower = 0
    elif N <= 4: # TODO: simple formula below doesn't work for N<=4
        ml = N / L 
#        upper = np.NaN
        # TODO: double check this
        upper = N / L * (1 + 1.96 / np.sqrt(N - 1))
        lower = 0
    else:
        ml = N / L 
        upper = N / L * (1 + 1.96 / np.sqrt(N - 1))
        lower = N / L * (1 - 1.96 / np.sqrt(N - 1))
        
        assert 0 <= lower < ml < upper

    
    res = np.ndarray((), dtype=fit_dtype)    
    res['mean'] = ml
    res['upper'] = upper
    res['lower'] = lower
    res['confidence'] = 0.05
    res['skewed'] = np.NaN
    return res


@contract(T='float,>0', refractory='>=0', count='array[K](int32),K>0')
def fit_poisson_multiple(count, T, refractory):
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
    actual_interval = T - refractory * total_count
    
    n = len(count)
    res = np.ndarray(n, dtype=fit_dtype) 
    for i in range(n):
        #res[i] = float(count[i]) / (T - refractory * total_count)
        res[i] = fit_poisson(num_events=count[i], interval=actual_interval)
    return res
