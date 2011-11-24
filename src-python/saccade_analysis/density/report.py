from . import (DACells, logger, compute_histogram, compute_histogram_saccades,
    compute_joint_statistics, report_models_choice, report_stats,
    report_visual_stimulus, compute_visual_stimulus, report_intuitive)
from ..tammero.tammero_analysis import (add_position_information,
    add_position_information_to_rows) # XXX: remove
from compmake import use_filesystem, comp, compmake_console
from flydra_db import safe_flydra_db_open
from geometric_saccade_detector import check_saccade_is_well_formed
from optparse import OptionParser
import compmake
import os
import sys
import traceback
import warnings
  
description = """  """



def main():
#    np.seterr(all='raise')
    
    parser = OptionParser(usage=description)
    parser.add_option("--db", help="Main data directory")
    parser.add_option("--outdir", help="Output directory for reports")
    parser.add_option("--datadir", help="Output directory for compmake files")
    parser.add_option("--version", help="Table version ('kf' or 'smooth')")
    parser.add_option("--group", help="Sample group", default='nopost')
    
    parser.add_option("--ncells_distance", type='int', default=20,
                      help="Discretization for distance")
    parser.add_option("--ncells_axis_angle", type='int', default=36,
                      help="Discretization for axis angle")
    parser.add_option("--compmake_command", default=None,
                      help="Execute the CompMake command and exit.")
    (options, args) = parser.parse_args() #@UnusedVariable
    
    try:
        if args:
            raise Exception('Spurious arguments %r.' % args)
    
        def missing(x): raise Exception('Please provide --%s option.' % x)
        
        if not options.db: missing('db')
        if not options.outdir:  missing('outdir')
        if not options.datadir: missing('datadir') 
        if not options.version: missing('version') 
        
    except Exception as e:
        logger.error('Error while parsing configuration.')
        logger.error(str(e))
        sys.exit(-1)
  
    try:
        confid = '%s-%s-D%d-A%d' % (options.group,
                                       options.version,
                                       options.ncells_distance,
                                       options.ncells_axis_angle)
        
        compmake_dir = os.path.join(options.datadir, confid)
        use_filesystem(compmake_dir)
        
          
        bin_enlarge_dist = 0.05
        bin_enlarge_angle = 10
        min_distance = 0.15
        
        cells = DACells(
                    ncells_distance=options.ncells_distance,
                    ncells_axis_angle=options.ncells_axis_angle,
                    arena_radius=1, min_distance=min_distance,
                    bin_enlarge_angle=bin_enlarge_angle,
                    bin_enlarge_dist=bin_enlarge_dist)
        
        stats = comp(get_group_density_stats,
                     options.db, options.group, options.version,
                     cells)
          
        saccades = comp(get_saccades_for_group,
                        options.db, options.group, options.version)
        saccades_stats = comp(compute_histogram_saccades, saccades, cells)
        
        
        joint_stats = comp(compute_joint_statistics, stats, saccades_stats)
        joint_stats = comp(compute_visual_stimulus, joint_stats)
        
        report = comp(report_stats, confid, stats, saccades_stats)
        rd = os.path.join(options.outdir, 'images')
        html = os.path.join(options.outdir, "%s.html" % confid)
        comp(write_report, report, html, rd)
        
        report_m = comp(report_models_choice, confid, joint_stats)        
        html = os.path.join(options.outdir, "%s_models.html" % confid)
        comp(write_report, report_m, html, rd)
        
        report_s = comp(report_visual_stimulus, confid, joint_stats,
                        job_id='report_stimulus')        
        html = os.path.join(options.outdir, "%s_stimulus.html" % confid)
        comp(write_report, report_s, html, rd,
             job_id='report_stimulus-write')
        
        report_i = comp(report_intuitive, confid, joint_stats,
                               job_id='report_intuitive')        
        html = os.path.join(options.outdir, "%s_intuitive.html" % confid)
        comp(write_report, report_i, html, rd,
             job_id='report_intuitive-write')
             
        if options.compmake_command is not None:
            compmake.batch_command(options.compmake_command)
        else:
            compmake_console()

    except Exception as e:
        logger.error('Error while processing. Exception and traceback follow.')
        logger.error(str(e))
        logger.error(traceback.format_exc())
        sys.exit(-2) 
    

def write_report(report, html, rd):
    print('Writing to %r.' % html)
    report.to_html(html, resources_dir=rd)

def get_group_density_stats(flydra_db_directory, db_group, version, cells): 
    with safe_flydra_db_open(flydra_db_directory) as db:
        rows = db.get_table_for_group(db_group, table='rows', version=version)
        print('Read %d rows' % len(rows))
    
        print('Computing extra information')
        warnings.warn('Using hardcoded arena size and position.')
        rowsp = add_position_information_to_rows(rows)
        
        print('Computing histogram')
        stats = compute_histogram(rowsp, cells)
        return stats


def get_saccades_for_group(flydra_db_directory, db_group, version):
    
    with safe_flydra_db_open(flydra_db_directory) as db:
        
        saccades = db.get_table_for_group(group=db_group,
                                          table='saccades',
                                          version=version)
        if len(saccades) == 0:
            raise Exception('No saccades found for group %r.' % db_group)
        
        for s in saccades:
            check_saccade_is_well_formed(s)
        
        warnings.warn('Using hardcoded arena size and position.')
        saccades = add_position_information(saccades) # XXX: using default arena size
       
        return saccades
