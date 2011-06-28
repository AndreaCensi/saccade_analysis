import sys, numpy as np, traceback
from optparse import OptionParser
 
from flydra_db import safe_flydra_db_open 
from ..tammero.tammero_analysis import add_position_information_to_rows
from .density_estimation import compute_histogram
from reprep import Report
import os
import itertools 
import pickle
from geometric_saccade_detector.well_formed_saccade import check_saccade_is_well_formed
from saccade_analysis.tammero.tammero_analysis import add_position_information


from reprep import Report
from compmake import use_filesystem, comp, compmake_console 
from flydra_db import safe_flydra_db_open 
from saccade_analysis.density.density_estimation import compute_histogram_saccades
from reprep.graphics.scale import scale
from reprep.graphics.posneg import posneg

from saccade_analysis.tammero_flydradb.report_axis_angle import binomial_stats

 


description = """  """


from . import logger

def main():
    #np.seterr(all='raise')
    
    parser = OptionParser(usage=description)
    parser.add_option("--db", help="Main data directory")
    parser.add_option("--outdir", help="Output directory")
    parser.add_option("--group", help="Sample group", default='nopost')
    
    parser.add_option("--ncells_distance", type='int', default=20,
                      help="Discretization for distance")
    parser.add_option("--ncells_axis_angle", type='int', default=36,
                      help="Discretization for axis angle")
    
    (options, args) = parser.parse_args() #@UnusedVariable
    
    try:
        if args:
            raise Exception('Spurious arguments %r.' % args)
    
        if not options.db:
            raise Exception('Please provide --db option')
    
        if not options.outdir:
            raise Exception('Please provide --outdir option')
        
    except Exception as e:
        logger.error('Error while parsing configuration.')
        logger.error(str(e))
        sys.exit(-1)
  
    try:
        
        compmake_dir = os.path.join(options.outdir, 'compmake')
        use_filesystem(compmake_dir)
        
        confid = '%s-D%d-A%d' % (options.group, options.ncells_distance,
                              options.ncells_axis_angle)
          
        bin_enlarge_dist = 0.05
        bin_enlarge_angle = 10
        stats = comp(get_group_density_stats, options.db, options.group,
                             ncells_axis_angle=options.ncells_axis_angle,
                            ncells_distance=options.ncells_distance,
                             bin_enlarge_dist=bin_enlarge_dist,
                             bin_enlarge_angle=bin_enlarge_angle)
          
        saccades = comp(get_saccades_for_group, options.db, options.group)
        saccades_stats = comp(compute_histogram_saccades, saccades, stats,
                              bin_enlarge_dist=bin_enlarge_dist,
                              bin_enlarge_angle=bin_enlarge_angle)
        
        report = comp(report_stats, confid, stats, saccades_stats)
        
        
        html = os.path.join(options.outdir, "%s.html" % confid)
        rd = os.path.join(options.outdir, 'images')
           
        comp(write_report, report, html, rd)
        
        compmake_console()


    except Exception as e:
        logger.error('Error while processing. Exception and traceback follow.')
        logger.error(str(e))
        logger.error(traceback.format_exc())
        sys.exit(-2)
        
