
if not(exist('saccade_data', 'dir'))
   error('I expect to see a directory named "saccade_data"') 
end

% Peter's data

peters_conf = struct;
peters_conf.id = 'peters_conf';
% peters_conf.id = 'use_for_report';
peters_conf.saccade_detection_method = 'linear';
peters_conf.smooth_steps = 3;
peters_conf.filtered_velocity_significant_threshold = 75;
peters_conf.filtered_velocity_zero_threshold = 7.5;
peters_conf.min_significant_amplitude = 15;
peters_conf.robust_amplitude_delta = 0.1;
peters_conf.debug = false;

process_species('saccade_data/indoorhalogen', peters_conf);
process_species('saccade_data/blueFilter', peters_conf);
process_species('saccade_data/circularPolarizer', peters_conf);
process_species('saccade_data/circularPolarizercloudy', peters_conf);
process_species('saccade_data/grayFilter', peters_conf);
process_species('saccade_data/grayFiltercloudy', peters_conf);
process_species('saccade_data/indoorhalogen', peters_conf);
process_species('saccade_data/noFilter', peters_conf);
process_species('saccade_data/noFiltercloudy', peters_conf);

% various configurations for other data
master = struct;
master.id = 'tmp_conf';
master.saccade_detection_method = 'linear';
master.smooth_steps = 3;
master.filtered_velocity_significant_threshold = 50;
master.filtered_velocity_zero_threshold = 15;
master.min_significant_amplitude = 5;
master.robust_amplitude_delta = 0.1;
master.debug = false;

significant_threshold = 25:5:100;

clear configurations
for i=1:numel(significant_threshold)
	configurations(i) = master;
	configurations(i).filtered_velocity_significant_threshold = significant_threshold(i);
	configurations(i).id = sprintf('threshold%d', i);
end

for i=1:numel(configurations)
    conf = configurations(i)
    process_species('saccade_data/Dananassae', conf);
    process_species('saccade_data/Darizonae', conf);
    process_species('saccade_data/Dhydei', conf);
    process_species('saccade_data/Dmelanogaster', conf);
    process_species('saccade_data/Dmojavensis', conf);
    process_species('saccade_data/Dpseudoobscura', conf);
end

% TODO: check for mamaramaposts, noposts

