from . import (PlotParams, XYCells, plot_arena, plot_image, scale_score_norm, np,
    Report, ParamsEstimation)
from reprep.plot_utils.spines import set_spines_look_A


def report_models_choice(confid, stats):
    r = Report('%s_models' % confid)
    
    figparams = dict(figsize=PlotParams.figsize)

    cells = stats['cells']
    
    rate_saccade_left_order = scale_score_norm(
                                    stats['rate_saccade_left2']['mean'])
    rate_saccade_right_order = scale_score_norm(
                                    stats['rate_saccade_right2']['mean'])

    feature = stats['feature']
    phi = feature['mean']
    phi_var = feature['upper'] - feature['lower']
    
    ncells = 200  # XXX: repeated
    xy_cells = XYCells(radius=ParamsEstimation.arena_radius,
                       ncells=ncells, da_cells=cells)

    da2xy = lambda F:  xy_cells.from_da_field(F.astype('float')) 

    
    # XXX: detect this
    
    speed_format = dict(colors='cmap',
                        scale_params=dict(cmap=PlotParams.cmap_speed,
                                          **PlotParams.speed_bounds),
                        scale_format='%.2f')
    total_format = dict(colors='cmap',
                        scale_params=dict(min_value=0, cmap=PlotParams.cmap_total),
                        scale_format='%d')
               
    phi_colors = dict(scale_params={}, colors='posneg')
    
    
    num_left_saccades_format = dict(colors='scale',
                                    scale_params=dict(
                                            min_value=0,
                                            min_color=[1, 1, 1],
                                            max_color=PlotParams.COL_LEFT_RGB),
                                    scale_format='%d')
    num_right_saccades_format = dict(colors='scale',
                                     scale_params=dict(min_value=0,
                                                       min_color=[1, 1, 1],
                                        max_color=PlotParams.COL_RIGHT_RGB),
                                    scale_format='%d')
                               
                               
                               
    f_counts = r.figure('counts', cols=3)
    f_arena = r.figure('counts_arena', cols=3)
    
    def plot_both(name, field, caption, **kwargs):
    
        plot_image(f_counts, f_counts, name, cells, field, caption=caption,
                   **kwargs)
      
        plot_arena(f_arena, f_arena, name, da2xy(field), caption=caption,
                   **kwargs)
        
    seconds2minutes = 1 / 60.0
    samples2seconds = 1 / 60.0 # XXX fixed
    plot_both('time_spent', stats['count'] * samples2seconds * seconds2minutes,
              "Time spent (min)",
              scale_params=dict(min_value=0),
              scale_format='%.2f')


    
    plot_image(f_counts, f_counts, 'mean_speed',
               cells, stats['mean_speed'],
               caption="Mean speed in cell (m/s)",
               **speed_format)
  
    plot_image(f_counts, f_counts, 'mean_speed_sac_start',
               cells, stats['mean_speed_sac_start'],
               caption="Mean speed at saccade start (m/s)",
               **speed_format)
    
    
    plot_both('num_left', stats['num_left'].astype('int'),
              caption="Number of left saccades",
              **num_left_saccades_format)
    
    
    plot_both('num_right', stats['num_right'].astype('int'),
              caption="Number of right saccades",
              **num_right_saccades_format)
    
    
    
    plot_image(f_counts, f_counts, 'total',
               cells, stats['total'],
               caption="Number of saccades",
               **total_format)
   
    
    plot_arena(f_arena, f_arena, 'mean_speed', da2xy(stats['mean_speed']),
               caption="Mean speed in cell (m/s)",
               **speed_format)
    plot_arena(f_arena, f_arena, 'mean_speed_sac_start',
               da2xy(stats['mean_speed_sac_start']),
               caption="Mean speed at saccade start (m/s)",
               **speed_format)
    
  
    plot_arena(f_arena, f_arena, 'total', da2xy(stats['total']),
               caption="Number of saccades",
               **total_format) 

    f_rates = r.figure('Event_rates', cols=3)
    f_arena = r.figure('Arena_view', cols=3)
    
