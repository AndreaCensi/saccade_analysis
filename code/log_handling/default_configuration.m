function configuration = default_configuration()
% function configuration = default_configuration()
%
%  Return the default parameters

 	configuration.id = 'default';
	configuration.lambda = .0000005; % .000001
	configuration.saccade_detection_method = 'l1tf';
	configuration.min_significant_amplitude = 5;