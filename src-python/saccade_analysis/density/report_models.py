from reprep import  Report
import numpy as np
from .plot_utils import plot_image
from saccade_analysis.density.plot_utils import plot_arena
from saccade_analysis.density.xy_cells import XYCells

COL_LEFT = 'r'
COL_LEFT_RGB = [1, 0, 0]

COL_RIGHT = 'b'
COL_RIGHT_RGB = [0, 0, 1]

 
def report_models_choice(confid, stats):
    r = Report('%s_models' % confid)
    
    cells = stats['cells']

    rate_saccade_left_order = scale_score_norm(stats['rate_saccade_left2']['mean'])
    rate_saccade_right_order = scale_score_norm(stats['rate_saccade_right2']['mean'])
               
    M = 0.5 * (rate_saccade_left_order + 1 - rate_saccade_right_order)
    c = 0.5 # TODO
    phi = 2 * (M - c)


    f_rates = r.figure('Saccade rates', cols=3)
    
    max_rate = np.nanmax([np.nanmax(stats['rate_saccade_left2']['mean']),
                          np.nanmax(stats['rate_saccade_right2']['mean'])])
    
    plot_image(r, f_rates, 'rate_sac_left',
               cells, stats['rate_saccade_left2']['mean'],
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_LEFT_RGB),
               caption="Left saccading rate (saccades/s)")
    
    plot_image(r, f_rates, 'rate_sac_right',
               cells, stats['rate_saccade_right2']['mean'],
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_RIGHT_RGB),
               caption="Right saccading rate (saccades/s)") 


    plot_image(r, f_rates, 'rate_sac',
               cells, stats['rate_saccade2']['mean'],
               scale_params=dict(max_color=[0, 0, 0.2], min_value=0),
               caption="Saccading rate (saccades/s)")

    order_params = dict(max_color=[0, 1, 0], min_color=[1, 0, 1])
    
    plot_image(r, f_rates, 'rate_saccade_left_order',
               cells, rate_saccade_left_order,
               scale_params=order_params,
               caption="order[ left saccade rate]")
   
    plot_image(r, f_rates, 'rate_saccade_right_order',
               cells, rate_saccade_right_order,
               scale_params=order_params,
               caption="order[ right saccade rate]")
   

    plot_image(r, f_rates, 'phi', cells, phi,
               scale_params={}, use_posneg=True,
                caption="""Normalized reduced stimulus. 
This is the 1D quantity that best explains the saccading rates,
assuming that there is a left-right symmetry. """)
    
    f_arena = r.figure('Arena view', cols=3)
    
    ncells = 200
    xy_cells = XYCells(radius=1, ncells=ncells, da_cells=cells)

    da2xy = lambda F:  xy_cells.from_da_field(F) 
    
    if True:
        plot_arena(f_arena, f_arena, 'x', xy_cells.x,
                   use_posneg=True, caption="x")
        plot_arena(f_arena, f_arena, 'y', xy_cells.y,
                   use_posneg=True, caption="y")
        plot_arena(f_arena, f_arena, 'd', xy_cells.d,
                   use_posneg=True, caption="d")
        plot_arena(f_arena, f_arena, 'axis_angle', xy_cells.axis_angle_deg,
                   use_posneg=True, caption="axis_angle")
