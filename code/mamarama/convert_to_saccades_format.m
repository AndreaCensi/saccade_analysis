function res = convert_to_saccades_format(snpall, directory)
	% This function takes a big structure in the format I used for the visual mamarama analysis
	% and converts it to logs of the kind we used for the saccade analysis.
	
	sample2episodes = group_samples(snpall);
	
	for sample=1:numel(sample2episodes)
%	for sample=80
		episodes = sample2episodes{sample};
		
		filename = snpall.episode_data{episodes(1)}.fh5_filename;
		stim = snpall.episode_data{episodes(1)}.stim_fname;
		stim = stim(1:(numel(stim)-4));
		
		fprintf('Sample %d / %d  %s %s \n', sample, numel(sample2episodes), filename, stim);
	
		x =[]; y=[];
		theta = [];
		for episode=episodes
			interval = find(snpall.episode_id == episode);
			if numel(interval) < 10
				continue
			end

			timestamp = snpall.time(interval);
			x_ep = snpall.position(interval,1);
			y_ep = snpall.position(interval,2);

			% sigma = 0;
			% filter_g = fspecial('gaussian', [1 ceil(sigma*6)], sigma);
			% xf = conv_pad(x_ep, filter_g);
			% yf = conv_pad(y_ep, filter_g);
			xf=x_ep;
			yf=y_ep;

			zone=3;
			sigma=2;
			[theta_episode, choice_ep] = line_filter(timestamp, xf,yf,sigma,zone);

			theta = [theta theta_episode];
			x = [x x_ep'];
			y = [y y_ep'];
		end
		if numel(theta) < 100
			continue
		end
		theta = theta_unwrap(theta);
		
		data.species = 'Dmelanogaster';
		data.sample = filename;
		data.stim = stim;
		dt = timestamp(2)-timestamp(1);
		data.exp_timestamps = (0:numel(theta)-1) * dt;
		% Rose uses degrees instead of radians
		data.exp_orientation = rad2deg(theta);

		species = sprintf('mamarama%s', stim);
		id = filename(5:(numel(filename)-4));
		basename = sprintf('data_%s.mat', id);
		species_dir = path_join(directory, species);
		if ~exist(species_dir)
			mkdir(directory, species)
		end
		mat_filename = path_join(species_dir, basename);
		fprintf('Writing on %s \n', mat_filename);
		save(mat_filename, 'data');
		
		if false
			figure
			plot_with_arrows(x,y,theta);
			axis('equal')
			title('orientation')
		end

		if false
			figure;
			t=1:numel(theta);
			x = cos(theta) .* t;
			y = sin(theta) .* t;
			plot(x,y,'-')
		end
		
%		figure;
%		t=(1:numel(theta)) / 60;
%		plot(t,theta)
%		pause
		
		
	end
	
	
	
	

	
function s = detect_saccades(s)
	% function snpall = snp002_detect_saccades(snpall)
	%   Computes saccades statistics

	angular_velocity_threshold = 5;

	f = fspecial('gaussian',10,2);
	s.reduced_angular_velocity_smooth = filter2(f, s.reduced_angular_velocity);
	s.reduced_angular_acceleration_smooth = diff(s.reduced_angular_velocity_smooth);

	s.sac_maxima = extrema(s.reduced_angular_velocity_smooth);
	candidates = abs(s.sac_maxima)>0;
	fast_enough = (abs(s.reduced_angular_velocity_smooth) > angular_velocity_threshold) & ...
		(s.linear_velocity_modulus > 0.02);

	s.sac_detect = candidates & fast_enough;
	s.sac_signs = s.sac_maxima(s.sac_detect);	

	s.sac_letters( s.sac_signs < 0) = 'R';
	s.sac_letters( s.sac_signs > 0) = 'L';

	s.saccades_moments = find(s.sac_detect);

	s.saccades_intervals = s.saccades_moments(2:end) - s.saccades_moments(1:end-1);

	if 0
		figure; hold on;
	%	plot(s.reduced_angular_velocity, 'k-')
		plot(s.reduced_angular_velocity_smooth, 'b-')
		a=axis;
		plot([a(1) a(2)], [1 1]*angular_velocity_threshold, 'k--')
	end