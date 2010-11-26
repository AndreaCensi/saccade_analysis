function r = roughness(x,y,zone)
	neighborhood = [ones(1,zone)  0   ones(1,zone)];
	neighborhood = neighborhood  / sum(neighborhood);
	xf = conv_pad(x, neighborhood);
	yf = conv_pad(y, neighborhood);
	
	r = sqrt( (x-xf).^2 + (y-yf).^2 );
	