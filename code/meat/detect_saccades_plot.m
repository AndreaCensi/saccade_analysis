function detect_saccades_plot(res)
% function detect_saccades_plot(res)
%   plots the results returned by detect_saccades()

	start = [res.saccades.start];
	stop = [res.saccades.stop];

	figure; hold off
	plot(res.timestamp, res.orientation, 'r.'); hold on
	plot(res.timestamp, res.filtered_orientation, 'b-')
title('orientation')
	plot_saccade_delimiters(res.saccades, res.timestamp, res.orientation, 50)
	
	figure; hold off
	plot(res.timestamp, res.velocity, 'r.'); hold on
	plot(res.timestamp, res.filtered_velocity, 'b-')
	title('angular velocity')
	plot_saccade_delimiters(res.saccades, res.timestamp, res.velocity, 250)
	
	if false
	figure; hold on
	plot(res.timestamp, res.robust_velocity, 'k.')
	w = res.saccades_moments;
	plot(res.timestamp(w), res.robust_velocity(w), 'rx')
	plot(res.timestamp(start), res.robust_velocity(start), 'gx')
	title('maxima detection')
	end
	

function plot_saccade_delimiters(saccades, xf, yf, ybarsize)
	for i=1:numel(saccades)
		s = saccades(i).start;
		x1 = xf(s);
		y1 = yf(s);
		plot( [x1 x1], [y1-ybarsize y1+ybarsize] , 'g-')
		s = saccades(i).stop;
		x2 = xf(s);
		y2 = yf(s);
		plot( [x2 x2], [y2-ybarsize y2+ybarsize] , 'b-')
		plot( [x1 x2], [y1-ybarsize y2-ybarsize] , 'r-')
	end	
	
		
	