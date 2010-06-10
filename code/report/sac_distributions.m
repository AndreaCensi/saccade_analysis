function sac_distributions(saccades, out_dir)
% function sac_distributions(saccades, out_dir)
%
	
	nv=1;
	vars(nv).id = 'amplitude';
	vars(nv).letter = 'A';
	vars(nv).interesting = [1 200];
	vars(nv).name = 'Amplitude';
	vars(nv).values = [saccades.amplitude];
	vars(nv).unit = 'deg';
	vars(nv).density_max_y = 0.06;
	vars(nv).density_bins = 100;
	vars(nv).include_in_bigcorr = true;
	

	nv=nv+1;
	vars(nv).id = 'duration';
	vars(nv).letter = 'D';
%	vars(nv).interesting = [0.01 0.3];
	vars(nv).interesting = [0.01 0.9];
	vars(nv).name = 'Duration';
	vars(nv).values = [saccades.duration];
	vars(nv).unit = 's';
	vars(nv).density_max_y = 10;
	vars(nv).density_bins = 50;
	vars(nv).include_in_bigcorr = true;
	
	
	nv=nv+1;
	vars(nv).id = 'top_velocity';
	vars(nv).letter = 'V';
	vars(nv).interesting = [10 2000];
	vars(nv).name = 'Top angular velocity';
	vars(nv).values = [saccades.top_velocity];
	vars(nv).unit = 'deg/s';
	vars(nv).density_max_y = 3 * 1e-3;
	vars(nv).density_bins = 100;
	vars(nv).include_in_bigcorr = true;


	nv=nv+1;
	vars(nv).id = 'interval';
	vars(nv).letter = 'I';
	vars(nv).interesting = [0.01 8];
	vars(nv).name = 'Interval';
	vars(nv).values = [saccades.time_passed];
	vars(nv).unit = 's';
	vars(nv).density_max_y = 1.1;
	vars(nv).density_bins = 100;
	vars(nv).include_in_bigcorr = true;

	nv=nv+1;
	vars(nv).id = 'sign';
	vars(nv).letter = 'S';
	vars(nv).interesting = [-1.1 1.1];
	vars(nv).name = 'Sign';
	vars(nv).values = [saccades.sign];
	vars(nv).unit = '';
	vars(nv).density_max_y = 1.1;
	vars(nv).density_bins = 100;
	vars(nv).include_in_bigcorr = false;


	nv=nv+1;
	vars(nv).id = 'initial_orientation';
	vars(nv).letter = 'io';
	vars(nv).interesting = [0, 360];
	vars(nv).name = 'Initial orientation';
	vars(nv).values = mod([saccades.orientation_start], 360);
	vars(nv).unit = 'deg';
	vars(nv).include_in_bigcorr = false;

	nv=nv+1;
	vars(nv).id = 'final_orientation';
	vars(nv).letter = 'fo';
	vars(nv).interesting = [0, 360];
	vars(nv).name = 'Final orientation';
	vars(nv).values = mod([saccades.orientation_stop], 360);
	vars(nv).unit = 'deg';
	vars(nv).include_in_bigcorr = false;
