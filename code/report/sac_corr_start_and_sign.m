function sac_corr_start_and_sign(saccades, out_dir)

	S = [saccades.sign];

	theta0 = max(1, min(360, round(mod([saccades.orientation_start],360))));
	
	orientation_start_left  = theta0(S == +1);
	orientation_start_right = theta0(S == -1);
	
	
	nbins = 180;
	[hist_left, bin_positions] = hist(orientation_start_left, nbins);
	[hist_right, bin_positions] = hist(orientation_start_right, nbins);

	prob_right = hist_right ./ (hist_left + hist_right);
	prob_left = hist_left ./ (hist_left + hist_right);
	
	f=figure(33);  
	hold on
	plot(bin_positions, hist_left, 'r-')
	plot(bin_positions, hist_right, 'g-')
	legend('left turn', 'right turn')
	xlabel('start orientation (deg)')
	ylabel('number of samples')
	title('sample count, turning left or right')
	print('-depsc2', sprintf('%s/sac_turn_count.eps', out_dir))
	
	
	f=figure(32);  
	hold on
	plot(bin_positions, prob_left, 'r-')
	plot(bin_positions, prob_right, 'g-')
	a = axis;
	a(3) = 0;
	a(4) = 1;
	axis(a);
	legend('prob. of left turn', 'prob. of right turn')
	xlabel('start orientation (deg)')
	ylabel('probability')
	print('-depsc2', sprintf('%s/sac_turn_probability.eps', out_dir))
	
	
	