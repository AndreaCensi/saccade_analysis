function sac_correlation(saccades, out_dir)
% function sac_correlation(saccades, out_dir)
%
% Displays various correlation data

	S = [saccades.sign];
	maxlag = 20;
	
	[S_xcorr, lags] = xcorr(S, maxlag, 'coeff');
	
	f = figure(21);
	plot(lags, S_xcorr, '.')
	ylabel('correlation')
	xlabel('distance in the sequence')
	title('Correlation of saccade sign')
	print('-depsc2', sprintf('%s/sac_sign_corr.eps', out_dir))
	
	A = abs([saccades.amplitude]);
	[A_xcorr, lags] = xcorr(A, maxlag, 'coeff');
	
	f = figure(22);
	plot(lags, A_xcorr, '.')
	ylabel('correlation')
	xlabel('distance in the sequence')
	title('Correlation of saccade amplitude')
	print('-depsc2', sprintf('%s/sac_amp_corr.eps', out_dir))
	