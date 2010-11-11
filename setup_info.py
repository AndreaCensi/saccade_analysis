
scripts = [
    ('sac_plot_xy', 'saccade_analysis.hollywood.plot_xy_direction'),
 #   ('sac_sequence_analysis','saccade_analysis.analysis201009.sequence_analysis'),
 #   ('sac_levy_analysis','saccade_analysis.analysis201009.levy_analysis'),
    ('sac_tammero_analysis', 'saccade_analysis.tammero.tammero_analysis'),
    ('sac_peter2ros', 'expdb.peter2ros'),
    ('sac_db_stats', 'expdb.db_stats'),
    ('sac_master_plot', 'saccade_analysis.analysis201009.master_plot'),
]

# this is the format for setuptools
console_scripts = map(lambda s: '%s = %s:main' % (s[0], s[1]), scripts)