% 
% 	nv=nv+1;
% 	vars(nv).id = 'time_start';
% 	vars(nv).name = 'Time from log start';
% %	vars(nv).interesting = [0 400];
% 	vars(nv).values = [saccades.time_start];
% 	vars(nv).unit = 's';

	nv=nv+1;
	vars(nv).id = 'amplitudeL';
	vars(nv).letter = 'pA';	
	vars(nv).name = 'Previous amplitude';
	vars(nv).interesting = [1 200];
	x = [saccades.amplitude];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 'deg';
	vars(nv).include_in_bigcorr = true;
	

	nv=nv+1;
	vars(nv).id = 'durationL';
	vars(nv).letter = 'pD';
	vars(nv).name = 'Previous duration';
	vars(nv).interesting = [0.01 0.3];
	x = [saccades.duration];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 's';
	vars(nv).include_in_bigcorr = true;

	nv=nv+1;
	vars(nv).id = 'top_velocityL';
	vars(nv).letter = 'pV';
	vars(nv).name = 'Previous top velocity';
	vars(nv).interesting = [10 2000];
	x = [saccades.top_velocity];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 'deg/s';
	vars(nv).include_in_bigcorr = true;
	

	nv=nv+1;
	vars(nv).id = 'intervalL';
	vars(nv).letter = 'pI';
	vars(nv).name = 'Previous interval';
	vars(nv).interesting = [0.01 8];
	x = [saccades.time_passed];
	y = [nan x(1:end-1)];
	vars(nv).values = y;
	vars(nv).unit = 's';
	vars(nv).include_in_bigcorr = true;

    sac_temporal_correlation(saccades, vars(1:4), out_dir);

	create_joint_plots_by_sample(saccades, vars(1), vars(4), out_dir);

	for i=1:numel(vars)
		vars(i).is_delayed = numel(strfind(vars(i).id, 'L'))>0;
	end
	
	for i=1:numel(vars)
		% do not create histogram for delayed variables
		if not(vars(i).is_delayed)
			create_dist_plots(vars(i), out_dir);
			create_dist_samples_plots(saccades, vars(i), out_dir);
			create_xcorr_plots(vars(i), out_dir);
			create_xcorr_sample_plots(saccades, vars(i), out_dir);
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
	
	vartoinclude = vars( [vars.include_in_bigcorr] == true );
	create_bigcorr_plots(saccades, vartoinclude, out_dir);

function create_bigcorr_plots(saccades, vars, out_dir)
	basename='sac_bigcorr';
	if report_should_I_skip(out_dir, basename), return, end
	
	[all_samples, saccades] = add_sample_num(saccades);
	N = numel(all_samples);
	nvars = numel(vars);

    side = 4;
    bigbigR = zeros(nvars*side, nvars*side);

	bigR = zeros(nvars, nvars);
	for a=1:N
		for_this_sample = [saccades.sample_num] == a;
		sample_len = numel(find(for_this_sample));
		% create a big array with all the values
		X = zeros(sample_len, nvars);
		for v=1:numel(vars)
			x = vars(v).values(for_this_sample);
			assert(numel(x) == sample_len);
			X(:, v) = x;
		end
		% remove rows that have nans
		good_rows = not(any(isnan(X),2));
		X = X(good_rows, :);
		
%		C = cov(X);
		R = corr(X);
		% average all correlation matrices
		fraction = sample_len / numel(saccades);
		assert(fraction <= 1);
		bigR = bigR + R * fraction;
	
        u = mod(a-1, side);
        v = floor( (a-1)/side);
        assert(u<=side && v<=side);
        for i=1:size(R,1)
        for j=1:size(R,2)
            m = 1+(i-1)*side + u;
            n = 1+(j-1)*side + v;
            bigbigR(m,n) = R(i,j);
        end
        end 
    end
	
	f = sac_figure(70); hold on
	im = colorcorr(bigR);
	image(1:nvars, 1:nvars, im);
	axis([0 nvars+1 0 nvars+1])
	letters = {vars.letter};
	set(gca, 'XTick', 1:nvars);
	set(gca, 'XTickLabel', letters);
	set(gca, 'YTick', 1:nvars);
	set(gca, 'YTickLabel', letters);
	ftitle=sprintf('variables correlation');
	sac_print(out_dir, basename, ftitle);
	close(f)

	
	astext = write_corr_as_text(bigR);
	f=fopen(sprintf('%s/%s.txt', out_dir, basename),'w');
	fwrite(f,astext);
	fclose(f);

	f = sac_figure(70); hold on
	im = colorcorr(bigbigR);
	image(1:nvars, 1:nvars, im);
	axis([0 nvars+1 0 nvars+1])
	letters = {vars.letter};
	set(gca, 'XTick', 1:nvars);
	set(gca, 'XTickLabel', letters);
	set(gca, 'YTick', 1:nvars);
	set(gca, 'YTickLabel', letters);
	ftitle=sprintf('variables correlation (per sample)');
	sac_print(out_dir, 'sac_bigcorr_2', ftitle);
	close(f)

