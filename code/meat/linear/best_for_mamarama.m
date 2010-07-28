tmp_conf = struct;
tmp_conf.id = 'use_for_report';
tmp_conf.saccade_detection_method = 'mamarama';
tmp_conf.debug = 0;
tmp_conf.min_significant_amplitude = 15; % deg
tmp_conf.robust_amplitude_delta = 0.05; % seconds
tmp_conf.robust_amplitude_var = 20;

% trying
% tmp_conf.min_significant_amplitude = 10; % deg

process_species('data/mamaramanopost', tmp_conf);
r=roc_analysis_species_conf('data/mamaramanopost', tmp_conf.id, false)

process_species('data/allmamarama', tmp_conf);