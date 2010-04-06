function sac_distributions(saccades, out_dir)
% function sac_distributions(saccades, out_dir)
%
	
	nv=1;
	vars(nv).id = 'amplitude';
	vars(nv).interesting = [1 200];
	vars(nv).name = 'Amplitude';
	vars(nv).values = [saccades.amplitude];
	vars(nv).unit = 'deg';
	vars(nv).density_max_y = 0.06;
	vars(nv).density_bins = 100;

	nv=nv+1;
	vars(nv).id = 'duration';
	vars(nv).interesting = [0.01 0.3];
	vars(nv).name = 'Duration';
	vars(nv).values = [saccades.duration];
	vars(nv).unit = 's';
	vars(nv).density_max_y = 40;
	vars(nv).density_bins = 100;
	
	
	nv=nv+1;
	vars(nv).id = 'top_velocity';
	vars(nv).interesting = [10 2000];
	vars(nv).name = 'Top angular velocity';
	vars(nv).values = [saccades.top_velocity];
	vars(nv).unit = 'deg/s';
	vars(nv).density_max_y = 3 * 1e-3;
	vars(nv).density_bins = 100;
	

	nv=nv+1;
	vars(nv).id = 'interval';
	vars(nv).interesting = [0.01 8];
	vars(nv).name = 'Interval';
	vars(nv).values = [saccades.time_passed];
	vars(nv).unit = 's';
	vars(nv).density_max_y = 1.1;
	vars(nv).density_bins = 100;
	

	nv=nv+1;
	vars(nv).id = 'initial_orientation';
	vars(nv).interesting = [0, 360];
	vars(nv).name = 'Initial orientation';
	vars(nv).values = mod([saccades.orientation_start], 360);
	vars(nv).unit = 'deg';

	nv=nv+1;
	vars(nv).id = 'final_orientation';
	vars(nv).interesting = [0, 360];
	vars(nv).name = 'Final orientation';
	vars(nv).values = mod([saccades.orientation_stop], 360);
	vars(nv).unit = 'deg';
% 
% 	nv=nv+1;
% 	vars(nv).id = 'time_start';
% 	vars(nv).name = 'Time from log start';
% %	vars(nv).interesting = [0 400];
% 	vars(nv).values = [saccades.time_start];
% 	vars(nv).unit = 's';

	nv=nv+1;
	vars(nv).id = 'amplitudeL';
	vars(nv).name = 'Previous amplitude';
	vars(nv).interesting = [1 200];
	x = [saccades.amplitude];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 'deg';

	nv=nv+1;
	vars(nv).id = 'durationL';
	vars(nv).name = 'Previous duration';
	vars(nv).interesting = [0.01 0.3];
	x = [saccades.duration];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 's';

	nv=nv+1;
	vars(nv).id = 'top_velocityL';
	vars(nv).name = 'Previous top velocity';
	vars(nv).interesting = [10 2000];
	x = [saccades.top_velocity];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 'deg/s';

	nv=nv+1;
	vars(nv).id = 'intervalL';
	vars(nv).name = 'Previous interval';
	vars(nv).interesting = [0.01 8];
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
			create_dist_plots(vars(i), out_dir);
			create_xcorr_plots(vars(i), out_dir);
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

function create_xcorr_plots(var1, out_dir)
	basename=sprintf('sac_xcorr-%s', var1.id);
	if ~report_should_I_skip(out_dir, basename)	
		f = sac_figure;
		x = [var1.values];
		x = x(not(isnan(x)));
		x = x - mean(x);
		maxlag = 20;
		[S_xcorr, lags] = xcorr(x, maxlag, 'coeff');
		plot(lags, S_xcorr, 'kx-');
		ylabel('Autocorrelation')
		xlabel(sprintf('distance in saccade sequence'))
		axis([-maxlag +maxlag -0.5 1])
		ftitle=sprintf('Autocorrelation of %s ', var1.name);
		sac_print(out_dir, basename, ftitle);
		close(f)
	end

	
function create_dist_plots(var1, out_dir)
	basename=sprintf('sac_dist-%s_all', var1.id);
	if ~report_should_I_skip(out_dir, basename)	
		f = sac_figure;
		hist(var1.values, 360);
		ylabel('density')
		xlabel(sprintf('%s (%s)', var1.name, var1.unit))
		ftitle=sprintf('Distribution of %s ', var1.name);
		sac_print(out_dir, basename, ftitle);
		close(f)
	end
	
	if (var1.interesting(1)>0)
	basename=sprintf('sac_dist-%s_cdf', var1.id);
	if ~report_should_I_skip(out_dir, basename)	
		f = sac_figure;
		[ycdf, xcdf] = cdfcalc(var1.values);
		semilogx(xcdf, ycdf(1:(end-1)), '-')
		m = var1.interesting(2)*10;
		axis([var1.interesting(1) m 0 1])
