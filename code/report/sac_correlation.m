function sac_correlation(saccades, out_dir)
% function sac_correlation(saccades, out_dir)
%
% Displays various correlation data

	S = [saccades.sign];
	maxlag = 20;
	
	[S_xcorr, lags] = xcorr(S, maxlag, 'coeff');
	
	f = sac_figure(21);
	plot(lags, S_xcorr, '.')
	ylabel('correlation')
	xlabel('distance in the sequence')
	ftitle='Correlation of saccade sign';
	sac_print(out_dir, 'sac_sign_corr', ftitle);
	
	
	A = abs([saccades.amplitude]);
	[A_xcorr, lags] = xcorr(A, maxlag, 'coeff');
	
	f = sac_figure(22);
	plot(lags, A_xcorr, '.')
	ylabel('correlation')
	xlabel('distance in the sequence')
	ftitle = 'Correlation of saccade amplitude';
	sac_print(out_dir, 'sac_amp_corr', ftitle);
	