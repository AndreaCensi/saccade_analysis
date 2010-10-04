import numpy
import scipy.stats
from scipy.stats.morestats import binom_test
from numpy.lib.function_base import linspace

def first_order_analysis(s, significance=0.01):
    symbols = ['L', 'R']

    results = []
    results.append(('significance', significance))

    N = len(s)
    
    if N == 0:
        raise ValueError('Empty string')
    
    for x in s:
        if not x in symbols:
            raise ValueError('Unknown character "%s" in string.' % x)
    
    count = {}
    frequencies = {}
    for symbol in symbols:
        count[symbol] = s.count(symbol)
        frequencies[symbol] = zdiv(count[symbol], N) 
    results.append(('N', N))
    results.append(('count', count))
    results.append(('frequencies', frequencies))
    
    fair_pvalue = scipy.stats.binom_test(count['L'], N, 0.5)
    fair_rejected = fair_pvalue < significance
    
    results.append(('fair_pvalue', fair_pvalue))
    results.append(('fair_rejected', fair_rejected))
    
    # rejecting independence, without knowing p_L

    n_L = count_overlapping(s, 'L')
    n_R = count_overlapping(s, 'R')
    n_RL = count_overlapping(s, 'RL')
    n_LL = count_overlapping(s, 'LL')
    n_RR = count_overlapping(s, 'RR')
    n_LR = count_overlapping(s, 'LR')
    
    # Get a confidence interval
    p_L_lb, p_L_ub = binofit(n_L, N, significance) 

    # Run the test for the lower bound
    
    ps = linspace(p_L_lb, p_L_ub, 50)
    pvalues = []
    whys = []
    
    for p in ps:
        RL_pvalue_p = binom_test(n_RL, n_R, p)
        LL_pvalue_p = binom_test(n_LL, n_L, p)
        pvalue_p = min([ RL_pvalue_p, LL_pvalue_p ])
        correlation = '-' if RL_pvalue_p < LL_pvalue_p else '+'
        whys.append(correlation)
        pvalues.append(pvalue_p)
    
    best = numpy.argmax(pvalues)
    best_p = ps[best] 
    indep_pvalue = pvalues[best]
    indep_rejected = indep_pvalue < significance
    why = whys[best] if indep_rejected else ''
        
    results.extend([
        ('n_L', n_L),
        ('n_R', n_R),
        ('n_RL', n_RL),
        ('p_RL', zdiv(n_RL, n_R)),
        ('n_LL', n_LL),
        ('p_LL', zdiv(n_LL, n_L)),
        ('n_RR', n_RR),
        ('p_RR', zdiv(n_RR, n_R)),
        ('n_LR', n_LR),
        ('p_LR', zdiv(n_LR, n_L)),
        ('p_L_lb', p_L_lb),
        ('p_L_ub', p_L_ub),
#        ('RL_pvalue_lb', RL_pvalue_lb),
#        ('LL_pvalue_lb', LL_pvalue_lb),
#        ('pvalue_lb', pvalue_lb),
#        ('RL_pvalue_ub', RL_pvalue_ub),
#        ('LL_pvalue_ub', LL_pvalue_ub),
#        ('pvalue_ub', pvalue_ub),
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

from scipy.stats import f

def binofit(x, n, alpha):
    ''' Copied from Matlab. '''
    # Lower limits
    
    if x == 0:
        lb = 0
    else:    
        nu1 = 2 * x;
        nu2 = 2 * (n - x + 1);
        F = f.ppf(alpha / 2, nu1, nu2);
        lb = (nu1 * F) / (nu2 + nu1 * F);
        
    if x == n:
        ub = 1
    else:
        nu1 = 2 * (x + 1);
        nu2 = 2 * (n - x);
        F = f.ppf(1 - alpha / 2, nu1, nu2);
        ub = (nu1 * F) / (nu2 + nu1 * F);
        
    
    return (lb, ub)




