function create_temporal_correlation(saccades, vars, out_dir)
	basename='sac_bigtime';
	if report_should_I_skip(out_dir, basename), return, end
	
	magnify=8;
	
	[all_samples, saccades] = add_sample_num(saccades);
	N = numel(all_samples);
	nvars = numel(vars);
	noriginal_vars = numel(vars);
    
    nv = nvars;
    
    % let's create the delayed version
%    deltas = [1,2,3,5,10,20];
%    deltas = [1,2,3];
	deltas = [1];
%	deltas = [1,2,10];
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
    %bigbigR = zeros(nvars*side, nvars*side);
	correlation = nan * zeros(nvars,nvars,N);
	correlation_pvalues = nan * zeros(nvars,nvars,N);
	
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
		 
		[R, pval] = corr(X);
		
		% average all correlation matrices
		fraction = sample_len / numel(saccades);
		assert(fraction <= 1);
		bigR = bigR + R * fraction;
	
		correlation(:,:,a) = R; 
		correlation_pvalues(:,:,a) = pval;
		correlation_significant(:,:,a) = pval < 0.01; 
    end
	
	letters = {vars.letter};
	orig_letters = {vars(1:noriginal_vars).letter}; 
	
	
	f = sac_figure(70); hold on
	X = bigR(1:noriginal_vars,:);
	X = kron(X, ones(4,4));
	im = colorcorr(X);
	im = magnify_image(im, magnify);
	%image(1:nvars, 1:noriginal_vars, im);
	image((0:nvars)+0.5, (0:noriginal_vars)+0.5, im);
	axis([0 nvars+1 0 nvars+1])
%	axis('equal')
	set(gca, 'XTick', 1:nvars);
	set(gca, 'XTickLabel', letters);
	set(gca, 'YTick', 1:noriginal_vars);
	set(gca, 'YTickLabel', orig_letters);
	ftitle=sprintf('variables correlation');
	sac_print(out_dir, basename, ftitle);
	close(f)
	
	astext = write_corr_as_text(bigR);
	f=fopen(sprintf('%s/%s.txt', out_dir, basename),'w');
	fwrite(f,astext);
	fclose(f);


	f = sac_figure(70); hold on	
	X = correlation(1:noriginal_vars,:,:);
	im = colorcorr(make_mosaic(X, 4, 4));
	im = magnify_image(im, magnify);
	image((0:nvars)+0.5, (0:noriginal_vars)+0.5, im);
	axis([0 nvars+1 0 nvars+1])
%	axis('equal')
	set(gca, 'XTick', 1:nvars);
	set(gca, 'XTickLabel', letters);
	set(gca, 'YTick', 1:noriginal_vars);
	set(gca, 'YTickLabel', orig_letters);
	ftitle=sprintf('variables correlation (per sample)');
	sac_print(out_dir, 'sac_bigtime_2', ftitle);
	close(f)


	f = sac_figure(70); hold on
	X = correlation_significant(1:noriginal_vars,:,:);
	im = truth2rgb(make_mosaic(X, 4, 4));
	im = magnify_image(im, magnify);
	image((0:nvars)+0.5, (0:noriginal_vars)+0.5, im);
	axis([0 nvars+1 0 nvars+1])
%	axis('equal')
	set(gca, 'XTick', (1:nvars));
	set(gca, 'XTickLabel', letters);
	set(gca, 'YTick', (1:noriginal_vars));
	set(gca, 'YTickLabel', orig_letters);
	ftitle=sprintf('significant correlation (per sample)');
	sac_print(out_dir, 'sac_bigtime_3', ftitle);
	close(f)

	% Find if the distributions are significantly correlated
	% significant = [];
	% significant_pvalue = [];
	% for a=1:N
	% 	for_this_sample = [saccades.sample_num] == a;
	% 	for v1=1:numel(vars)
	% 	for v2=1:numel(vars)
	% 		x1 = vars(v1).values(for_this_sample);
	% 		x2 = vars(v2).values(for_this_sample);
	% 
	% 		[h,p] = ttest2(x1,x2,0.01);
	% 		significant_pvalue(v1,v2,a) = p;
	% 		significant(v1,v2,a) = h;
	% 	end
	% 	end
	% end
	% 
	% significant_pvalue(:,:,1)
	% significant(:,:,1)
	% 
	% significant_big = make_mosaic(significant, 4, 4);
	
	% 
	% f = sac_figure(70); hold on
	% rgb = truth2rgb(significant_big);
	% image(1:nvars, 1:nvars, rgb);
	% axis([0 nvars+1 0 nvars+1])
	% letters = {vars.letter};
	% set(gca, 'XTick', 1:nvars);
	% set(gca, 'XTickLabel', letters);
	% set(gca, 'YTick', 1:nvars);
	% set(gca, 'YTickLabel', letters);
	% ftitle=sprintf('significance of correlation');
	% sac_print(out_dir, 'sac_bigtime_3', ftitle);
	% close(f)
	% 
	% 
	% 
	


function res = magnify_image(im, magnify)
	for i=1:3
	res(:,:,i) = kron(im(:,:,i), ones(magnify,magnify));
	end

%	res = im; % disable