def report_stats(id, stats, saccades_stats):
    r = Report(id)
    
    distance_edges = stats['distance_edges']
    axis_angle_edges = stats['axis_angle_edges']
    count = stats['count']
    #mean_speed = stats['mean_speed']
    #time_spent = stats['time_spent']
    #probability = stats['probability']
    
    f = r.figure('flight')
    
    plot_image(r, f, 'transit', distance_edges, axis_angle_edges, count,
               caption="Transit probability")
    #plot_image(r, f, 'mean_speed', distance_edges, axis_angle_edges, mean_speed)
    #plot_image(r, f, 'time_spent', distance_edges, axis_angle_edges, time_spent)
    #plot_image(r, f, 'probability', distance_edges, axis_angle_edges, probability)
    
    f2 = r.figure('saccades', cols=2) 
  
    total = saccades_stats['total']
    num_left = saccades_stats['num_left']
    num_right = saccades_stats['num_right']
    prob_left = np.zeros(total.shape)
    prob_right = np.zeros(total.shape)
    skewed = np.zeros(total.shape)
    for a, d in itertools.product(range(len(axis_angle_edges) - 1),
                                      range(len(distance_edges) - 1)):
        
    
        pl, pr, ml, mr = \
            binomial_stats(total[d, a], num_left[d, a], num_right[d, a])
            
        prob_left[d, a] = pl
        prob_right[d, a] = pr
        skewed[d, a] = 0 if (ml[0] < 0.5 and 0.5 < ml[1])  else 1
    
    #  plot_image(r, f2, 'total', distance_edges, axis_angle_edges, total)
    max_num = max(num_left.max(), num_right.max())
    min_num = min(num_left.min(), num_right.min())
    scale_params = dict(max_value=max_num, min_value=min_num)
    plot_image(r, f2, 'num_left', distance_edges, axis_angle_edges, num_left,
               scale_params=scale_params,
               caption="Raw count of left saccades")
    plot_image(r, f2, 'num_right', distance_edges, axis_angle_edges, num_right,
               scale_params=scale_params,
               caption="Raw count of right saccades")

    plot_image(r, f2, 'prob_left',
               distance_edges, axis_angle_edges, prob_left,
               scale_params=dict(min_value=0, max_value=1),
               caption="Prob. of saccading left (if saccading)")
    plot_image(r, f2, 'prob_right',
               distance_edges, axis_angle_edges, prob_right,
               scale_params=dict(min_value=0, max_value=1),
               caption="Prob. of saccading right (if saccading)")
    
    plot_image(r, f2, 'skewed',
               distance_edges, axis_angle_edges, skewed,
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
               distance_edges, axis_angle_edges, prob_sac,
               scale_params=dict(skim=1, max_color=[0, 0, 0.2],),
               caption="Saccading rate (saccades/s)")
    plot_image(r, f3, 'rate_sac_left',
               distance_edges, axis_angle_edges, prob_sac_left,
               scale_params=scale_params,
               caption="Left saccading rate (saccades/s)")
    plot_image(r, f3, 'rate_sac_right',
               distance_edges, axis_angle_edges, prob_sac_right,
               scale_params=scale_params,
               caption="Right saccading rate (saccades/s)")
    
    
    baseline_rate = np.percentile(np.array(prob_sac[-4:, :].flat), 65)
    prob_sac2 = np.array(prob_sac)
    prob_sac2 [prob_sac < baseline_rate] = np.NaN
    
    print('baseline_rate is %g' % baseline_rate)
#    plot_image(r, f3, 'prob_sac2',
#               distance_edges, axis_angle_edges, prob_sac2,
#               caption="Used to compute baseline saccade rate")
    
    baseline = np.mean([ np.mean(prob_sac_left[-4:, :]),
                        np.mean(prob_sac_right[-4:, :])])
    print('baseline is %g' % baseline)
    
    baseline_both = np.mean(prob_sac[-4:, :])
    print('baseline_both is %g' % baseline_both)
    
    sac_norm = prob_sac - baseline_both
    sac_left_norm = prob_sac_left - baseline 
    sac_right_norm = prob_sac_right - baseline 
    skim = 1
    plot_image(r, f3, 'sac_norm',
               distance_edges, axis_angle_edges, sac_norm,
               use_posneg=True,
               scale_params=dict(skim=skim),
               caption='Saccade rate over baseline')
    
    max_value = max(sac_left_norm.max(), sac_right_norm.max())
    plot_image(r, f3, 'sac_left_norm',
               distance_edges, axis_angle_edges, sac_left_norm,
                use_posneg=True,
               scale_params=dict(max_value=max_rate - baseline),
               caption='Left saccade rate over baseline')
    
    
    plot_image(r, f3, 'sac_right_norm',
               distance_edges, axis_angle_edges, sac_right_norm,
               use_posneg=True,
               scale_params=dict(max_value=max_rate - baseline),
               caption='Right saccade rate over baseline')
    r.text('comment', 'The last three figures display in red '
           'the areas where the fly saccades more than the baseline.')
    


    return r