%		cdfplot(var1.values);
		ylabel('cdf')
		xlabel(sprintf('%s (%s)', var1.name, var1.unit))
		ftitle=sprintf('CDF of %s ', var1.name);
		sac_print(out_dir, basename, ftitle);
		close(f)
	end
	end
	
	if numel(var1.interesting) > 0
	basename=sprintf('sac_dist-%s', var1.id);
	if ~report_should_I_skip(out_dir, basename)	
		f = sac_figure;
		from = var1.interesting(1);
		to = var1.interesting(2);
		if isfield(var1, 'density_bins') && (numel(var1.density_bins) > 0)
			nbins = var1.density_bins;
		else
			nbins = 100;
		end
		[pdf, bins, fraction_excluded] = compute_pdf(var1.values, [from to], nbins);
		plot(bins, pdf, 'b-');
		a=axis(); a(1)=from; a(2)=to;
	%	text(a(1), a(4), sprintf('Excluded: %f', fraction_excluded))
		if isfield(var1,'density_max_y') && (numel(var1.density_max_y) > 0)
			a = axis();
			a(4) = var1.density_max_y;
			axis(a);
		end
		ylabel('density')
		xlabel(sprintf('%s (%s)', var1.name, var1.unit))
		ftitle=sprintf('Distribution of %s', var1.name);
%		ftitle=sprintf('Distribution of %s (detail in %f - %f)', var1.name, from, to);
		sac_print(out_dir, basename, ftitle);
		close(f)
	end
	end
	
function create_joint_plots(var1, var2, out_dir)
	if false
	basename=sprintf('sac_joint-%s-%s', var1.id, var2.id);
	if ~report_should_I_skip(out_dir, basename)	
		f = sac_figure;
		h = plot(var1.values, var2.values, 'k.');
		set(h, 'MarkerSize', 0.1);
		xlabel(sprintf('%s (%s)', var1.name, var1.unit))
		ylabel(sprintf('%s (%s)', var2.name, var2.unit))
		a=axis;
		if numel(var1.interesting) == 2
			a(1) = var1.interesting(1);
			a(2) = var1.interesting(2);
		end
		if numel(var2.interesting) == 2
			a(3) = var2.interesting(1);
			a(4) = var2.interesting(2);
		end
		axis(a);
		
		ftitle = sprintf('Joint distribution of %s / %s ', var1.name, var2.name);
		sac_print(out_dir, basename, ftitle);
		close(f)
	end
	end
	
	if (var1.interesting(1)>0) && (var2.interesting(1)>0)
	basename=sprintf('sac_joint-%s-%s_log', var1.id, var2.id);
	if ~report_should_I_skip(out_dir, basename)	
		f = sac_figure;
		
		x_interval = [var1.interesting(1) var1.interesting(2) * 5];
		y_interval = [var2.interesting(1) var2.interesting(2) * 5];
		
		plot_log_hist3(var1.values',var2.values',x_interval, y_interval, 50, 50);
		
		xlabel(sprintf('%s (%s)', var1.name, var1.unit))
		ylabel(sprintf('%s (%s)', var2.name, var2.unit))
		% a=axis;
		% if numel(var1.interesting) == 2
		% 	a(1) = var1.interesting(1);
		% 	a(2) = var1.interesting(2) * 10;
		% end
		% if numel(var2.interesting) == 2
		% 	a(3) = var2.interesting(1);
		% 	a(4) = var2.interesting(2) * 10;
		% end
		% axis(a);
		
		ftitle = sprintf('Joint distribution of %s / %s ', var1.name, var2.name);
		sac_print(out_dir, basename, ftitle);
		close(f)
	end
	end

	basename=sprintf('sac_joint-%s-%s', var1.id, var2.id);
	if ~report_should_I_skip(out_dir, basename)	
		f = sac_figure;
		
		valid = not(isnan(var1.values)) & not(isnan(var2.values));
		if numel(var1.interesting) == 2
			valid = valid & (var1.values >= var1.interesting(1));
			valid = valid & (var1.values <= var1.interesting(2));
		end
		if numel(var2.interesting) == 2
			valid = valid & (var2.values >= var2.interesting(1));
			valid = valid & (var2.values <= var2.interesting(2));
		end
		x = var1.values(valid);
		y = var2.values(valid);
		
		[N,C] = hist3([x' y'], [50 50]);
		cx=C{1}; cy=C{2};
		
		w=max(cx)-min(cx);
		h=max(cy)-min(cy);
		t=100;
		w=0;h=0;
		a=[min(cx)-w/t max(cx)+w/t min(cy)-h/t max(cy)+h/t];
		axis(a)
		h=plot(a(1),a(3),'.');
		set(h,'MarkerSize',0.001);
		hold on;
		imagesc(cx, cy, -N');
		axis(a)
		
		xlabel(sprintf('%s (%s)', var1.name, var1.unit))
		ylabel(sprintf('%s (%s)', var2.name, var2.unit))
		colormap('bone')
		
		ftitle = sprintf('Joint distribution of %s / %s ', var1.name, var2.name);
		sac_print(out_dir, basename, ftitle);
		close(f)
	end
	
	
	
	