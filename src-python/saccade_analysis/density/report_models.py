from .order_estimation import scale_score_norm
from .plot_utils import plot_arena, plot_image
from .xy_cells import XYCells
from reprep import Report
import numpy as np

COL_LEFT = 'r'
COL_LEFT_RGB = [1, 0, 0]

COL_RIGHT = 'b'
COL_RIGHT_RGB = [0, 0, 1]

COL_BOTH = 'k'
COL_BOTH_RGB = [0, 0, 0.2]

FEATURE_TEXT = 'Estimated feature'


figparams = dict(figsize=(2.5, 1.5))

def report_models_choice(confid, stats):
    r = Report('%s_models' % confid)
    
    cells = stats['cells']
    
    rate_saccade_left_order = scale_score_norm(stats['rate_saccade_left2']['mean'])
    rate_saccade_right_order = scale_score_norm(stats['rate_saccade_right2']['mean'])

    feature = stats['feature']
    phi = feature['mean']
    phi_var = feature['upper'] - feature['lower']
    
    ncells = 200
    xy_cells = XYCells(radius=1, ncells=ncells, da_cells=cells)

    da2xy = lambda F:  xy_cells.from_da_field(F.astype('float')) 
    
    f_counts = r.figure('counts', cols=3)
    
    plot_image(f_counts, f_counts, 'time_spent',
               cells, stats['time_spent'],
               scale_params=dict(min_value=0),
               caption="Time spent (s)")
  
    plot_image(f_counts, f_counts, 'mean_speed',
               cells, stats['mean_speed'],
               #scale_params=dict(min_value=0),
               caption="Mean speed in cell (m/s)")
  
    plot_image(f_counts, f_counts, 'mean_speed_sac_start',
               cells, stats['mean_speed_sac_start'],
               #scale_params=dict(min_value=0),
               caption="Mean speed at saccade start (m/s)")
    
    plot_image(f_counts, f_counts, 'total',
               cells, stats['total'],
               scale_params=dict(min_value=0, max_color=COL_BOTH_RGB),
               caption="Number of  saccades")
  
    plot_image(f_counts, f_counts, 'num_left',
               cells, stats['num_left'],
               scale_params=dict(min_value=0, max_color=COL_LEFT_RGB),
               caption="Number of left saccades")
  
    plot_image(f_counts, f_counts, 'num_right',
               cells, stats['num_right'],
               scale_params=dict(min_value=0, max_color=COL_RIGHT_RGB),
               caption="Number of right saccades")
    
    f_counts = r.figure('counts_arena', cols=3)
    
    plot_arena(f_counts, f_counts, 'time_spent',
               da2xy(stats['time_spent']),
               scale_params=dict(min_value=0),
               caption="Time spent (s)")
    
    plot_arena(f_counts, f_counts, 'mean_speed',
               da2xy(stats['mean_speed']),
               caption="Mean speed in cell (m/s)")
    plot_arena(f_counts, f_counts, 'mean_speed_sac_start',
               da2xy(stats['mean_speed_sac_start']),
               caption="Mean speed at saccade start (m/s)")
    
  
    plot_arena(f_counts, f_counts, 'total',
               da2xy(stats['total']),
               scale_params=dict(min_value=0, max_color=COL_BOTH_RGB),
               caption="Number of  saccades")
  
    plot_arena(f_counts, f_counts, 'num_left',
               da2xy(stats['num_left']),
               scale_params=dict(min_value=0, max_color=COL_LEFT_RGB),
               caption="Number of left saccades")
  
    plot_arena(f_counts, f_counts, 'num_right',
               da2xy(stats['num_right']),
               scale_params=dict(min_value=0, max_color=COL_RIGHT_RGB),
               caption="Number of right saccades")
  

    f_rates = r.figure('Saccade rates', cols=3)
    
    max_rate = np.nanmax([np.nanmax(stats['rate_saccade_left2']['mean']),
                          np.nanmax(stats['rate_saccade_right2']['mean']),
                          np.nanmax(stats['rate_saccade_L_est']['mean']),
                          np.nanmax(stats['rate_saccade_R_est']['mean'])])
    
    plot_image(r, f_rates, 'rate_sac',
               cells, stats['rate_saccade2']['mean'],
               scale_params=dict(max_color=COL_BOTH_RGB, min_value=0),
               caption="Saccading rate (saccades/s)")
    
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

    plot_image(r, f_rates, 'rate_saccade_L_est',
               cells, stats['rate_saccade_L_est']['mean'],
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_LEFT_RGB),
               caption="Est. left saccading rate (saccades/s)")
    
    plot_image(r, f_rates, 'rate_saccade_R_est',
               cells, stats['rate_saccade_R_est']['mean'],
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_RIGHT_RGB),
               caption="Est. right saccading rate (saccades/s)") 


    order_params = dict(max_color=[0, 1, 0], min_color=[1, 0, 1])
    
    plot_image(r, f_rates, 'rate_saccade_left_order',
               cells, rate_saccade_left_order,
               scale_params=order_params,
               caption="order[left saccade rate]")
   
    plot_image(r, f_rates, 'rate_saccade_right_order',
               cells, rate_saccade_right_order,
               scale_params=order_params,
               caption="order[right saccade rate]")
