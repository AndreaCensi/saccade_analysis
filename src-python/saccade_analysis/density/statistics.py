import numpy as np
from saccade_analysis.markov import fit_poisson, fit_dtype, fit_poisson_multiple, \
    fit_binomial

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
    stats['rate_saccade_L_est'] = ft()
    stats['rate_saccade_R_est'] = ft()
    stats['prob_left2'] = ft()
    stats['prob_right2'] = ft()
    
    alpha = 0.05

    for c in cells.iterate():
        k = c.k
        T = C[k] * dt
        
        stats['rate_saccade2'][k] = fit_poisson(N[k], T)
        stats['rate_saccade_left2'][k] = fit_poisson(N_L[k], T)
        stats['rate_saccade_right2'][k] = fit_poisson(N_R[k], T)
        
        count = np.array([N_L[k], N_R[k]])
        refractory = 0.1
        rates = fit_poisson_multiple(count=count, T=T, refractory=refractory)
        
        stats['rate_saccade_L_est'][k] = rates[0]
        stats['rate_saccade_R_est'][k] = rates[1]
        
        
        stats['prob_left2'][k] = fit_binomial(N_L[k], N[k], alpha)
        stats['prob_right2'][k] = fit_binomial(N_R[k], N[k], alpha)
         
    return stats




