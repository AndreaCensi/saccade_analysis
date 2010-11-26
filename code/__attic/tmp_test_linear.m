

tmp_conf = default_configuration();
tmp_conf.id = 'tmp_conf';
tmp_conf.saccade_detection_method = 'linear';

tmp_conf.smooth_steps = 3;
tmp_conf.filtered_velocity_significant_threshold = 50;
tmp_conf.filtered_velocity_zero_threshold = 15;
tmp_conf.min_significant_amplitude = 5;

process_all_data('data/Darizonae', tmp_conf);

a = load('data/Darizonae/processed/tmp_conf/processed_data_Darizonae-20080409-173446.mat');

%detect_saccades_plot(a.res.chunk(1))

roc_analysis_species_conf('data/Darizonae', tmp_conf.id, false)
roc_analysis_species_conf('data/Darizonae', tmp_conf.id, true)