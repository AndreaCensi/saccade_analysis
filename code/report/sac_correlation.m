function sac_correlation(saccades, out_dir)
% function sac_correlation(saccades, out_dir)
%
% Displays various correlation data

	maxlag = 100;
	
	if ~report_should_I_skip(out_dir, 'sac_sign_corr')
		S = [saccades.sign];
		[S_xcorr, lags] = xcorr(S, maxlag, 'coeff');	
		f = sac_figure(21);
		plot(lags, S_xcorr, 'bx-')
		ylabel('correlation')
		xlabel('distance in the sequence')
		axis([-maxlag +maxlag 0 1])
		ftitle='Correlation of saccade sign';
		sac_print(out_dir, 'sac_sign_corr', ftitle);
		close(f)
	end
	
	basename = 'sac_sign_corr_2';
	if ~report_should_I_skip(out_dir, basename)
		[all_samples, saccades] = add_sample_num(saccades);
		colors={'r','g','b','k','m'};
		f = sac_figure(21); hold on
		for a=1:numel(all_samples)
			sample_saccades = saccades([saccades.sample_num] == a);
			S = [sample_saccades.sign];
			mean_S = mean(S);
			S = S - mean_S;
			fprintf('%s mean S = %f\n', all_samples{a}, mean_S);
			[S_xcorr, lags] = xcorr( S , maxlag, 'coeff');	
			color_index = 1 + mod(a-1, numel(colors));
			plot(lags, S_xcorr, sprintf('%sx-', colors{color_index}))
		end
		ylabel('correlation')
		xlabel('distance in the sequence')
		axis([-maxlag +maxlag 0 1])
		%legend(all_samples)
		ftitle='Correlation of saccade sign';
		sac_print(out_dir, basename, ftitle);
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
%		colors={'r','g','b','k','m'};
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

function [all_samples, saccades] = add_sample_num(saccades)
	all_samples = unique( {saccades.sample} );
	for i=1:numel(saccades)
		for a=1:numel(all_samples)
			if strcmp(all_samples{a}, saccades(i).sample)
				saccades(i).sample_num = a;
			end
		end	
	end
	
	
		% 
		% A = abs([saccades.amplitude]);
		% [A_xcorr, lags] = xcorr(A, maxlag, 'coeff');
		% 
		% f = sac_figure(22);
		% plot(lags, A_xcorr, '.')
		% ylabel('correlation')
		% xlabel('distance in the sequence')
		% ftitle = 'Correlation of saccade amplitude';
		% sac_print(out_dir, 'sac_amp_corr', ftitle);
		% 