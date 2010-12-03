import numpy
from numpy import log

from reprep import Report

from .utils import iterate_over_samples, attach_description
    

def levy_exp(groups, configuration, saccades): #@UnusedVariable
    
    all_results = []
    
    for sample, saccades_for_sample in iterate_over_samples(saccades): 
        results = levy_vs_exp_sample(sample, saccades_for_sample)
        all_results.append(results)
   
    return create_report(all_results)
   
def levy_vs_exp_sample(sample, saccades):
    intervals = saccades['time_passed']
    a = 0.1
    mu, mu_lik = levy_estimate_mu(intervals, a) 
    
    lambda_, lambda_lik = exponential_fit(intervals, a) 

    AIC = lambda loglik:-2 * loglik + 2 * 1 
    
    mu_aic = AIC(mu_lik)
    lambda_aic = AIC(lambda_lik)
    
    aic_min = min([mu_aic, lambda_aic])
    
    mu_delta = mu_aic - aic_min
    lambda_delta = lambda_aic - aic_min
    
    mu_w = numpy.exp(-mu_delta / 2)
    lambda_w = numpy.exp(-lambda_delta / 2)
    
    #print "before", mu_w, lambda_w
    # normalize
    s = mu_w + lambda_w
    lambda_w = lambda_w / s
    mu_w = mu_w / s 
    #print "after", mu_w, lambda_w
    
    results = []
    results.append(('sample_id', sample))
    results.append(('N', len(saccades)))
    results.append(('a', a))
    results.append(('mu', mu))
    results.append(('mu_lik', mu_lik))
    results.append(('mu_aic', mu_aic))
    results.append(('mu_w', mu_w))
    results.append(('lambda', lambda_))
    results.append(('lambda_lik', lambda_lik))
    results.append(('lambda_aic', lambda_aic))
    results.append(('lambda_w', lambda_w))
     
    return results
    
description = """

These tables compare the best fit of the interval distribution
according to Levy or Exponential distribution. "interval" is the interval
between two successive saccades.

The fields shown are:

``a``
  This is the lower bound on the distribution used (we consider only x>a). 
  It is fixed for all samples.
  
``mu``
  Estimated mu parameter for Levy.
  
``Levy log.lik.``
  Likelihood of the data with the estimate mu.
  
``lambda``
  Estimated parameter of the exponential distribution.
  
``Exp. log.lik``
  Likelihood of the data according to the estimated exponential distribution.
  
``Levy Akaike w.``, ``Exp. Akaike w.``
  The Akaike weights for the two models, normalized such that they sum to one.
  It seems always the case that one is 1 and the other is 0, which means
  that the data fits one or the other model always considerably better.
  Not what I expected, but I'm reasonably sure the math is correct.


"""

#TODO: compute bounds for mu
def create_report(all_results):  
    cols_desc = ['ID', 'Num. saccades', 'a', 'mu',
                 'Levy log.lik.' , 'Levy Akaike w.', 'lambda',
                  'Exp. log.lik.', 'Exp. Akaike w', 'best model']
    rows = []     
    
    for i, results in enumerate(all_results): 
        results = dict(results)
        
        if results['lambda_w'] > results['mu_w']:
            best = 'exponential'
        else:
            best = 'levy'
            
        row = [i,
              results['N'],
               results['a'],
               "%.2f" % results['mu'],
               "%.2f" % results['mu_lik'],
               "%.4f" % results['mu_w'],
               "%.2f" % results['lambda'] ,
               "%.2f" % results['lambda_lik'],
               "%.4f" % results['lambda_w'],
               best
               ]

        rows.append(row)
 
    # sort by length
    rows.sort(key=lambda x:-float(x[2]))
    
    r = Report()
    attach_description(r, description)
    r.table('levy_vs_exp', rows, cols=cols_desc)
    return r
 

def get_good_data(x):
    x = numpy.array(x)
    good, = numpy.nonzero(numpy.isfinite(x))
    num_removed = len(x) - len(good)
    if num_removed > 0:
        #print 'Removed %s/%s invalid data.' % (num_removed, len(x))
        pass
    return x[good]


def levy_estimate_mu(x, a):
    x = get_good_data(x)
    mu = 1 - 1 / (log(a) - log(x).mean())
    
    n = len(x)
    log_likelihood = n * log(mu - 1) + n * (mu - 1) * log(a) - mu * log(x).sum()
    
    return mu, log_likelihood
    
def exponential_fit(x, a):
    x = get_good_data(x)
    lambda_ = 1 / (x.mean() - a)
    n = len(x)
    log_likelihood = n * log(lambda_) + n * lambda_ * a - lambda_ * x.sum() 
    return lambda_ , log_likelihood
