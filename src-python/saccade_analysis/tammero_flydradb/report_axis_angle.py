from contracts import contract
from reprep import Report
import numpy as np
from ..markov import binomial_stats


def create_report_axis_angle(id, desc, saccades):
    r = Report('axis_angle')
        # 
        # axis_angle = saccades['axis_angle']
        # saccade_angle = saccades['saccade_angle']
                      
    stats = statistics_distance_axis_angle(saccades,
        num_distance_intervals=10,
        axis_angle_bin_interval=10,
        axis_angle_bin_size=10
    )
               
    f = r.figure(cols=1)
    
    for i, section in enumerate(stats['distance_sections']):
        distance_min = section['distance_min']
        distance_max = section['distance_max']
        prob_left = section['prob_left']
        prob_right = section['prob_right']
        margin_left = section['margin_left']
        margin_right = section['margin_right']
        bin_centers = section['bin_centers']
        num_saccades = section['num_saccades']
        n = len(bin_centers)
        
        with r.data_pylab('section%d' % i) as pylab:
            el = np.zeros((2, n))
            el[0, :] = +(margin_left[0, :] - prob_left)
            el[1, :] = -(margin_left[1, :] - prob_left)
            pylab.errorbar(bin_centers, prob_left, el, None, None,
                           ecolor='g', label='left', capsize=8, elinewidth=1)
            er = np.zeros((2, n))
            er[0, :] = +(margin_right[0, :] - prob_right)
            er[1, :] = -(margin_right[1, :] - prob_right)
            pylab.errorbar(bin_centers, prob_right, er, None, None,
                           ecolor='r', label='right', capsize=8, elinewidth=1)
    
            pylab.plot(bin_centers, prob_left, 'g-', label='left')
            pylab.plot(bin_centers, prob_right, 'r-', label='right')
            pylab.xlabel('axis angle (deg)')
            pylab.ylabel('probability of turning')
            pylab.title('Direction probability for distance in [%dcm,%dcm], %d saccades' % 
                        (distance_min * 100, distance_max * 100, num_saccades))
            pylab.plot([0, 0], [0, 1], 'k-')
            pylab.axis([-180, 180, 0, 1])
            pylab.legend()
        r.last().add_to(f)
            
    return r
    
    
@contract(x='array[N]', direction='array[N]',
          x_bin_centers='array[K]', x_bin_size='>0')
def compute_direction_statistics(x, x_bin_centers, x_bin_size, direction,
    alpha=0.01):
    
    K = len(x_bin_centers)
    t_prob_left = np.zeros(K)
    t_prob_right = np.zeros(K)
    t_margin_left = np.zeros((2, K))
    t_margin_right = np.zeros((2, K))
    for k in range(K):
        bin_center = x_bin_centers[k]
        inbin = np.logical_and(x <= bin_center + x_bin_size / 2,
                               bin_center - x_bin_size / 2 <= x)
        dirs = direction[inbin]
        
        num = len(dirs)
        num_left = (dirs > 0).sum()
        num_right = (dirs < 0).sum()
        
        prob_left, prob_right, margin_left, margin_right = \
            binomial_stats(num, num_left, num_right, alpha)
        
        t_prob_left[k] = prob_left
        t_prob_right[k] = prob_right
        t_margin_left[:, k] = margin_left
        t_margin_right[:, k] = margin_right
        
    return dict(bin_centers=x_bin_centers,
                prob_left=t_prob_left,
                prob_right=t_prob_right,
                margin_left=t_margin_left,
                margin_right=t_margin_right)
        
def statistics_distance_axis_angle(saccades,
        num_distance_intervals,
        axis_angle_bin_interval,
        axis_angle_bin_size
    ):
    distance = saccades['distance_from_wall']
    
    qs = np.linspace(0, 100, num_distance_intervals)
    # distance_edges = np.linspace(0, 1, distance_intervals)
    distance_edges = np.percentile(distance, qs.tolist())
    distance_num_sections = len(distance_edges) - 1 
    
    distance_sections = []
    for di in range(distance_num_sections):
        distance_min = distance_edges[di]
        distance_max = distance_edges[di + 1]
        select = np.logical_and(distance > distance_min,
                                distance < distance_max)
        
        relevant_saccades = saccades[select]
        
        bin_centers = range(-180, 180 + axis_angle_bin_interval,
                            axis_angle_bin_interval)
        statistics = compute_direction_statistics(
            x=relevant_saccades['axis_angle'],
            x_bin_centers=np.array(bin_centers),
            x_bin_size=axis_angle_bin_size,
            direction=relevant_saccades['sign'])
            
        statistics['num_saccades'] = len(relevant_saccades)
        statistics['distance_min'] = distance_min
        statistics['distance_max'] = distance_max
        distance_sections.append(statistics)
        
    return dict(distance_edges=distance_edges,
                distance_sections=distance_sections)
        
