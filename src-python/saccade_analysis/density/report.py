from . import (DACells, logger, compute_histogram, compute_histogram_saccades,
    compute_joint_statistics, report_models_choice, report_stats,
    report_visual_stimulus, compute_visual_stimulus, report_intuitive,
    ParamsEstimation, report_saccades, PlotParams, report_traj)
from ..tammero.tammero_analysis import (add_position_information,
    add_position_information_to_rows) # XXX: remove
from ..utils import (LenientOptionParser, check_no_spurious, check_mandatory,
    wrap_script_entry_point)
from compmake import use_filesystem, comp, compmake_console
from flydra_db import safe_flydra_db_open
from geometric_saccade_detector import (
    check_saccade_is_well_formed) # TODO: remove
from reprep import MIME_PDF, RepRepDefaults
import compmake
import os
import warnings
  
  
description = """  """

def report_main(args):
#    np.seterr(all='raise')
    
    parser = LenientOptionParser(usage=description)
    parser.add_option("--db", help="Main data directory")
    parser.add_option("--outdir", help="Output directory for reports")
    parser.add_option("--datadir", help="Output directory for compmake files")
    parser.add_option("--version_rows",
                      help="Table version ('kf' or 'smooth')")
    parser.add_option("--version_saccades",
                      help="Table version ('kf', 'smooth', 'angvel')")
    parser.add_option("--group", help="Sample group", default='nopost')
    
    parser.add_option("--ncells_distance", type='int', default=20,
                      help="Discretization for distance")
    parser.add_option("--ncells_axis_angle", type='int', default=36,
                      help="Discretization for axis angle")
    parser.add_option("--compmake_command", default=None,
                      help="Execute the CompMake command and exit.")
    
    parser.add_option("--pdf", default=False, action='store_true',
                      help="Uses PDF for the reports (slower).")
    
    (options, args) = parser.parse_args(args) #@UnusedVariable
    
    check_no_spurious(args)
    check_mandatory(options,
                    ['db', 'outdir', 'datadir',
                     'version_rows', 'version_saccades'])


    
    if options.pdf:
        logger.info('Using PDF for plots.')
        RepRepDefaults.default_image_format = MIME_PDF
                
    PlotParams.init_matplotlib()
    
    confid = '%s-%s-%s-D%d-A%d' % (options.group,
                                   options.version_rows,
                                   options.version_saccades,
                                   options.ncells_distance,
                                   options.ncells_axis_angle)
    
    compmake_dir = os.path.join(options.datadir, confid)
    use_filesystem(compmake_dir)
    logger.info('Storing computation in %r.' % compmake_dir)
      
    
    
    arena_radius = ParamsEstimation.arena_radius
    warnings.warn('Using hardcoded arena radius %s.' % arena_radius)
    
    cells = DACells(
                ncells_distance=options.ncells_distance,
                ncells_axis_angle=options.ncells_axis_angle,
                arena_radius=arena_radius,
                min_distance=ParamsEstimation.min_distance,
                bin_enlarge_angle=ParamsEstimation.bin_enlarge_angle,
                bin_enlarge_dist=ParamsEstimation.bin_enlarge_dist)
    
    stats = comp(get_group_density_stats,
                 options.db, options.group, options.version_rows,
                 cells)
      
    saccades = comp(get_saccades_for_group,
                    options.db, options.group, options.version_saccades)
    saccades_stats = comp(compute_histogram_saccades, saccades, cells)
    
    
    joint_stats = comp(compute_joint_statistics, stats, saccades_stats)
    joint_stats = comp(compute_visual_stimulus, joint_stats)
    
    report = comp(report_stats, confid, stats, saccades_stats)
    rd = os.path.join(options.outdir, 'images')
    html = os.path.join(options.outdir, "%s.html" % confid)
    comp(write_report, report, html, rd,
         job_id='report_stats-write')
    
    report_m = comp(report_models_choice, confid, joint_stats)        
    html = os.path.join(options.outdir, "%s_models.html" % confid)
    comp(write_report, report_m, html, rd,
         job_id='report_models_choice-write')
    
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
    
    comp(write_report, comp(report_saccades, confid, saccades,
        job_id='report_saccades'),
          html=os.path.join(options.outdir, "%s_saccades.html" % confid),
          rd=rd, job_id='report_saccades-write')

    comp(write_report, comp(report_traj, confid,
                            options.db, options.group, options.version_rows,
                            job_id='report_traj'),
          html=os.path.join(options.outdir, "%s_traj.html" % confid),
          rd=rd, job_id='report_traj-write')

    if options.compmake_command is not None:
        compmake.batch_command(options.compmake_command)
    else:
        compmake_console()



def main():
    wrap_script_entry_point(report_main, logger)
    
if __name__ == '__main__':
    main()
    
    
def write_report(report, html, rd):
    print('Writing to %r.' % html)
    
    # add_extensive_version_info(report) # TODO
    report.to_html(html, resources_dir=rd)

def get_group_density_stats(flydra_db_directory, db_group, version, cells):
    center = ParamsEstimation.arena_center
    radius = ParamsEstimation.arena_radius 
    warnings.warn('Using hardcoded arena size and position (%s, %s)' 
                    % (center, radius))
    with safe_flydra_db_open(flydra_db_directory) as db:
        rows = db.get_table_for_group(db_group, table='rows', version=version)
        print('Read %d rows' % len(rows))
    
        print('Computing extra information')

        rowsp = add_position_information_to_rows(rows,
                                                 arena_radius=radius,
                                                 arena_center=center)
        
        print('Computing histogram')
        stats = compute_histogram(rowsp, cells)
        return stats

def get_saccades_for_group(flydra_db_directory, db_group, version):
    center = ParamsEstimation.arena_center
    radius = ParamsEstimation.arena_radius 
    warnings.warn('Using hardcoded arena size and position (%s, %s)' 
                  % (center, radius))
        
        
    with safe_flydra_db_open(flydra_db_directory) as db:

        print('Getting all saccades from group %r.' % db_group)
        saccades = db.get_table_for_group(group=db_group,
                                          table='saccades',
                                          version=version)
        if len(saccades) == 0:
            raise Exception('No saccades found for group %r.' % db_group)
        
        print('Checking saccades are well formed.')
        for s in saccades:
            check_saccade_is_well_formed(s)
        
        print('Adding position information')
        saccades = add_position_information(saccades,
                                            arena_radius=radius,
                                            arena_center=center)  
        
        return saccades


