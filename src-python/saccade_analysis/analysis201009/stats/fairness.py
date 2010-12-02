from reprep import Report

from saccade_analysis.markov.first_order import first_order_analysis

from .utils import iterate_over_samples, \
    create_letter_sequence, attach_description
    
   


def fairness(group, configuration, saccades):
    
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
    
    return fairness_table(all_results)

description = """
This table reports the statistical tests used
to discard the null hypothesis that the turns are balanced left/right,
that is, binomial with p = 0.5. ``p_L`` is the probability 
of left turns. The p-value is a two-sides binomial test. 
""" 
    
def fairness_table(all_results):
        
    cols_desc = [' ID', 'Length (min)', 'Num. saccades', 'saccades/s',
                 'p_L', 'p value', 'rejected']
    rows = []     
    for i, results in enumerate(all_results):
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

    # caption = get_nice_dataset_description(dataset)
    print rows
    
    # sort by length
    rows.sort(key=lambda x:-float(x[1]))
    
    r = Report()
    attach_description(r, description)
    r.table('fairness', rows, cols=cols_desc)
    return r


