from reprep import Report

from saccade_analysis.analysis201009.stats.utils import iterate_over_samples,\
    create_letter_sequence
from saccade_analysis.markov.first_order import first_order_analysis



def independence(group, configuration, saccades):
    
    # list, one per sample
    all_results = []
    
    for sample, saccades_for_sample in iterate_over_samples(saccades):
        letters = create_letter_sequence(saccades_for_sample)
        results = first_order_analysis(letters)
        
        length = saccades_for_sample[-1]['time_start'] - \
            saccades_for_sample[0]['time_start'] 
        density = len(saccades_for_sample) / length
        
        results.append(('length', length))
        results.append(('density', density))
        results.append(('sample', sample))
        
        all_results.append(results)
    
    return independence_table(all_results)

    
def independence_table(all_results):
        
    cols_desc = ['ID', 'Length (m)', 'N', 'n_L', 'n_R',
                     'n_RL', 'n_LL',
                     'n_RR', 'n_LR',
                     'p_L interval',
                     'best p_L',
                     'indep pvalue',
                     'why'
                     ]

        
    rows = []     
    for i, results in enumerate(all_results):
        results = dict(results)
        
        #rejected = {True:'*', False:''}[results['indep_rejected']]
        def pformat(seq):
            num = results['n_' + seq]
            prob = results['p_' + seq]
            return '%d (%.2f)' % (num, prob)

       
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

    report = Report()
    # Sort by length
    rows.sort(key=lambda x:-float(x[1]))
    report.table('independence', rows, cols=cols_desc)
    return report


        
def pvalue_format(v):
    if v < 0.01:
        return "%.3f**" % v 
    elif v < 0.05:
        return "%.3f*" % v
    else:
        return "%.3f" % v