def plot_image(r, f, nid, d_edges, a_edges, field, caption=None, scale_params={},
               use_posneg=False):
    
    if use_posneg:
        rgb = posneg(field, **scale_params) / 255.0
    else:
        rgb = scale(field, **scale_params) / 255.0
         
    with r.data_pylab(nid) as pl:
        pl.title(nid if caption is None else caption)
        pl.xlabel('axis angle (deg)')
        pl.ylabel('distance from wall (m)')
        for a, d in itertools.product(range(len(a_edges) - 1),
                                      range(len(d_edges) - 1)):
            a_min = a_edges[a]
            a_max = a_edges[a + 1] 
            d_min = d
            d_max = d + 1
            quatx = [a_min, a_min, a_max, a_max]
            quaty = [d_min, d_max, d_max, d_min] 
            pl.fill(quatx, quaty, color=rgb[d, a, :])
            
        labels_at = [0, 0.15, 0.25, 0.5, 0.75, 1]
        tick_pos = []
        tick_label = []
        for l in labels_at:
            closest = np.argmin(np.abs(d_edges - l))
            tick_pos.append(closest)
            tick_label.append('%.2f' % l)
        pl.yticks(tick_pos, tick_label)
        pl.axis((a_edges[0], a_edges[-1], tick_pos[1], len(d_edges) - 1))
    r.last().add_to(f, caption=caption)
#
#def plot_image_nonscaled(r, f, nid, d_edges, a_edges, field, caption=None, skim=0):
#    
#    rgb = scale(field, skim=skim) / 255.0
#         
#    with r.data_pylab(nid) as pl:
#        pl.title(nid)
#        pl.xlabel('axis angle (deg)')
#        pl.ylabel('distance from wall')
#        for a, d in itertools.product(range(len(a_edges) - 1),
#                                      range(len(d_edges) - 1)):
#            a_min = a_edges[a]
#            a_max = a_edges[a + 1] 
#            d_min = d_edges[d]
#            d_max = d_edges[d + 1]   
#            quatx = [a_min, a_min, a_max, a_max]
#            quaty = [d_min, d_max, d_max, d_min] 
#            pl.fill(quatx, quaty, color=rgb[d, a, :])
#        pl.axis((a_edges[0], a_edges[-1], d_edges[0], d_edges[-1]))
#    r.last().add_to(f, caption=caption)
#   
   
def zoom(x, n):
    k = np.ones((n, n))
    return np.kron(x, k) 
    

def write_report(report, html, rd):
    print('Writing to %r.' % html)
    report.to_html(html, resources_dir=rd)

def get_group_density_stats(flydra_db_directory, db_group,
                            ncells_distance, ncells_axis_angle,
                             bin_enlarge_dist=0,
                             bin_enlarge_angle=0):
    with safe_flydra_db_open(flydra_db_directory) as db:
        rows = db.get_table_for_group(db_group, table='rows')
        
        print('Read %d rows' % len(rows))
    
        print('Computing extra information')
        rowsp = add_position_information_to_rows(rows)
        
        print('Computing histogram')
        stats = compute_histogram(
                    rowsp,
                    ncells_axis_angle=ncells_axis_angle,
                    ncells_distance=ncells_distance,
                     bin_enlarge_dist=bin_enlarge_dist,
                    bin_enlarge_angle=bin_enlarge_angle)
        return stats


def get_saccades_for_group(flydra_db_directory, db_group):
    
    with safe_flydra_db_open(flydra_db_directory) as db:
        
        saccades = db.get_table_for_group(db_group, 'saccades')
        if len(saccades) == 0:
            raise Exception('No saccades found for group %r.' % db_group)
        
        for s in saccades:
            check_saccade_is_well_formed(s)
            
        saccades = add_position_information(saccades) # XXX: using default arena size
       
        return saccades
