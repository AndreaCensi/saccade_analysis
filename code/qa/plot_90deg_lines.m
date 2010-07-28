function plot_90deg_lines()
% plot every 90 deg
	a = axis();
	T1 = a(1); T2 = a(2); 
	O1 = a(3); O2 = a(4);
	grid_interval = 90;
	first_line = floor(O1 / grid_interval) * grid_interval;
	last_line = ceil(O2 / grid_interval) * grid_interval;
	for line_pos=first_line:grid_interval:last_line
		plot([T1 T2], [line_pos, line_pos], 'k--')
		hold on
	end
	