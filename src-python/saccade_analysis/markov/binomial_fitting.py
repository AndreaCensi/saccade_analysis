from . import contract, fit_dtype, np

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
