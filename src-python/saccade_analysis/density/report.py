from . import logger
from ..density.density_estimation import (compute_histogram,
    compute_histogram_saccades)
from ..tammero.tammero_analysis import (add_position_information,
    add_position_information_to_rows) 
from compmake import use_filesystem, comp, compmake_console
from flydra_db import safe_flydra_db_open
from geometric_saccade_detector.well_formed_saccade import (
    check_saccade_is_well_formed)
from optparse import OptionParser 
import numpy as np
import os
import sys
import traceback
from .report_models import report_models_choice
from .statistics import compute_joint_statistics 
from .report_previous import report_stats

 
description = """  """



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
        
        
        joint_stats = comp(compute_joint_statistics, stats, saccades_stats)
        
        report = comp(report_stats, confid, stats, saccades_stats)
        rd = os.path.join(options.outdir, 'images')
        html = os.path.join(options.outdir, "%s.html" % confid)
        comp(write_report, report, html, rd)
        
        report_m = comp(report_models_choice, confid, joint_stats)        
        html = os.path.join(options.outdir, "%s_models.html" % confid)
        comp(write_report, report_m, html, rd)
        
        compmake_console()


    except Exception as e:
        logger.error('Error while processing. Exception and traceback follow.')
        logger.error(str(e))
        logger.error(traceback.format_exc())
        sys.exit(-2)
        
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
