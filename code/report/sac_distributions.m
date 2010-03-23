function sac_distributions(saccades, out_dir)
% function sac_distributions(saccades, out_dir)
%
  	A = [saccades.amplitude];
	S = [saccades.sign];
	D = [saccades.duration];
	V = [saccades.top_velocity];

	f = figure(25);
	hist(V, 100);
	ylabel('density')
	xlabel('saccade top angular velocity (deg/s)')
	title('Saccade velocity')
	print('-depsc2', sprintf('%s/sac_distribution_velocity.eps', out_dir))

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
	