#   
#    phi_colors = dict(scale_params=dict(max_value= +1, min_value= -1,
#                                 min_color=COL_RIGHT_RGB,
#                                 max_color=COL_LEFT_RGB),
#                      use_posneg=False)
    phi_colors = dict(scale_params={},
                      use_posneg=True)
    plot_image(r, f_rates, 'phi', cells, phi,
               #scale_params={}, 
                caption="""%s. 
This is the 1D quantity that best explains the saccading rates,
assuming that there is a left-right symmetry. """ % FEATURE_TEXT, **phi_colors)

    plot_image(r, f_rates, 'phi_var', cells, phi_var,
               scale_params=dict(min_value=0), use_posneg=False,
                caption="""Uncertainty of in the feature estimate """)
    
    f_arena = r.figure('Arena view', cols=3)
    
    
    if False: # XXX
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
        

    plot_arena(f_arena, f_arena, 'rate_sac',
               da2xy(stats['rate_saccade2']['mean']),
               scale_params=dict(max_color=[0, 0, 0.2], min_value=0),
               caption="Saccading rate (saccades/s)")
    
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


    plot_arena(f_arena, f_arena, 'rate_saccade_L_est',
               da2xy(stats['rate_saccade_L_est']['mean']),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_LEFT_RGB),
               caption="Est. left saccade gen. rate (saccades/s)")
    
    plot_arena(f_arena, f_arena, 'rate_saccade_R_est',
               da2xy(stats['rate_saccade_R_est']['mean']),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_RIGHT_RGB),
               caption="Est. right saccade gen. rate (saccades/s)")

    order_params = dict(max_color=[0, 1, 0], min_color=[1, 0, 1])
    
    plot_arena(f_arena, f_arena, 'rate_saccade_left_order',
               da2xy(rate_saccade_left_order),
               scale_params=order_params,
               caption="order[ left saccade rate]")
   
    plot_arena(f_arena, f_arena, 'rate_saccade_right_order',
               da2xy(rate_saccade_right_order),
               scale_params=order_params,
               caption="order[ right saccade rate]")
   
    plot_arena(f_arena, f_arena, 'phi', da2xy(phi),
#               scale_params={}, use_posneg=True,
                caption="""Normalized reduced stimulus. 
This is the 1D quantity that best explains the saccading rates,
assuming that there is a left-right symmetry. """, **phi_colors)
    
    plot_arena(f_arena, f_arena, 'phi_var', da2xy(phi_var),
               scale_params=dict(min_value=0), use_posneg=False,
                caption="""Uncertainty in estimated stimulus""")
    
    raw_params = dict(markersize=1)
    int_params = dict(elinewidth=0.5)
    
    f_stimulus = r.figure('stimulus', cols=2)
    with r.plot('behavior_rates_both_raw', **figparams) as pylab:
        pylab.plot(phi.flat, stats['rate_saccade2']['mean'].flat,
                   'k.', label='saccade (left or right)', **raw_params)
        pylab.ylabel('Saccade rates')
        pylab.xlabel(FEATURE_TEXT)
        #pylab.legend()
        
    r.last().add_to(f_stimulus, caption="""
Saccade rate as a function of normalized stimulus. 
""")
    
       
    with r.plot('behavior_rates_both_intervals', **figparams) as pylab:
        plot_rate_bars(pylab, phi, stats['rate_saccade2'], 'k', **int_params)
        pylab.ylabel('Event rates')
        pylab.xlabel(FEATURE_TEXT)

    r.last().add_to(f_stimulus, caption="""
Same thing, but plotting 95% confidence intervals.

Note that it would be desirable to have x-axis error bars, but 
the analysis gets a bit complicated...
""")
    
    scale_rate = 6
    
    # plot error bars slightlty dealigned
    phir = phi + 0.005

    with r.plot('behavior_rates_raw', caption="""
Event rates as a function of normalized stimulus. 

Because they are not monotone, we know there is at least another
relevant stimulus; note however that phi captures most of the dimensionality.
We could analyze the samples near 0 to find what is the other most important
feature.""", **figparams) as pylab:
        pylab.plot(phi.flat, stats['rate_saccade_left2']['mean'].flat,
                   '%s.' % COL_LEFT, label='saccade left', **raw_params)
        pylab.plot(phi.flat, stats['rate_saccade_right2']['mean'].flat,
                   '%s.' % COL_RIGHT, label='saccade right', **raw_params)
        pylab.ylabel('Event rates')
        pylab.xlabel(FEATURE_TEXT)
        pylab.axis((-1, +1, 0, scale_rate))
        #pylab.legend()
        
    r.last().add_to(f_stimulus)
    
        
    with r.plot('behavior_rates_raw_intervals', caption="""
Same thing, but plotting 95% confidence intervals.
This shows that the outliers are just noisy samples.
""", **figparams) as pylab:
        plot_rate_bars(pylab, phi, stats['rate_saccade_left2'], COL_LEFT, **int_params)
        plot_rate_bars(pylab, phir, stats['rate_saccade_right2'], COL_RIGHT, **int_params)
        pylab.ylabel('Event rates')
        pylab.xlabel('Normalized reduced stimulus') 
        pylab.axis((-1, +1, 0, scale_rate))
        
    r.last().add_to(f_stimulus)
    
    with r.plot('behavior_rates_est',
                caption="""This is the rate estimated taking into account a refractory 
    period.""",
                **figparams) as pylab:
        pylab.plot(phi.flat, stats['rate_saccade_L_est']['mean'].flat,
                   '%s.' % COL_LEFT, label='saccade left', **raw_params)
        pylab.plot(phi.flat, stats['rate_saccade_R_est']['mean'].flat,
                   '%s.' % COL_RIGHT, label='saccade right', **raw_params)
        pylab.ylabel('Event rates')
        pylab.xlabel('Normalized reduced stimulus') 
        pylab.axis((-1, +1, 0, scale_rate))
    
    r.last().add_to(f_stimulus)
    
         
    with r.plot('behavior_rates_est_intervals',
                caption="Same thing, but plotting 95% confidence intervals.",
                **figparams) as pylab:
        plot_rate_bars(pylab, phi, stats['rate_saccade_L_est'], COL_LEFT, **int_params)
        plot_rate_bars(pylab, phir, stats['rate_saccade_R_est'], COL_RIGHT, **int_params)
        pylab.ylabel('Event rates')
        pylab.xlabel(FEATURE_TEXT) 
        pylab.axis((-1, +1, 0, scale_rate))
        
    r.last().add_to(f_stimulus)
    
    
    with r.plot('behavior_prob_raw',
                **figparams) as pylab: 
        pylab.plot(phi.flat, stats['prob_left2']['mean'].flat,
                   '%s.' % COL_LEFT, label='saccade left', **raw_params)
        pylab.plot(phi.flat, stats['prob_right2']['mean'].flat,
                   '%s.' % COL_RIGHT, label='saccade right', **raw_params)

        pylab.ylabel('Relative probability')
        pylab.xlabel(FEATURE_TEXT)
        pylab.axis((-1, +1, 0, 1))
        #pylab.legend()
        
    r.last().add_to(f_stimulus, caption="""
Direction choice probabilities 
(given that we are saccading, are we going left or right?).
""")
    
          
    with r.plot('behavior_prob_raw_intervals', caption="""
Same thing, but plotting 95% confidence intervals. 
""", **figparams) as pylab:
        plot_rate_bars(pylab, phi, stats['prob_left2'], COL_LEFT, **int_params)
        plot_rate_bars(pylab, phi, stats['prob_right2'], COL_RIGHT, **int_params)
        pylab.ylabel('Relative probability')
        pylab.xlabel('Normalized reduced stimulus') 
        pylab.axis((-1, +1, 0, 1))
    r.last().add_to(f_stimulus)
   
    with r.plot('model_manifold', caption="""Model manifold""", **figparams) as pylab:
        fL = stats['rate_saccade_L_est']['mean']
        fR = stats['rate_saccade_R_est']['mean']
        pylab.plot(fL, fR, 'k.', **raw_params)
        pylab.ylabel('f_L')
        pylab.xlabel('f_R') 
        #pylab.axis((-1, +1, 0, 1))
    r.last().add_to(f_stimulus)
    
    
    f_misc = r.figure('misc', cols=3)
    
    phi_threshold = 0.5
    phi_small = np.abs(phi) <= phi_threshold
    phi_large = np.abs(phi) >= phi_threshold
    plot_arena(f_misc, f_misc, 'phi_small', da2xy(phi_small),
               scale_params={}, use_posneg=True,
               caption=""" |z| <= %g """ % phi_threshold)
    plot_arena(f_misc, f_misc, 'phi_large', da2xy(phi_large),
               scale_params={}, use_posneg=True,
               caption=""" |z| >= %g """ % phi_threshold)
   
