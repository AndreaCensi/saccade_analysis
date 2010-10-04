'''

Utils for binomial functions.

Wrappers around scipy, with the same interface as Matlab.

'''


def binocdf(X, N, p):
    ''' Returns p-values for one-sided test '''
    ''' % p can be an array '''
    assert(X >= 0);
    assert(N > 0);
    assert(X <= N);
    assert(all(0 <= p));
    assert(all(p <= 1));
    assert(round(X) == X)
    assert(round(N) == N)
    
    #for i = 1:numel(p)
    #    cdf(i) = sum(binopdf(0:X, N, p(i)));
    #end 
