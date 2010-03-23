function sac_distributions(saccades, out_dir)
% function sac_distributions(saccades, out_dir)
%
  	A = [saccades.amplitude];
	S = [saccades.sign];
	D = [saccades.duration];
	V = [saccades.top_velocity];
	I = [saccades.time_passed];
	orientation_start = mod([saccades.orientation_start], 360);
	orientation_stop = mod([saccades.orientation_stop], 360);
	
	
	f = figure(27);
	hist(orientation_start, 100);
	ylabel('density')
	xlabel('initial orientation (deg)')
	title('Saccade initial orientation ')
	print('-depsc2', sprintf('%s/sac_distribution_orientation_start.eps', out_dir))

	f = figure(28);
	hist(orientation_start, 100);
	ylabel('density')
	xlabel('final orientation (deg)')
	title('Saccade final orientation ')
	print('-depsc2', sprintf('%s/sac_distribution_orientation_stop.eps', out_dir))


	f = figure(25);
	hist(V, 100);
	ylabel('density')
	xlabel('saccade top angular velocity (deg/s)')
	title('Saccade velocity')
	print('-depsc2', sprintf('%s/sac_distribution_velocity.eps', out_dir))

	f = figure(26);
	hist(I, -20:0.1:1);
	ylabel('density')
	xlabel('time from previous saccade (s)')
	title('Saccade interval')
	print('-depsc2', sprintf('%s/sac_distribution_interval.eps', out_dir))

	f = figure(23);
	hist(A, 100);
	ylabel('density')
	xlabel('amplitude (degrees)')
	title('Saccade amplitude')
	print('-depsc2', sprintf('%s/sac_distribution_amplitude.eps', out_dir))

	f = figure(24);
	hist(D, 100);
	ylabel('density')
	xlabel('saccade duration (s)')
	title('Saccade duration')
	print('-depsc2', sprintf('%s/sac_distribution_duration.eps', out_dir))
	