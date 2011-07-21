import numpy as np
from collections import namedtuple
from scipy.stats import f
from contracts import contract

BinomialStats = namedtuple('BinomialStats',
                          'prob_left prob_right margin_left margin_right')


@contract(num='int,>=0,x',
          num_left='int,>=0,<=x',
          num_right='int,>=0,<=x',
          alpha='>0,<1')
def binomial_stats(num, num_left, num_right, alpha=0.01):
    assert num == num_left + num_right
    
    if num == 0:
        return np.NaN, np.NaN, [0, 1], [0, 1]
        
    margin_left = binofit(num_left, num, alpha)
    margin_right = binofit(num_right, num, alpha)
    
    prob_left = num_left * 1.0 / num
    prob_right = num_right * 1.0 / num

    return BinomialStats(prob_left=prob_left,
                         prob_right=prob_right,
                         margin_left=margin_left,
                         margin_right=margin_right)


@contract(x='int,>=0,x', n='int,>=0,>=x', alpha='>0,<1')
def binofit(x, n, alpha=0.01):
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


