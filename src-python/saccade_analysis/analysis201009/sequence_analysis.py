from optparse import OptionParser
from saccade_analysis.analysis201009.datasets import load_datasets
from saccade_analysis import logger
from saccade_analysis.markov.first_order import first_order_analysis
import os

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
    
    report_fair = write_summary_fairness(datasets)
    report_indep = write_summary_independence(datasets)
    
    report = Report(children=[report_fair, report_indep])
    
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
        
        cols_desc = ['Sample ID', 'Length (min)', 'Num. saccades', 'saccades/s',
                     'p(L)', 'p value', 'rejected']
        rows = []     
        for i, results in enumerate(analysis):
            results = dict(results)
            p_L = "%3d%%" % (results['frequencies']['L'] * 100)
            rejected = {True:'*', False:''}[results['fair_rejected']]
            row = [i,
                   "%.1f" % (results['length'] / 60),
                   results['N'],
                   "%.2f" % results['density'],
                   p_L,
                   "%.3f" % results['fair_pvalue'],
                   rejected]

            rows.append(row)

        caption = "%s - %s" % (dataset['species'], dataset['experiment'])
        if 'description' in dataset:
            caption += ' - ' + dataset['description']

        report.table(id, rows, cols=cols_desc, caption=caption)
    
    return report
        
def write_summary_independence(datasets):
    report = Report('independence')
    
    for dataset in datasets:
        id = dataset['id']
        if not 'analysis' in dataset:
            logger.warning('Not creating report for %s' % id)
            continue
        
        analysis = dataset['analysis']
        
        cols_desc = ['N', 'n_L', 'n_R',
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
            p_L = "%3d%%" % (results['frequencies']['L'] * 100)
            
            rejected = {True:'*', False:''}[results['indep_rejected']]
            
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

            row = [
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

        report.table(id, rows, cols=cols_desc, caption=caption)
    
    return report
        
if __name__ == '__main__':
    main()
