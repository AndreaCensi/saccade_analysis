import os
import numpy
from reprep import Report

from optparse import OptionParser

from saccade_analysis.analysis201009.datasets import load_datasets
from saccade_analysis import logger 
from saccade_analysis.analysis201009.sequence_analysis import iterate_over_samples, \
    get_nice_dataset_description


            
def main():
    parser = OptionParser()
    parser.add_option("--data", help="Main data directory", default='.')
    parser.add_option("--output", help="Output directory", default='levy_analysis_output')
    (options, args) = parser.parse_args()

    datasets = load_datasets(options.data)
    
    for dataset in datasets:
        dataset['levy_analysis'] = []

        for sample_id, saccades_for_sample in \
            iterate_over_samples(dataset['saccades']):

            results = levy_analysis(sample_id, saccades_for_sample)

            dataset['levy_analysis'].append(results)

    
    report = Report('levy_analysis')
    report.add_child(create_report_levy(datasets))
    
    if not os.path.exists(options.output):
        os.makedirs(options.output)
    
    filename = os.path.join(options.output, 'levy_analysis.html')
    logger.info('Writing output to %s.' % filename)
    report.to_html(filename)
        
    
    
def get_good_data(x):
    x = numpy.array(x)
    good, = numpy.nonzero(numpy.isfinite(x))
    num_removed = len(x) - len(good)
    if num_removed > 0:
        #print 'Removed %s/%s invalid data.' % (num_removed, len(x))
        pass
    return x[good]

from numpy import log

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

def levy_analysis(sample_id, saccades):
    intervals = saccades['time_passed']
    a = 0.1
    mu, mu_lik = levy_estimate_mu(intervals, a) 
    
#    models = {}
    
    lambda_, lambda_lik = exponential_fit(intervals, a) 
#    
#    models['exponential'] = { 
#        'param_name' : 'lambda',
#        ''} 
#    
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
    results.append(('sample_id', sample_id))
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
    
def create_report_levy(datasets):
    report = Report('levy_analysis')
    
    for dataset in datasets:
        id = dataset['id']
        if not 'levy_analysis' in dataset:
            logger.warning('Not creating report for %s' % id)
            continue
        
        analysis = dataset['levy_analysis']
        
        cols_desc = ['ID', 'Num. saccades', 'a', 'mu',
                     'Levy log.lik.' , 'Akaike weight', 'lambda',
                      'Exponential log.lik.', 'Akaike weight', 'best model']
        rows = []     
        
        for i, results in enumerate(analysis): 
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

        caption = get_nice_dataset_description(dataset)
        
        # sort by length
        rows.sort(key=lambda x:-float(x[2]))
        report.table(id, rows, cols=cols_desc, caption=caption)
    
    return report
 
 
if __name__ == '__main__':
    main()
