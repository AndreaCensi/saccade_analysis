function create_temporal_correlation(saccades, vars, out_dir)
	basename='sac_bigtime';
	if report_should_I_skip(out_dir, basename), return, end
	
	[all_samples, saccades] = add_sample_num(saccades);
	N = numel(all_samples);
	nvars = numel(vars);
    
    nv = nvars;
    
    % let's create the delayed version
    deltas = [1,2,3,5,10,20];
    for i=1:numel(deltas)
        delta = deltas(i);
        
        for k=1:nvars 
            nv = nv + 1;
            
        	vars(nv).id = sprintf('%s%d', vars(k).id, delta);
	        vars(nv).letter = sprintf('%s%d', vars(k).letter, delta);
	        
	        y = vars(k).values;
            for tau=1:delta
                y = [nan y(1:end-1)];
            end

        	vars(nv).values = y;
        end 
    end	

% XXXXXXXXXXXXXXXXXXXXXXXX
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
	sac_print(out_dir, 'sac_bigtime_2', ftitle);
	close(f)