#    rate_threshold = 1.5
   
    feature_small_rate_L = stats['rate_saccade_L_est']['mean'] * phi_small
    feature_small_rate_R = stats['rate_saccade_R_est']['mean'] * phi_small
    feature_large_rate_L = stats['rate_saccade_L_est']['mean'] * phi_large
    feature_large_rate_R = stats['rate_saccade_R_est']['mean'] * phi_large
    
    plot_arena(f_misc, f_misc, 'phi_small_rate_L', da2xy(feature_small_rate_L),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_LEFT_RGB),
               caption="""Left rate (|z| <= %g) """ % phi_threshold)
    plot_arena(f_misc, f_misc, 'phi_small_rate_R', da2xy(feature_small_rate_R),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_RIGHT_RGB),
               caption="""Right rate (|z| <= %g) """ % phi_threshold)
    plot_arena(f_misc, f_misc, 'phi_large_rate_L', da2xy(feature_large_rate_L),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_LEFT_RGB),
               caption="""Left rate (|z| >= %g) """ % phi_threshold)
    plot_arena(f_misc, f_misc, 'phi_large_rate_R', da2xy(feature_large_rate_R),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=COL_RIGHT_RGB),
               caption="""Right rate (|z| >= %g) """ % phi_threshold)
         
    with r.plot('behavior_rates_est_intervals_small_stimulus',
                caption="Saccade rates for small stimulus.",
                **figparams) as pylab: 
        pylab.plot(phi.flat, feature_small_rate_L.flat,
                   '%s.' % COL_LEFT, label='saccade left', **raw_params)
        pylab.plot(phi.flat, feature_small_rate_R.flat,
                   '%s.' % COL_RIGHT, label='saccade right', **raw_params)
      
        pylab.ylabel('Event rates')
        pylab.xlabel(FEATURE_TEXT) 
        pylab.axis((-1, +1, 0, scale_rate))
        
    r.last().add_to(f_misc)
      
    with r.plot('stimulus_uncertainty',
                caption="Errors on the estimate of z.",
                **figparams) as pylab:
        plot_rate_bars(pylab, feature['mean'], feature, COL_BOTH, **int_params) 
        pylab.ylabel('Uncertainty on feature determination')
        pylab.xlabel(FEATURE_TEXT) 
        pylab.axis((-1, +1, -1, +1))
        
    r.last().add_to(f_stimulus)
    
    
    return r

def plot_rate_bars(pylab, phi, st, color, elinewidth=1, **kwargs):
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
                         elinewidth=elinewidth, ** kwargs)
    

def compute_interval(rate, perc=[1, 99]):
    limits = np.percentile(np.array(rate.flat), perc)
    min_rate = limits[0]
    max_rate = limits[1]
    return min_rate, max_rate
