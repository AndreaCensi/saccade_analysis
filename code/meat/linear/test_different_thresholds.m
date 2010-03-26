tmp_conf = default_configuration();
tmp_conf.id = 'tmp_conf';
tmp_conf.saccade_detection_method = 'linear';

tmp_conf.smooth_steps = 3;
tmp_conf.filtered_velocity_significant_threshold = 50;
tmp_conf.filtered_velocity_zero_threshold = 15;
tmp_conf.min_significant_amplitude = 5;

significant_threshold = 25:5:100;

clear configurations 
for i=1:numel(significant_threshold)
	configurations(i) = tmp_conf;
	configurations(i).filtered_velocity_significant_threshold = significant_threshold(i);
	configurations(i).id = sprintf('threshold%d', i);
end
	
	
process_data('data', configurations);
