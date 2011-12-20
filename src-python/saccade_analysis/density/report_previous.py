from . import plot_image, Report, np
from ..markov import binomial_stats


def report_stats(confid, stats, saccades_stats):
    r = Report(confid)
    
    cells = stats['cells']
    
    count = stats['count']
    
    f = r.figure('flight')
    
    dt = 1.0 / 60
    plot_image(r, f, 'transit', cells, count * dt,
               caption="Transit probability")
    plot_image(r, f, 'mean_speed', cells, stats['mean_speed'],
               caption="Mean speed (m/s)")
        
    f2 = r.figure('saccades', cols=2) 
  
    total = saccades_stats['total']
    num_left = saccades_stats['num_left']
    num_right = saccades_stats['num_right']
    prob_left = np.zeros(cells.shape)
    prob_right = np.zeros(cells.shape)
    skewed = np.zeros(cells.shape)
    for c in cells.iterate():
        pl, pr, ml, _ = (
            binomial_stats(total[c.k], num_left[c.k], num_right[c.k])
            )
        prob_left[c.k] = pl
        prob_right[c.k] = pr
        skewed[c.k] = 0 if (ml[0] < 0.5 and 0.5 < ml[1])  else 1
    
    #  plot_image(r, f2, 'total', distance_edges, axis_angle_edges, total)
    max_num = max(num_left.max(), num_right.max())
    min_num = min(num_left.min(), num_right.min())
    scale_params = dict(max_value=max_num, min_value=min_num)
    plot_image(r, f2, 'num_left', cells, num_left,
               scale_params=scale_params,
               caption="Raw count of left saccades")
    plot_image(r, f2, 'num_right', cells, num_right,
               scale_params=scale_params,
               caption="Raw count of right saccades")

    plot_image(r, f2, 'prob_left', cells, prob_left,
               scale_params=dict(min_value=0, max_value=1),
               caption="Prob. of saccading left (if saccading)")
    plot_image(r, f2, 'prob_right', cells, prob_right,
               scale_params=dict(min_value=0, max_value=1),
               caption="Prob. of saccading right (if saccading)")
    
    plot_image(r, f2, 'skewed', cells, skewed,
               scale_params=dict(max_color=[0, 1, 0]),
               caption="Significantly skewed (<0.01)")

    f3 = r.figure('stats', cols=3)

    dt = 1.0 / 60
    T = count * dt

    T[count == 0] = 1
    prob_sac = total * 1.0 / T
    prob_sac_left = num_left * 1.0 / T
    prob_sac_right = num_right * 1.0 / T
    
    limits = np.percentile(np.array(prob_sac_left.flat), [1, 99])
    min_rate = limits[0]
    max_rate = limits[1]
    print('Limits %r' % limits)
    scale_params = dict(max_value=max_rate, min_value=min_rate, skim=0.5)
    
    plot_image(r, f3, 'rate_sac',
               cells, prob_sac,
               scale_params=dict(skim=1, max_color=[0, 0, 0.2],),
               caption="Saccading rate (saccades/s)")
    plot_image(r, f3, 'rate_sac_left',
               cells, prob_sac_left,
               scale_params=scale_params,
               caption="Left saccading rate (saccades/s)")
    plot_image(r, f3, 'rate_sac_right',
               cells, prob_sac_right,
               scale_params=scale_params,
               caption="Right saccading rate (saccades/s)")
    
    baseline_rate = np.percentile(np.array(prob_sac[-4:, :].flat), 65)
    prob_sac2 = np.array(prob_sac)
    prob_sac2[prob_sac < baseline_rate] = np.NaN
    
    #print('baseline_rate is %g' % baseline_rate)
#    plot_image(r, f3, 'prob_sac2',
#               distance_edges, axis_angle_edges, prob_sac2,
#               caption="Used to compute baseline saccade rate")
    
    baseline = np.mean([np.mean(prob_sac_left[-4:, :]),
                        np.mean(prob_sac_right[-4:, :])])
    print('baseline is %g' % baseline)
    
    baseline_both = np.mean(prob_sac[-4:, :])
    print('baseline_both is %g' % baseline_both)
    
    sac_norm = prob_sac - baseline_both
    sac_left_norm = prob_sac_left - baseline 
    sac_right_norm = prob_sac_right - baseline 
    skim = 1
    plot_image(r, f3, 'sac_norm',
               cells, sac_norm,
               colors='posneg',
               scale_params=dict(skim=skim),
               caption='Saccade rate over baseline')
    
    #max_value = max(sac_left_norm.max(), sac_right_norm.max())
    plot_image(r, f3, 'sac_left_norm',
               cells, sac_left_norm,
               colors='posneg',
               scale_params=dict(max_value=max_rate - baseline),
               caption='Left saccade rate over baseline')
    
    plot_image(r, f3, 'sac_right_norm',
               cells, sac_right_norm,
               colors='posneg',
               scale_params=dict(max_value=max_rate - baseline),
               caption='Right saccade rate over baseline')
    r.text('comment', 'The last three figures display in red '
           'the areas where the fly saccades more than the baseline.')
    
    return r
   