#    max_rate = np.nanmax([np.nanmax(stats['rate_saccade_left2']['mean']),
#                          np.nanmax(stats['rate_saccade_right2']['mean']),
#                          np.nanmax(stats['rate_saccade_L_est']['mean']),
#                          np.nanmax(stats['rate_saccade_R_est']['mean'])])
    
    max_rate = PlotParams.max_rate
    
    sum_format = dict(scale_params=dict(min_value=0),
                      colors='cmap')   
    
    plot_image(r, f_rates, 'rate_sac',
               cells, stats['rate_saccade2']['mean'],
               caption="Saccading rate (saccades/s)",
                **sum_format)
    
    plot_image(r, f_rates, 'rate_sac_left',
               cells, stats['rate_saccade_left2']['mean'],
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=PlotParams.COL_LEFT_RGB),
               caption="Left saccading rate (saccades/s)")
    
    plot_image(r, f_rates, 'rate_sac_right',
               cells, stats['rate_saccade_right2']['mean'],
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=PlotParams.COL_RIGHT_RGB),
               caption="Right saccading rate (saccades/s)") 

    plot_image(r, f_rates, 'rate_saccade_L_est',
               cells, stats['rate_saccade_L_est']['mean'],
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=PlotParams.COL_LEFT_RGB),
               caption="Est. left saccading rate (saccades/s)")
    
    plot_image(r, f_rates, 'rate_saccade_R_est',
               cells, stats['rate_saccade_R_est']['mean'],
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=PlotParams.COL_RIGHT_RGB),
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
    
    plot_image(r, f_rates, 'phi', cells, phi,
                caption="""%s. 
This is the 1D quantity that best explains the saccading rates,
assuming that there is a left-right symmetry. """ % PlotParams.FEATURE_TEXT,
                **phi_colors)

    plot_image(r, f_rates, 'phi_var', cells, phi_var,
               scale_params=dict(min_value=0), colors='scale',
                caption="""Uncertainty of in the feature estimate """)
    
    
    
    if False: # XXX
        plot_arena(f_arena, f_arena, 'x', xy_cells.x,
                   colors='posneg', caption="x")
        plot_arena(f_arena, f_arena, 'y', xy_cells.y,
                   colors='posneg', caption="y")
        plot_arena(f_arena, f_arena, 'd', xy_cells.d,
                   colors='posneg', caption="d")
        plot_arena(f_arena, f_arena, 'axis_angle', xy_cells.axis_angle_deg,
                   colors='posneg', caption="axis_angle")
        plot_arena(f_arena, f_arena, 'd_index', xy_cells.d_index % 2,
                   colors='posneg', caption="d_index")
        plot_arena(f_arena, f_arena, 'a_index', xy_cells.a_index % 2,
                   colors='posneg', caption="a_index")
        plot_arena(f_arena, f_arena, 'cells',
                   (xy_cells.a_index + xy_cells.d_index) % 2,
                   colors='posneg', caption="Cells division")
        

    plot_arena(f_arena, f_arena, 'rate_sac',
               da2xy(stats['rate_saccade2']['mean']),
               caption="Saccading rate (saccades/s)",
               **sum_format)
    
    plot_arena(f_arena, f_arena, 'rate_sac_left',
               da2xy(stats['rate_saccade_left2']['mean']),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=PlotParams.COL_LEFT_RGB),
               caption="Left saccading rate (saccades/s)")
    
    plot_arena(f_arena, f_arena, 'rate_sac_right',
               da2xy(stats['rate_saccade_right2']['mean']),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=PlotParams.COL_RIGHT_RGB),
               caption="Right saccading rate (saccades/s)") 


    plot_arena(f_arena, f_arena, 'rate_saccade_L_est',
               da2xy(stats['rate_saccade_L_est']['mean']),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=PlotParams.COL_LEFT_RGB),
               caption="Est. left saccade gen. rate (saccades/s)")
    
    plot_arena(f_arena, f_arena, 'rate_saccade_R_est',
               da2xy(stats['rate_saccade_R_est']['mean']),
               scale_params=dict(max_value=max_rate, min_value=0,
                                 max_color=PlotParams.COL_RIGHT_RGB),
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
#               scale_params={}, colors='posneg',
                caption="""Normalized reduced stimulus. 
This is the 1D quantity that best explains the saccading rates,
assuming that there is a left-right symmetry. """, **phi_colors)
    
    plot_arena(f_arena, f_arena, 'phi_var', da2xy(phi_var),
               scale_params=dict(min_value=0), colors='scale',
                caption="""Uncertainty in estimated stimulus""")
    
    raw_params = dict(markersize=1)
    int_params = dict(elinewidth=0.5)
    
    f_stimulus = r.figure('stimulus', cols=2)

    with r.plot('behavior_rates_both_raw',
                caption="""Saccade rate as a function of normalized stimulus.""",
                **figparams) as pylab:
        compact_labeling_rates(pylab, PlotParams.TEXT_EVENT_GEN_RATES)
        pylab.plot(phi.flat, stats['rate_saccade2']['mean'].flat,
                   'k.', label='saccade (left or right)', **raw_params)
        #pylab.legend()
        
    r.last().add_to(f_stimulus)
    
       
    with r.plot('behavior_rates_both_intervals', **figparams) as pylab:
        compact_labeling_rates(pylab, PlotParams.TEXT_EVENT_GEN_RATES)
        plot_rate_bars(pylab, phi, stats['rate_saccade2'], 'k', **int_params)
        
    r.last().add_to(f_stimulus, caption="""
Same thing, but plotting 95% confidence intervals.

Note that it would be desirable to have x-axis error bars, but 
the analysis gets a bit complicated...
""")
    

    # plot error bars slightlty dealigned
    phir = phi + 0.005

 
    with r.plot('behavior_rates_raw', caption="""
Event rates as a function of normalized stimulus.  

Because they are not monotone, we know there is at least another
relevant stimulus; note however that phi captures most of the dimensionality.
We could analyze the samples near 0 to find what is the other most important
feature.""", **figparams) as pylab:
        pylab.plot(phi.flat, stats['rate_saccade_left2']['mean'].flat,
                   '%s.' % PlotParams.COL_LEFT, label=PlotParams.LABEL_LEFT,
                   **raw_params)
        pylab.plot(phi.flat, stats['rate_saccade_right2']['mean'].flat,
                   '%s.' % PlotParams.COL_RIGHT, label=PlotParams.LABEL_RIGHT,
                   **raw_params)
        compact_labeling_rates(pylab, PlotParams.TEXT_OBSERVED_EVENT_RATES)
        

    r.last().add_to(f_stimulus)
    
         
    def plot_rate_bars_x(pylab, left, right, ylabel):
        plot_rate_bars(pylab, phi, left,
                       PlotParams.COL_LEFT, label=PlotParams.LABEL_LEFT,
                       **int_params)
        plot_rate_bars(pylab, phir, right,
                       PlotParams.COL_RIGHT, label=PlotParams.LABEL_RIGHT,
                        **int_params)
        compact_labeling_rates(pylab, ylabel)
        pylab.legend()
   
    with r.plot('behavior_rates_raw_intervals',
                caption="""
                    Same thing, but plotting 95% confidence intervals.
                    This shows that the outliers are just noisy samples.
                """, **figparams) as pylab:
        plot_rate_bars_x(pylab,
                         stats['rate_saccade_left2'],
                         stats['rate_saccade_right2'],
                         PlotParams.TEXT_OBSERVED_EVENT_RATES)

    r.last().add_to(f_stimulus)
     
    with r.plot('behavior_rates_est', caption="""
                  This is the rate estimated taking into account a refractory 
                  period.
                """, **figparams) as pylab: 
        pylab.plot(phi.flat, stats['rate_saccade_L_est']['mean'].flat,
                   '%s.' % PlotParams.COL_LEFT, label='saccade left', **raw_params)
        pylab.plot(phi.flat, stats['rate_saccade_R_est']['mean'].flat,
                   '%s.' % PlotParams.COL_RIGHT, label='saccade right', **raw_params)
        compact_labeling_rates(pylab, PlotParams.TEXT_EVENT_GEN_RATES)
            
    r.last().add_to(f_stimulus)
     
    with r.plot('behavior_rates_est_intervals',
                caption="Same thing, but plotting 95% confidence intervals.",
                **figparams) as pylab:
        plot_rate_bars_x(pylab,
                 stats['rate_saccade_L_est'],
                 stats['rate_saccade_R_est'],
                 PlotParams.TEXT_EVENT_GEN_RATES) 
        
    r.last().add_to(f_stimulus)
    
     
    with r.plot('behavior_prob_raw', caption="""
                  Direction choice probabilities 
                  (given that we are saccading, are we going left or right?).
                """, **figparams) as pylab:  
        compact_feature_xlabel(pylab)
        pylab.axis((-1, +1, 0, 1))
        pylab.plot(phi.flat, stats['prob_left2']['mean'].flat,
                   '%s.' % PlotParams.COL_LEFT, label='saccade left', **raw_params)
        pylab.plot(phi.flat, stats['prob_right2']['mean'].flat,
                   '%s.' % PlotParams.COL_RIGHT, label='saccade right', **raw_params)

        pylab.ylabel('Relative probability')
        
    r.last().add_to(f_stimulus)
     
    with r.plot('behavior_prob_raw_intervals', caption="""
                Same thing, but plotting 95% confidence intervals. 
                """, **figparams) as pylab:
        pylab.axis((-1, +1, 0, 1))
        compact_feature_xlabel(pylab)
        plot_rate_bars(pylab, phi, stats['prob_left2'], PlotParams.COL_LEFT, **int_params)
        plot_rate_bars(pylab, phi, stats['prob_right2'], PlotParams.COL_RIGHT, **int_params)
        pylab.ylabel('Relative probability') 
    r.last().add_to(f_stimulus)
    
    
    if False:
        with r.plot('model_manifold', caption="""Model manifold""", **figparams) as pylab:
            fL = stats['rate_saccade_L_est']['mean']
            fR = stats['rate_saccade_R_est']['mean']
            pylab.plot(fL, fR, 'k.', **raw_params)
            pylab.ylabel('$f_L$')
            pylab.xlabel('$f_R$') 
            #pylab.axis((-1, +1, 0, 1))
        r.last().add_to(f_stimulus)
    
        
        f_misc = r.figure('misc', cols=3)
        
        phi_threshold = 0.5
        phi_small = np.abs(phi) <= phi_threshold
        phi_large = np.abs(phi) >= phi_threshold
        plot_arena(f_misc, f_misc, 'phi_small', da2xy(phi_small),
                   scale_params={}, colors='posneg',
                   caption=""" |z| <= %g """ % phi_threshold)
        plot_arena(f_misc, f_misc, 'phi_large', da2xy(phi_large),
                   scale_params={}, colors='posneg',
                   caption=""" |z| >= %g """ % phi_threshold)
       
    #    rate_threshold = 1.5
       
        feature_small_rate_L = stats['rate_saccade_L_est']['mean'] * phi_small
        feature_small_rate_R = stats['rate_saccade_R_est']['mean'] * phi_small
        feature_large_rate_L = stats['rate_saccade_L_est']['mean'] * phi_large
        feature_large_rate_R = stats['rate_saccade_R_est']['mean'] * phi_large
        
        plot_arena(f_misc, f_misc, 'phi_small_rate_L', da2xy(feature_small_rate_L),
                   scale_params=dict(max_value=max_rate, min_value=0,
                                     max_color=PlotParams.COL_LEFT_RGB),
                   caption="""Left rate (|z| <= %g) """ % phi_threshold)
        plot_arena(f_misc, f_misc, 'phi_small_rate_R', da2xy(feature_small_rate_R),
                   scale_params=dict(max_value=max_rate, min_value=0,
                                     max_color=PlotParams.COL_RIGHT_RGB),
                   caption="""Right rate (|z| <= %g) """ % phi_threshold)
        plot_arena(f_misc, f_misc, 'phi_large_rate_L', da2xy(feature_large_rate_L),
                   scale_params=dict(max_value=max_rate, min_value=0,
                                     max_color=PlotParams.COL_LEFT_RGB),
                   caption="""Left rate (|z| >= %g) """ % phi_threshold)
        plot_arena(f_misc, f_misc, 'phi_large_rate_R', da2xy(feature_large_rate_R),
                   scale_params=dict(max_value=max_rate, min_value=0,
                                     max_color=PlotParams.COL_RIGHT_RGB),
                   caption="""Right rate (|z| >= %g) """ % phi_threshold)
           
        with r.plot('behavior_rates_est_intervals_small_stimulus',
                    caption="Event rates for small stimulus.",
                    **figparams) as pylab: 
            pylab.plot(phi.flat, feature_small_rate_L.flat,
                       '%s.' % PlotParams.COL_LEFT, label='saccade left', **raw_params)
            pylab.plot(phi.flat, feature_small_rate_R.flat,
                       '%s.' % PlotParams.COL_RIGHT, label='saccade right', **raw_params)
            compact_labeling_rates(pylab, PlotParams.TEXT_EVENT_GEN_RATES)
            
        r.last().add_to(f_misc)
           
        with r.plot('stimulus_uncertainty',
                    caption="Errors on the estimate of z.",
                    **figparams) as pylab:
            plot_rate_bars(pylab, feature['mean'], feature,
                           PlotParams.COL_BOTH, **int_params) 
            pylab.ylabel('Uncertainty of feature estimate')
            compact_feature_xlabel(pylab)
            pylab.axis((-1, +1, -1, +1))
            
        r.last().add_to(f_stimulus)
        
        
    return r

def compact_labeling_rates(pylab, ylabel):
    compact_feature_xlabel(pylab)
    pylab.ylabel(ylabel)
        
    xt = [0, 1, 2, 3, 4, 5, 6]
    xtt = ["0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0"]
    pylab.yticks(xt, xtt) 
    pylab.axis((-1, +1, 0, PlotParams.max_rate))
    #pylab.gca().yaxis.set_ticks_position('right')
    #pylab.gca().yaxis.set_label_coords(0, 0.5)
    
def compact_feature_xlabel(pylab):
    #pylab.gca().xaxis.set_label_coords(0.5, -0.02)    
    set_spines_look_A(pylab, PlotParams.spines_outward)
    pylab.xlabel(PlotParams.FEATURE_TEXT) 
    
    xt = [-1, -0.5, 0, 0.5, +1]
    xtt = ["-1", "-0.5", "0", "+0.5", "+1"]
    pylab.xticks(xt, xtt) 

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
