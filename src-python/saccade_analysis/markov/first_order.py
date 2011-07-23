import numpy as np
import scipy.stats
from scipy.stats.morestats import binom_test
from scipy.stats import binom
from . import binofit


def first_order_analysis(s, significance=0.05):
    symbols = ['L', 'R']

    results = []

    N = len(s)
    
    if N == 0:
        raise ValueError('Empty string')
    
    for x in s:
        if not x in symbols:
            raise ValueError('Unknown character %r in string.' % x)
     
    n_L = count_overlapping(s, 'L')
    n_R = count_overlapping(s, 'R')
    n_RL = count_overlapping(s, 'RL')
    n_LL = count_overlapping(s, 'LL')
    n_RR = count_overlapping(s, 'RR')
    n_LR = count_overlapping(s, 'LR')
    
    fair_pvalue = scipy.stats.binom_test(n_L, N, 0.5)
    fair_rejected = fair_pvalue < significance
    
    # Get a confidence interval
    p_L_lb, p_L_ub = binofit(n_L, N, significance) 

    # Run the test for the lower bound
    
    ps = np.linspace(p_L_lb, p_L_ub, 50)
    pvalues = []
    whys = []
    
    for p in ps:
        # we check if any of the two is significant
        RL_pvalue_p = binom_test(n_RL, n_R, p)
        LL_pvalue_p = binom_test(n_LL, n_L, p)
        pvalue_p = min([ RL_pvalue_p, LL_pvalue_p ])
        
        # More detailed test (somewhat redudand)
        # We want to see if we are significantly POS or NEG correlated.
        LL_significantly_positive = binom.cdf(n_LL, n_L, p) > 1 - significance
        LL_significantly_negative = binom.cdf(n_LL, n_L, p) < significance
        # note: there was a bug in Matlab
        RL_significantly_negative = binom.cdf(n_RL, n_R, p) > 1 - significance
        RL_significantly_positive = binom.cdf(n_RL, n_R, p) < significance
        
        significantly_negative = LL_significantly_negative or RL_significantly_negative
        significantly_positive = LL_significantly_positive or RL_significantly_positive
        
        if  significantly_negative:
            correlation = '-'
        elif significantly_positive:
            correlation = '+'
        else:
            correlation = ''
        
        whys.append(correlation)
        pvalues.append(pvalue_p)
    
    best = np.argmax(pvalues)
    best_p = ps[best] 
    indep_pvalue = pvalues[best]
    indep_rejected = indep_pvalue < significance
    why = whys[best] if indep_rejected else ''
        
    
    results.extend([
        ('significance', significance),
        ('N', N),
        ('n_L', n_L),
        ('p_L', zdiv(n_L, N)),
        ('n_R', n_R),
        ('p_R', zdiv(n_R, N)),
        ('n_RL', n_RL),
        ('p_RL', zdiv(n_RL, n_R)),
        ('n_LL', n_LL),
        ('p_LL', zdiv(n_LL, n_L)),
        ('n_RR', n_RR),
        ('p_RR', zdiv(n_RR, n_R)),
        ('n_LR', n_LR),
        ('p_LR', zdiv(n_LR, n_L)),
        ('fair_pvalue', fair_pvalue),
        ('fair_rejected', fair_rejected),
        ('p_L_lb', p_L_lb),
        ('p_L_ub', p_L_ub),
        ('indep_pvalue', indep_pvalue),
        ('indep_rejected', indep_rejected),
        ('why', why),
        ('best_p_L', best_p),
    ]) 
    
    return results

def zdiv(a, b):
    ''' Returns (float) a / (float) b, with 0/0 = 0. 
        a/0, with a != 0, raises an exception. '''
    if b == 0:
        assert a == 0
        return 0
    else:
        return float(a) / float(b)
        

def count_overlapping(s, sub):
    ''' Counts the number of **overlapping** occurrencies of sub
        in the string s. Note that the method str.count does not 
        consider overlapping occurencies. For example: ::
        
             'LLL'.count('LL') == 1
             
        while
        
             count_overlapping('LLL','LL') == 2
    '''
    n = len(s)
    m = len(sub)
    
    if m == 0:
        raise ValueError('Cannot look for empty substring.')
    
    count = 0
    for i in range(0, n - m + 1):
        portion = s[i: i + m]
        if portion == sub:
            count += 1
    return count


