import numpy

def xcorr(a, b=None, maxlag=None):
    if b is None:
        b = a
    a = numpy.array(a)
    b = numpy.array(b)
    
    if maxlag is None:
        maxlag = len(a) / 2
        
    # normalize a, b
    a = a - a.mean()
    b = b - b.mean()
    
    na = numpy.linalg.norm(a)
    nb = numpy.linalg.norm(b)
    if na > 0:
        a = a / na
    if nb > 0:
        b = b / nb
        
    lags = range(-maxlag, maxlag + 1)
    results = numpy.zeros(shape=(len(lags),))
    for i, lag in enumerate(lags):
        if lag < 0:
            lag = -lag
            ta, tb = b, a
        else:
            ta, tb = a, b
        part_of_a = ta[lag:len(tb)]
        part_of_b = tb[0:len(part_of_a)]
        assert len(part_of_a) == len(part_of_b)
        results[i] = (part_of_a * part_of_b).sum()

    return results, lags