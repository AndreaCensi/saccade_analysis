tmp_conf = struct;
tmp_conf.id = 'tmp_conf';
tmp_conf.saccade_detection_method = 'linear';
tmp_conf.smooth_steps = 3;
tmp_conf.filtered_velocity_significant_threshold = 50;
tmp_conf.filtered_velocity_zero_threshold = 15;
tmp_conf.min_significant_amplitude = 5;
tmp_conf.robust_amplitude_delta = 0.1;
tmp_conf.debug = false;

significant_threshold = 25:5:100;

clear configurations 
for i=1:numel(significant_threshold)
	configurations(i) = tmp_conf;
	configurations(i).filtered_velocity_significant_threshold = significant_threshold(i);
	configurations(i).id = sprintf('threshold%d', i);
end
	
for i=1:numel(configurations)
    process_species('saccade_data/indoorhalogen', configurations(i));
end
