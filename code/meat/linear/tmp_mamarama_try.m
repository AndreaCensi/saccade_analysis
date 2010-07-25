tmp_conf = struct;
tmp_conf.id = 'tmp_conf';
tmp_conf.saccade_detection_method = 'linear';
tmp_conf.smooth_steps = 3;
%tmp_conf.filtered_velocity_significant_threshold = 50;
tmp_conf.filtered_velocity_significant_threshold = 80;
%tmp_conf.filtered_velocity_zero_threshold = 15;
tmp_conf.filtered_velocity_zero_threshold = 30;
tmp_conf.min_significant_amplitude = 30;
tmp_conf.robust_amplitude_delta = 0.1;
tmp_conf.debug = 0;

process_species('data/mamaramanopost', tmp_conf);
r=roc_analysis_species_conf('data/mamaramanopost', tmp_conf.id, false)

r=roc_analysis_species_conf('data/mamaramanopost', tmp_conf.id, true)


return

significant_threshold = 25:5:100;

clear configurations 
for i=1:numel(significant_threshold)
	configurations(i) = tmp_conf;
	configurations(i).filtered_velocity_significant_threshold = significant_threshold(i);
	configurations(i).id = sprintf('threshold%d', i);
end

for i=1:numel(configurations)
process_species('data/mamaramanopost', configurations(i))
end

r = roc_analysis_species('data/mamaramanopost')
roc_analysis_species_conf('data/mamaramanopost', configurations(1).id, true)