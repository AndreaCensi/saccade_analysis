function plot_with_arrows(x,y,theta)
	scale = 0.03;
	x = asrow(x);
	y = asrow(y);
	theta = asrow(theta);
	
	
	u = cos(theta) * scale;
	v = sin(theta) * scale;
	
	w = mod(1:numel(x), 1) == 0;
	
	
	plot(x,y,'k.')
	quiver(x(w),y(w),u(w),v(w))
	
function y = asrow(y)
	if size(y,1) > size(y,2)
		y = y';
	end