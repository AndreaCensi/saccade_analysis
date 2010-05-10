function sac_correlation(saccades, out_dir)
% function sac_correlation(saccades, out_dir)
%
% Displays various correlation data

	s1 = report_should_I_skip(out_dir,'sac_sign_corr');
	s2 = report_should_I_skip(out_dir,'sac_sign_corr_2');
	if s1 & s2
		return
	end

	maxlag = 8;
	
	[all_samples, saccades] = add_sample_num(saccades);
	all_xcorr = [];
	loglength = [];
	for a=1:numel(all_samples)
		sample_saccades = saccades([saccades.sample_num] == a);
		loglength(a) = numel(sample_saccades);
		S = [sample_saccades.sign];
		mean_S = mean(S);
		S = S - mean_S;
		fprintf('%s mean S = %f\n', all_samples{a}, mean_S);
		[xc, lags] = xcorr( S , maxlag, 'coeff');	
		all_xcorr(a,:) = xc;
	end
	
	logfrac = loglength ./ sum(loglength);
	all_xc = sum(diag(logfrac) * all_xcorr, 1);
	
	
	basename = 'sac_sign_corr';
	if ~s1
		colors={'r','g','b','k','m'};
		f = sac_figure(21); hold on
		for a=1:numel(all_samples)
			color_index = 1 + mod(a-1, numel(colors));
			plot(lags, all_xcorr(a,:), sprintf('%sx-', colors{color_index}));
		end
		ylabel('correlation')
		xlabel('distance in the sequence')
		axis([-maxlag +maxlag -0.5 1.1])
		%legend(all_samples)
		ftitle='Correlation of saccade sign';
		sac_print(out_dir, basename, ftitle);
		close(f)
	end
	
	basename='sac_sign_corr_2';
	if ~s2
		f = sac_figure(21);
		plot(lags, all_xc, 'bx-')
		ylabel('correlation')
		xlabel('distance in the sequence')
		axis([-maxlag +maxlag -0.5 1.1])
		ftitle='Correlation of saccade sign';
		sac_print(out_dir,basename, ftitle);
		close(f)
	end
	
	
	
	% Define:   X = Bin(n, 0.5)  number of left:
	% Define   A=X/n = average number of lefts:
	% Variance of X =  n p (1 - p)
	% Variance of A =  n p (1 - p)  / n^2 = p (1 - p)  / n
	% Std-dev of A = sqrt(0.5^2) / sqrt(n) = 0.5 / sqrt(n)
	
	basename = 'sac_sign_averages';
	if ~report_should_I_skip(out_dir, basename)
		[all_samples, saccades] = add_sample_num(saccades);
		f = sac_figure(21); hold on
		N = numel(all_samples);
		sample_saccades_num = [];
		for a=1:N
			sample_saccades = saccades([saccades.sample_num] == a);
			sample_saccades_num(a) = numel(sample_saccades);
			percentage_left(a) = 100 * sum([sample_saccades.sign]==+1) / numel(sample_saccades);
		end
		bar(1:N, percentage_left)
%		set(gca,'XTickLabel',all_samples)
%		plot([0 N+1], [50 50], 'r-')
		std = 1./sqrt(sample_saccades_num);
		E = 100* 3*std;
		M = 100*ones(N,1) * 0.5;
		errorbar(1:N,M,E,'rx')
		
		ylabel('perc. left turns %')
		xlabel('sample')
		axis([0 N+1 0 100])
		%legend(all_samples)
		ftitle='Percentage of left turns';
		sac_print(out_dir, basename, ftitle);
		close(f)
	end

	
	 