#        plot_arena(f_arena, f_arena, 'inside', xy_cells.in_cell * 1.0,
#                   use_posneg=True, caption="inside")
        plot_arena(f_arena, f_arena, 'd_index', xy_cells.d_index % 2,
                   use_posneg=True, caption="d_index")
        plot_arena(f_arena, f_arena, 'a_index', xy_cells.a_index % 2,
                   use_posneg=True, caption="a_index")
        plot_arena(f_arena, f_arena, 'cells',
                   (xy_cells.a_index + xy_cells.d_index) % 2,
                   use_posneg=True, caption="Cells division")
        
       
    plot_arena(f_arena, f_arena, 'rate_sac_left',
               da2xy(stats['rate_saccade_left2']['mean']),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_LEFT_RGB),
               caption="Left saccading rate (saccades/s)")
    
    plot_arena(f_arena, f_arena, 'rate_sac_right',
               da2xy(stats['rate_saccade_right2']['mean']),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_RIGHT_RGB),
               caption="Right saccading rate (saccades/s)") 

    plot_arena(f_arena, f_arena, 'rate_sac',
               da2xy(stats['rate_saccade2']['mean']),
               scale_params=dict(max_color=[0, 0, 0.2], min_value=0),
               caption="Saccading rate (saccades/s)")

    order_params = dict(max_color=[0, 1, 0], min_color=[1, 0, 1])
    
    plot_arena(f_arena, f_arena, 'rate_saccade_left_order',
               da2xy(rate_saccade_left_order),
               scale_params=order_params,
               caption="order[ left saccade rate]")
   
    plot_arena(f_arena, f_arena, 'rate_saccade_right_order',
               da2xy(rate_saccade_right_order),
               scale_params=order_params,
               caption="order[ right saccade rate]")
   
    plot_arena(f_arena, f_arena, 'phi',
               da2xy(phi),
               scale_params={}, use_posneg=True,
                caption="""Normalized reduced stimulus. 
This is the 1D quantity that best explains the saccading rates,
assuming that there is a left-right symmetry. """)
    
    
    
    
    f_stimulus = r.figure('stimulus', cols=2)
    with r.data_pylab('behavior_rates_both_raw') as pylab:
        params = dict()
        pylab.plot(phi.flat, stats['rate_saccade2']['mean'].flat,
                   'k.', label='saccade (left or right)', **params)
        pylab.ylabel('Saccade rates')
        pylab.xlabel('Normalized reduced stimulus')
        pylab.legend()
        
    r.last().add_to(f_stimulus, caption="""
Saccade rate as a function of normalized stimulus. 
""")
    
       
    with r.data_pylab('behavior_rates_both_intervals') as pylab:
        plot_rate_bars(pylab, phi, stats['rate_saccade2'], 'k')
        pylab.ylabel('Behavior rates')
        pylab.xlabel('Normalized reduced stimulus')

    r.last().add_to(f_stimulus, caption="""
Same thing, but plotting 95% confidence intervals.

Note that it would be desirable to have x-axis error bars, but 
the analysis gets a bit complicated...
""")
#
#    sample_phi = np.linspace(-1,+1, 100)
#    sample_fit = 
#    x = phi
#    y = stats['rate_saccade2']
#    yerr = stats['rate_saccade2']['confidence']
#    
#    with r.data_pylab('behavior_rates_both_intervals_fit') as pylab:
#        plot_rate_bars(pylab, phi, stats['rate_saccade2'], 'k')
#        pylab.ylabel('Behavior rates')
#        pylab.xlabel('Normalized reduced stimulus')
#
#    r.last().add_to(f_stimulus, caption="""Robust fit""")
    
    with r.data_pylab('behavior_rates_raw') as pylab:
        pylab.plot(phi.flat, stats['rate_saccade_left2']['mean'].flat,
                   '%s.' % COL_LEFT, label='saccade left')
        pylab.plot(phi.flat, stats['rate_saccade_right2']['mean'].flat,
                   '%s.' % COL_RIGHT, label='saccade right')
        pylab.ylabel('Behavior rates')
        pylab.xlabel('Normalized reduced stimulus')
        pylab.legend()
        
    r.last().add_to(f_stimulus, caption="""
Behavior rates as a function of normalized stimulus. 

Because they are not monotone, we know there is at least another
relevant stimulus; note however that phi captures most of the dimensionality.
We could analyze the samples near 0 to find what is the other most important
feature.
""")
    
        
    with r.data_pylab('behavior_rates_raw_intervals') as pylab:
        plot_rate_bars(pylab, phi, stats['rate_saccade_left2'], COL_LEFT)
        plot_rate_bars(pylab, phi, stats['rate_saccade_right2'], COL_RIGHT)
        pylab.ylabel('Behavior rates')
        pylab.xlabel('Normalized reduced stimulus') 
        # TODO: set same scale
        
    r.last().add_to(f_stimulus, caption="""
Same thing, but plotting 95% confidence intervals.
This shows that the outliers are just noisy samples.
""")
    
    with r.data_pylab('behavior_prob_raw') as pylab: 
        pylab.plot(phi.flat, stats['prob_left2']['mean'].flat,
                   '%s.' % COL_LEFT, label='saccade left')
        pylab.plot(phi.flat, stats['prob_right2']['mean'].flat,
                   '%s.' % COL_RIGHT, label='saccade right')

        pylab.ylabel('Relative probability')
        pylab.xlabel('Normalized reduced stimulus')
        pylab.axis((-1, +1, 0, 1))
        pylab.legend()
        
    r.last().add_to(f_stimulus, caption="""
Direction choice probabilities 
(given that we are saccading, are we going left or right?).
""")
    
          
    with r.data_pylab('behavior_prob_raw_intervals') as pylab:
        plot_rate_bars(pylab, phi, stats['prob_left2'], COL_LEFT)
        plot_rate_bars(pylab, phi, stats['prob_right2'], COL_RIGHT)
        pylab.ylabel('Relative probability')
        pylab.xlabel('Normalized reduced stimulus') 
        pylab.axis((-1, +1, 0, 1))
    r.last().add_to(f_stimulus, caption="""
Same thing, but plotting 99% confidence intervals. 
""")
    
    # TODO: do not enlarge in rho direction
    return r

def plot_rate_bars(pylab, phi, st, color, **kwargs):
    phi = np.array(phi.flat)
    order = np.argsort(phi)
    phi = phi[order]
    mean = np.array(st['mean'].flat)[order]
    upper = np.array(st['upper'].flat)[order]
    lower = np.array(st['lower'].flat)[order]
    err_upper = upper - mean
    err_lower = mean - lower
    yerr = np.vstack((err_lower, err_upper))
    pylab.errorbar(x=phi, y=mean, yerr=yerr,
                    xerr=None, fmt=None,
                       ecolor=color,
                       capsize=0, # was 8
                        elinewidth=1, **kwargs)
    
def scale_score_norm(x):
    ''' Returns the score, normalized in [0,1] '''
    return scale_score(x).astype('float32') / (x.size - 1)

def scale_score(x):
    y = x.copy()
    order = np.argsort(x.flat)
    # Black magic ;-) Probably the smartest thing I came up with today. 
    order_order = np.argsort(order)
    y.flat[:] = order_order.astype(y.dtype)
    return y

def compute_interval(rate, perc=[1, 99]):
    limits = np.percentile(np.array(rate.flat), perc)
    min_rate = limits[0]
    max_rate = limits[1]
    return min_rate, max_rate
