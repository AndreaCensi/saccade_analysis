import numpy as np
from contracts import contract

def compute_joint_statistics(stats, saccades_stats):
    for k in stats: 
        if k in saccades_stats:
            print('Warning, %r in both' % k)
    stats.update(**saccades_stats)
    C = stats['count']
    # Total number of saccades 
    N = saccades_stats['total']
    N_L = saccades_stats['num_left']
    N_R = saccades_stats['num_right']
    dt = 1.0 / 60 
    cells = stats['cells'] 
    ft = lambda: cells.zeros(fit_dtype) 
    stats['rate_saccade2'] = ft()
    stats['rate_saccade_left2'] = ft()
    stats['rate_saccade_right2'] = ft()
    stats['prob_left2'] = ft()
    stats['prob_right2'] = ft()
    
    alpha = 0.05

    for c in cells.iterate():
        k = c.k
        stats['rate_saccade2'][k] = fit_poisson(C[k], N[k], dt)
        stats['rate_saccade_left2'][k] = fit_poisson(C[k], N_L[k], dt)
        stats['rate_saccade_right2'][k] = fit_poisson(C[k], N_R[k], dt)
        stats['prob_left2'][k] = fit_binomial(N_L[k], N[k], alpha)
        stats['prob_right2'][k] = fit_binomial(N_R[k], N[k], alpha)
         
    return stats


fit_dtype = [('lower', float),
             ('upper', float),
             ('mean', float),
             ('confidence', float),
             ('skewed', float) # only used for binomial
             ]
 
@contract(samples_in_bin='>=0,int,x', num_events='>=0,int,<=x', sample_dt='>0')
def fit_poisson(samples_in_bin, num_events, sample_dt):
    ''' Returns 95% confidence intervals.

V. Guerriero, A. Iannace, S. Mazzoli, M. Parente, S. Vitale, M. Giorgioni
 (2009). "Quantifying uncertainties in multi-scale studies of fractured
 reservoir analogues: Implemented statistical analysis of scan line data 
from carbonate rocks". Journal of Structural Geology (Elsevier).
doi:10.1016/j.jsg.2009.04.016.
'''
    assert samples_in_bin >= num_events
    # length of interval
    L = float(samples_in_bin) * float(sample_dt)
    N = float(num_events)
    
    # maximum likelihood (also unbiased mean)
    if N <= 4: # TODO: simple formula below doesn't work for N<=4
        ml = N / L 
        upper = np.NaN
        lower = np.NaN
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


@contract(x='int,>=0,x', n='int,>=0,>=x', alpha='>0,<1')
def fit_binomial(x, n, alpha=0.01):
    ''' If n=0, the distribution is uniform in [0,1]. '''
    from scipy.stats import f
    if n == 0:
        ml = 0.5
    else:
        ml = float(x) / float(n)
    
    # Lower limits
    if x == 0:
        lb = 0
    else:    
        nu1 = 2 * x;
        nu2 = 2 * (n - x + 1)
        F = f.ppf(alpha / 2, nu1, nu2)
        lb = (nu1 * F) / (nu2 + nu1 * F)
        
    if x == n:
        ub = 1
    else:
        nu1 = 2 * (x + 1);
        nu2 = 2 * (n - x);
        F = f.ppf(1 - alpha / 2, nu1, nu2)
        ub = (nu1 * F) / (nu2 + nu1 * F)
         
    
    assert 0 <= lb <= ml <= ub <= 1
    res = np.ndarray((), dtype=fit_dtype)    
    res['mean'] = ml
    res['upper'] = ub
    res['lower'] = lb
    res['confidence'] = 0.01
    
    res['skewed'] = not (lb < 0.5 < ub)
    return res



