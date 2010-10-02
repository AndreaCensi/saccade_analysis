import numpy

def first_order_analysis(s):
    results = []
    symbols = ['L', 'R']
    #symbols = list(numpy.unique(s))
    N = len(s)
    
    if N == 0:
        raise ValueError('Empty string')
    
    for x in s:
        if not x in symbols:
            raise ValueError('Unknown character "%s" in string.' % x)
    
    frequencies = {}
    for symbol in symbols:
        frequencies[symbol] = zdiv(s.count(symbol), N) 
    
    results.append(('frequencies', frequencies))

    return results



def zdiv(a, b):
    ''' Returns (float) a / (float) b, with 0/0 = 0. 
        a/0, with a != 0, raises an exception. '''
    if b == 0:
        assert a == 0
        return 0
    else:
        return float(a) / float(b)
        




