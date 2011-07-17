from reprep import  Report
import numpy as np
from  .plot_utils import plot_image

 
def report_models_choice(confid, stats):
    
    r = Report('%s_models' % confid)
    
    distance_edges = stats['distance_edges']
    axis_angle_edges = stats['axis_angle_edges']
    rate_saccade = stats['rate_saccade']
    rate_saccade_left = stats['rate_saccade_left']
    rate_saccade_right = stats['rate_saccade_right']
    
    rate_saccade_lr = rate_saccade_left - np.fliplr(rate_saccade_right)
    rate_saccade_sym = symmetrize(rate_saccade) 
    
    rate_saccade_sym_order = scale_score(rate_saccade_sym)

    f_rates = r.figure('Saccade rates', cols=3)
    
    s = ""
    s += ('Saccade rate:      %8f  %8f\n' % compute_interval(rate_saccade))
    s += ('Saccade rate (L):  %8f  %8f\n' % compute_interval(rate_saccade_left))
    s += ('Saccade rate (R):  %8f  %8f\n' % compute_interval(rate_saccade_right))
    
    r.text('rate_values', s)
    
    min_rate, max_rate = compute_interval(rate_saccade_left)
    scale_params = dict(max_value=max_rate, min_value=min_rate, skim=0.5)
    
    plot_image(r, f_rates, 'rate_sac',
               distance_edges, axis_angle_edges, rate_saccade,
               scale_params=dict(skim=1, max_color=[0, 0, 0.2],),
               caption="Saccading rate (saccades/s)")
    plot_image(r, f_rates, 'rate_sac_left',
               distance_edges, axis_angle_edges, rate_saccade_left,
               scale_params=scale_params,
               caption="Left saccading rate (saccades/s)")
    plot_image(r, f_rates, 'rate_sac_right',
               distance_edges, axis_angle_edges, rate_saccade_right,
               scale_params=scale_params,
               caption="Right saccading rate (saccades/s)")
    plot_image(r, f_rates, 'rate_sac_sym',
               distance_edges, axis_angle_edges, rate_saccade_sym,
               scale_params=dict(skim=1, max_color=[0, 0, 0.2],),
               caption="Saccading rate (saccades/s)") 
   
    plot_image(r, f_rates, 'rate_sac_sym_order',
               distance_edges, axis_angle_edges, rate_saccade_sym_order,
               scale_params={},
               caption="Order saccading rate (saccades/s)")
   
    plot_image(r, f_rates, 'rate_sac_lr',
               distance_edges, axis_angle_edges, rate_saccade_lr,
               scale_params={}, use_posneg=True,
               caption="Symmetrized saccading rate (saccades/s)")
   
   
    return r


def scale_score(x):
    y = x.copy()
    order = np.argsort(x.flat)
    # Black magic ;-) Probably the smartest thing I came up with today. 
    order_order = np.argsort(order)
    y.flat[:] = order_order.astype(y.dtype)
    return y



def symmetrize(M):
    return 0.5 * (M + np.fliplr(M))

def compute_interval(rate, perc=[1, 99]):
    limits = np.percentile(np.array(rate.flat), perc)
    min_rate = limits[0]
    max_rate = limits[1]
    return min_rate, max_rate
