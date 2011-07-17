import sys, os, numpy as np, traceback
from optparse import OptionParser

from reprep import Report
from compmake import use_filesystem, comp, compmake_console 
from flydra_db import safe_flydra_db_open 
 
from .report_axis_angle import create_report_axis_angle
from .load_data import get_saccades

description = """ Creates figures similar to Tammero. """

from . import logger

def main():
    np.seterr(all='raise')
    
    parser = OptionParser(usage=description)
    parser.add_option("--db", help="Main data directory")
    
    parser.add_option("--interactive", action="store_true", default=False,
                      help="Starts an interactive compmake session.")
    
    parser.add_option("--outdir", help="Output directory")
    
        
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
        
        with safe_flydra_db_open(options.db) as db:
            spontaneous_analysis(db, options.outdir)
    
    
        compmake_console()
        
    except Exception as e:
        logger.error('Error while processing. Exception and traceback follow.')
        logger.error(str(e))
        logger.error(traceback.format_exc())
        sys.exit(-2)
        
        
def spontaneous_analysis(db, outdir):
    
    groups = {
        'posts':  dict(db_group='posts'),
        'noposts': dict(db_group='nopost'),
    }
    
    which = {
        'all':                dict(d_min=0, d_max=1, desc='All saccades'),
        'close_to_the_wall':  dict(d_min=0, d_max=0.5,
                                   desc='Close to the wall (<0.5m)'),
        'far_from_the_wall':  dict(d_min=0.5, d_max=1,
                                   desc='Far from the wall (>0.5m)'),
        'wdistance_00cm_to_50cm':  dict(d_min=0, d_max=0.5),
        'wdistance_00cm_to_40cm':  dict(d_min=0, d_max=0.4),
        'wdistance_00cm_to_30cm':  dict(d_min=0, d_max=0.3),
        'wdistance_00cm_to_20cm':  dict(d_min=0, d_max=0.2),
        'wdistance_90cm_to_100cm':  dict(d_min=0.90, d_max=1),
        'wdistance_80cm_to_100cm':  dict(d_min=0.80, d_max=1),
        'wdistance_75cm_to_100cm':  dict(d_min=0.75, d_max=1),
        'wdistance_70cm_to_100cm':  dict(d_min=0.70, d_max=1),
        'wdistance_65cm_to_100cm':  dict(d_min=0.65, d_max=1),
        'wdistance_60cm_to_100cm':  dict(d_min=0.60, d_max=1),
        'wdistance_55cm_to_100cm':  dict(d_min=0.55, d_max=1),
        'wdistance_50cm_to_100cm':  dict(d_min=0.50, d_max=1),
        'wdistance_45cm_to_100cm':  dict(d_min=0.45, d_max=1),
        'wdistance_40cm_to_100cm':  dict(d_min=0.40, d_max=1),
        'wdistance_30cm_to_100cm':  dict(d_min=0.30, d_max=1),
        'wdistance_20cm_to_100cm':  dict(d_min=0.20, d_max=1),
    }
    
    for group_id, group_attr in groups.items():
        for section_id, section_attrs in which.items():
            combination_id = '%s-%s' % (group_id, section_id)
            db_group = group_attr['db_group']
            d_interval = (section_attrs['d_min'], section_attrs['d_max'])
         
            saccades = comp(get_saccades, db.directory, db_group, d_interval,
                            job_id='%s-saccades' % combination_id)
            comp(create_report, outdir, combination_id, saccades,
                            job_id='%s-report' % combination_id)
        

def create_report(outdir, combination_id, saccades):
    r = Report(combination_id)
    
    stats = 'Combination %r has %d saccades' % (combination_id, len(saccades))
    r.text('stats', stats)
    
    desc = ""
    #r.add_child(create_report_subset(combination_id,desc, saccades))
    #r.add_child(create_report_randomness(combination_id, desc, saccades))
    r.add_child(create_report_axis_angle(combination_id, desc, saccades))

    
    rd = os.path.join(outdir, 'images')
    out = os.path.join(outdir, 'combinations', '%s.html' % combination_id)
    print('Writing to %r' % out)
    r.to_html(out, resources_dir=rd)
    
    
    
    
