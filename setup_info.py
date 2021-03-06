
scripts = [
    ('sac_plot_xy', 'saccade_analysis.hollywood.plot_xy_direction'),
    ('sac_tammero_analysis', 'saccade_analysis.tammero.tammero_analysis'),
    ('sac_spontaneous_analysis', 'saccade_analysis.tammero_flydradb.spontaneous'),
    
    ('sac_density_report', 'saccade_analysis.density.report'),
    # ('sac_peter2ros', 'expdb.peter2ros'),
    
    ('sac_import_peter', 'saccade_analysis.import_peter'),
    ('sac_import_matlab_andrea', 'saccade_analysis.import_matlab_andrea'),
    ('sac_import_matlab_ros', 'saccade_analysis.import_matlab_ros'),
    ('sac_export_matlab_ros', 'saccade_analysis.export_matlab_ros'),
    ('sac_choose_version', 'saccade_analysis.choose_version'),
    
    ('sac_master_plot', 'saccade_analysis.analysis201009.master_plot'),
]

# this is the format for setuptools
console_scripts = map(lambda s: '%s = %s:main' % (s[0], s[1]), scripts)
