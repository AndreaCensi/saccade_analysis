function der = numerical_derivative(dt, x)
	% Computes the derivative numerically.
	% timestamp is used to normalize the step size
	assert(numel(dt) == 1);
	
	% assert(min(size(x)) == 1);
	% if size(x,1) > 1
	% 	x = x';
	% end
	 

    der = conv_pad(x, [-1 0 1]) / (2*dt);

	
	% if not(all(size(der)==size(x)))
	% 		der = der';
	% 	end
	
