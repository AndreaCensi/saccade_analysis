function y = gaussian_smooth(x, sigma_steps)
	filter_g = fspecial('gaussian', [1 ceil(sigma_steps)*6], sigma_steps);
	y = conv_pad(x, filter_g);
	