function sac_corr_start_and_sign(saccades, out_dir)

	if report_should_I_skip(out_dir, 'sac_turn_count'), return, end
	

	S = [saccades.sign];

	theta0 = max(1, min(360, round(mod([saccades.orientation_start],360))));
	
	orientation_start_left  = theta0(S == +1);
	orientation_start_right = theta0(S == -1);
	
	
	nbins = 90;
	[hist_left, bin_positions] = hist(orientation_start_left, nbins);
	[hist_right, bin_positions] = hist(orientation_start_right, nbins);

	prob_right = hist_right ./ (hist_left + hist_right);
	prob_left = hist_left ./ (hist_left + hist_right);
	
	f=sac_figure(33);  
	hold off
	plot(bin_positions, hist_left, 'r-')
	hold on
	plot(bin_positions, hist_right, 'g-')
	legend('left', 'right')
	xlabel('start orientation (deg)')
	ylabel('number of samples')
	ftitle='Sample count, turning left or right';
	sac_print(out_dir, 'sac_turn_count', ftitle);
	a=axis;
	a(1)=0;
	a(2)=360;
	axis(a)
	close(f)
	
	
	f=sac_figure(32);  
	hold off
	plot(bin_positions, prob_left, 'r-')
	hold on
	plot(bin_positions, prob_right, 'g-')
	a = axis;
	a(3) = 0;
	a(4) = 1;
	axis(a);
	legend('prob. of left turn', 'prob. of right turn')
	xlabel('start orientation (deg)')
	ylabel('probability')
	ftitle='Probability of turning left or right';
	sac_print(out_dir, 'sac_turn_probability', ftitle);
	close(f)
	
	