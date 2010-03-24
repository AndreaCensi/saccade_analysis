function sac_distributions(saccades, out_dir)
% function sac_distributions(saccades, out_dir)
%
	
	nv=1;
	vars(nv).id = 'amplitude';
	vars(nv).interesting = [0 400];
	vars(nv).name = 'Amplitude';
	vars(nv).values = [saccades.amplitude];
	vars(nv).unit = 'deg';

	nv=nv+1;
	vars(nv).id = 'duration';
	vars(nv).interesting = [0 0.3];
	vars(nv).name = 'Duration';
	vars(nv).values = [saccades.duration];
	vars(nv).unit = 's';
	
	nv=nv+1;
	vars(nv).id = 'top_velocity';
	vars(nv).interesting = [0 2000];
	vars(nv).name = 'Top angular velocity';
	vars(nv).values = [saccades.top_velocity];
	vars(nv).unit = 'deg/s';

	nv=nv+1;
	vars(nv).id = 'interval';
	vars(nv).interesting = [0 8];
	vars(nv).name = 'Interval';
	vars(nv).values = [saccades.time_passed];
	vars(nv).unit = 's';

	nv=nv+1;
	vars(nv).id = 'initial_orientation';
	vars(nv).interesting = [];
	vars(nv).name = 'Initial orientation';
	vars(nv).values = mod([saccades.orientation_start], 360);
	vars(nv).unit = 'deg';

	nv=nv+1;
	vars(nv).id = 'final_orientation';
	vars(nv).interesting = [];
	vars(nv).name = 'Final orientation';
	vars(nv).values = mod([saccades.orientation_stop], 360);
	vars(nv).unit = 'deg';

	nv=nv+1;
	vars(nv).id = 'amplitudeL';
	vars(nv).name = 'Previous amplitude';
	vars(nv).interesting = [0 400];
	x = [saccades.amplitude];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 'deg';

	nv=nv+1;
	vars(nv).id = 'durationL';
	vars(nv).name = 'Previous duration';
	vars(nv).interesting = [0 0.3];
	x = [saccades.duration];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 's';

	nv=nv+1;
	vars(nv).id = 'top_velocityL';
	vars(nv).name = 'Previous top velocity';
	vars(nv).interesting = [0 2000];
	x = [saccades.top_velocity];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 'deg/s';

	nv=nv+1;
	vars(nv).id = 'intervalL';
	vars(nv).name = 'Previous interval';
	vars(nv).interesting = [0 8];
	x = [saccades.time_passed];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 's';

	for i=1:numel(vars)
		vars(i).is_delayed = numel(strfind(vars(i).id, 'L'))>0;
	end
	
	for i=1:numel(vars)
		% do not create histogram for delayed variables
		if not(vars(i).is_delayed)
			create_dist_plots(vars(i), out_dir)
		end
	end
	
	for i=1:numel(vars)
		for j=1:(i-1)
			% skip if both are delayed
			if not(vars(i).is_delayed & vars(j).is_delayed)
				create_joint_plots(vars(i), vars(j), out_dir)
			end
		end
	end
	
function create_dist_plots(var1, out_dir)
	f = figure;
	hist(var1.values, 360);
	ylabel('density')
	xlabel(sprintf('%s (%s)', var1.name, var1.unit))
	title(sprintf('Distribution of %s ', var1.name))
	print('-depsc2', sprintf('%s/sac_dist-%s.eps', out_dir, var1.id))
	close(f)
	
	if numel(var1.interesting) > 0
	
	f = figure;
	from = var1.interesting(1);
	to = var1.interesting(2);
	nbins = 1000;
	assert(from<to);
	bins = from:((to-from)/nbins):to;
	hist(var1.values, bins);
	a=axis(); a(1)=from; a(2)=to;
	ylabel('density')
	xlabel(sprintf('%s (%s)', var1.name, var1.unit))
	title(sprintf('Distribution of %s (detail in %f - %f)', var1.name, from, to))
	print('-depsc2', sprintf('%s/sac_dist-%s_detail.eps', out_dir, var1.id))
	close(f)
		
	end
	
function create_joint_plots(var1, var2, out_dir)
	f = figure;
	h = plot(var1.values, var2.values, 'k.');
	set(h, 'MarkerSize', 0.1);
	xlabel(sprintf('%s (%s)', var1.name, var1.unit))
	ylabel(sprintf('%s (%s)', var2.name, var2.unit))
	title(sprintf('Joint distribution of %s / %s ', var1.name, var2.name))
	
	print('-depsc2', sprintf('%s/sac_joint-%s-%s.eps', out_dir, var1.id, var2.id))
	close(f)
	
	
	
	
	