function create_dist_samples_plots(saccades, var1, out_dir)
	basename=sprintf('sac_dist_samples-%s', var1.id);
	if ~report_should_I_skip(out_dir, basename)
		[all_samples, saccades] = add_sample_num(saccades);
		f = sac_figure(70); hold on
		N = numel(all_samples);
		percentiles = [1 5 25 50 75 95 99];
		colors = {'k','r','b','g','b','r','k'};
		perc_results = [];
		variable_average = [];
		variable_std = [];
		for a=1:N
			saccades_for_sample = [saccades.sample_num] == a;
			assert(numel(saccades_for_sample) == numel(var1.values));
			
			selected_values = var1.values(saccades_for_sample);
			variable_average(a) = mean( selected_values);
			variable_std(a) = std( selected_values);
			perc_results(a,:) = prctile(selected_values, percentiles);
		end
		
		A=[0 N+1 var1.interesting(1)*1.5 var1.interesting(2)];
		axis(A)
		% lets order by the median
		median = perc_results(:,4);
		[dummy, ordered_by_median] = sort(median);
		
		perc_results = perc_results(ordered_by_median, :);
		
		legend_entries = {};
		for i=1:numel(percentiles)
			vals = perc_results(:, i);
			plot(1:N, vals, sprintf('%s.--', colors{i}));
			legend_entries{i} = sprintf('%d%%', percentiles(i));
		end
		
		colors2 = {'k','r','b','b','r','k'};
		for i=1:(numel(percentiles)-1)
			for a=1:N
				from = perc_results(a,i);
				to = perc_results(a,i+1);
				plot([a a], [from to], sprintf('%s-', colors2{i}));
			end
		end
%		legend(legend_entries)
		%errorbar(1:N,variable_average,variable_std*3,'rx')
		ylabel(sprintf('%s (%s)', var1.name, var1.unit))
		xlabel('sample')
		axis(A);

		
		%axis([0 N+1 0 100])
		%legend(all_samples)
		ftitle=sprintf('Percentiles of %s (1 5 25 50 75 95 99)', var1.name);
		sac_print(out_dir, basename, ftitle);
		close(f)
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

function create_xcorr_sample_plots(saccades, var1, out_dir)
	maxlag = 10;
	
	basename=sprintf('sac_xcorr_sample-%s', var1.id);
	if ~report_should_I_skip(out_dir, basename)	
		[all_samples, saccades] = add_sample_num(saccades);
		N = numel(all_samples);
		colors={'r','g','b','k','m'};
		f = sac_figure(21); hold on
		
		for a=1:N
			saccades_for_sample = [saccades.sample_num] == a;
			assert(numel(saccades_for_sample) == numel(var1.values));
			x = var1.values(saccades_for_sample);
			x = x(not(isnan(x)));
			x = x - mean(x);
			[S_xcorr, lags] = xcorr(x, maxlag, 'coeff');
			color_index = 1 + mod(a-1, numel(colors));
			style = sprintf('%s.-', colors{color_index});
			plot(lags, S_xcorr, style);
		end
		
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

% XXXX I changed var2-var1 because it's late
function create_joint_plots_by_sample(saccades, var2, var1, out_dir)
	colors = {'k','r','b','g','m','y'};
	basename=sprintf('sac_joint_samples-%s-%s', var2.id, var1.id);
	if report_should_I_skip(out_dir, basename), return, end	
	
	[all_samples, saccades] = add_sample_num(saccades);
	N = numel(all_samples);

	f = sac_figure;
	hold on
	N = 5;
	for a=1:N
		for_this_sample = [saccades.sample_num] == a;
		x = var1.values(for_this_sample);
		y = var2.values(for_this_sample);
		col = sprintf('%s.', colors{mod(a-1,numel(colors))+1});
		loglog(x,y,col,'MarkerSize',1)
		h=plot(x,y,col);
%		get(h,'MarkerSize')
	end
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
	
		
	xlabel(sprintf('%s (%s)', var1.name, var1.unit))
	ylabel(sprintf('%s (%s)', var2.name, var2.unit))
	ftitle = sprintf('Joint distribution of %s / %s ', var1.name, var2.name);
	sac_print(out_dir, basename, ftitle);
	close(f)
	
	
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
	
	
	
	
