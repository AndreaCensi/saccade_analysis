from optparse import OptionParser
from saccade_analysis.analysis201009.datasets import load_datasets
from saccade_analysis import logger
from saccade_analysis.markov.first_order import first_order_analysis
import os
import numpy

def  create_letter_sequence(saccades):
    letters = []
    for saccade in saccades:
        if saccade['sign'] == 1:
            letters.append('L')
        elif saccade['sign'] == -1:
            letters.append('R')
        else: 
            assert False
    return "".join(letters)
            
def main():
    parser = OptionParser()
    parser.add_option("--data", help="Main data directory", default='.')
    parser.add_option("--output", help="Output directory", default='sequence_analysis_output')
    (options, args) = parser.parse_args()


    datasets = load_datasets(options.data)
    
    for dataset in datasets:
    
        id = dataset['id']
        saccades = dataset['saccades']
        
        num_samples = 1 + saccades['sample_num'].max()
        
        dataset['analysis'] = []
        for i in range(num_samples):
            saccades_for_sample = saccades[saccades['sample_num'] == i]
            
            print 'dataset %15s, sample %4d: %5d saccades' % (id, i, len(saccades_for_sample))
    
            letters = create_letter_sequence(saccades_for_sample)
            results = first_order_analysis(letters)
            
            length = saccades_for_sample[-1]['time_start'] - \
                saccades_for_sample[0]['time_start'] 
            density = len(saccades_for_sample) / length
            
            results.append(('length', length))
            results.append(('density', density))
            
            dataset['analysis'].append(results)
        
        #break
    
    children = []
    children.append(write_summary_fairness(datasets))
    children.append(write_summary_independence(datasets))
    children.append(
        create_report_figure(datasets, 'sign_correlation',
                             caption='Sign correlation',
                             generic_figure_function=sample_sign_xcorr))
    
    
    report = Report('saccade_report', children=children)
    
    if not os.path.exists(options.output):
        os.makedirs(options.output)
    
    filename = os.path.join(options.output, 'summary.html')
    logger.info('Writing output to %s.' % filename)
    report.to_html(filename)
        
    
    
from reprep import Report

def write_summary_fairness(datasets):
    report = Report('fairness')
    
    for dataset in datasets:
        id = dataset['id']
        if not 'analysis' in dataset:
            logger.warning('Not creating report for %s' % id)
            continue
        
        analysis = dataset['analysis']
        
        cols_desc = [' ID', 'Length (m)', 'Num. saccades', 'saccades/s',
                     'p_L', 'p value', 'rejected']
        rows = []     
        for i, results in enumerate(analysis):
            results = dict(results)
            
            rejected = {True:'*', False:''}[results['fair_rejected']]
            row = [i,
                   "%.1f" % (results['length'] / 60),
                   results['N'],
                   "%.2f" % results['density'],
                   "%.2f" % results['p_L'],
                   "%.3f" % results['fair_pvalue'],
                   rejected]

            rows.append(row)

        caption = get_nice_dataset_description(dataset)
        
        # sort by length
        rows.sort(key=lambda x:-float(x[1]))
        report.table(id, rows, cols=cols_desc, caption=caption)
    
    return report

def get_nice_dataset_description(dataset):
    desc = "%s - %s" % (dataset['species'], dataset['experiment'])
    if 'description' in dataset:
        desc += ' - ' + dataset['description']
    return desc
    

def write_summary_independence(datasets):
    report = Report('independence')
    
    for dataset in datasets:
        id = dataset['id']
        if not 'analysis' in dataset:
            logger.warning('Not creating report for %s' % id)
            continue
        
        analysis = dataset['analysis']
        
        cols_desc = ['ID', 'Length (m)', 'N', 'n_L', 'n_R',
                     'n_RL', 'n_LL',
                     'n_RR', 'n_LR',
                     'p_L interval',
                     'best p_L',
                     'indep pvalue',
                     'why'
                     ]

            
        rows = []     
        for i, results in enumerate(analysis):
            results = dict(results)
            
            #rejected = {True:'*', False:''}[results['indep_rejected']]
            
            def pformat(seq):
                num = results['n_' + seq]
                prob = results['p_' + seq]
                return '%d (%.2f)' % (num, prob)
            
            def pvalue_format(v):
                if v < 0.01:
                    return "%.3f**" % v 
                elif v < 0.05:
                    return "%.3f*" % v
                else:
                    return "%.3f" % v

            row = [i,
                   "%.1f" % (results['length'] / 60),
                   results['N'],
                   results['n_L'],
                   results['n_R'],
                   pformat('RL'),
                   pformat('LL'),
                   pformat('RR'),
                   pformat('LR'),
                   "[%.2f, %.2f]" % (results['p_L_lb'], results['p_L_ub']),
                   "%.2f" % results['best_p_L'],
                   pvalue_format(results['indep_pvalue']),
                   results['why']
                ]

            rows.append(row)

        caption = "%s - %s" % (dataset['species'], dataset['experiment'])
        if 'description' in dataset:
            caption += ' - ' + dataset['description']

        # Sort by length
        rows.sort(key=lambda x:-float(x[1]))
        report.table(id, rows, cols=cols_desc, caption=caption)
    
    return report
  
def sample_sign_xcorr(dataset_saccades, pylab):
    for sample, saccades_for_sample in iterate_over_samples(dataset_saccades):
        sign = saccades_for_sample['sign']
        sign = sign.astype('float32')
        xc, lags = xcorr(sign, maxlag=10)
        pylab.plot(lags, xc, 'x-')
    pylab.axis([-10, 10, -0.5, 1.1])
    pylab.ylabel('cross-correlation')
    pylab.xlabel('interval in sequence')
    
def create_report_figure(datasets, node_id, caption, generic_figure_function, cols=3):
    node = Report(node_id)
    f = node.figure(shape=(3, 3))
    for dataset in datasets:
        id = dataset['id']
        saccades = dataset['saccades']
        
        with node.data_pylab(id) as pylab:
            generic_figure_function(saccades, pylab)
        
        f.sub(id, caption=get_nice_dataset_description(dataset))
            
    return node

def iterate_over_samples(saccades):
    ''' yields  sample_id, saccades_for_sample '''
    num_samples = 1 + saccades['sample_num'].max()
    for i in range(num_samples):
        saccades_for_sample = saccades[saccades['sample_num'] == i]
        if len(saccades_for_sample) == 0:
            continue
        id = saccades_for_sample[0]['sample']
        yield id, saccades_for_sample
     

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

if __name__ == '__main__':
    main()
