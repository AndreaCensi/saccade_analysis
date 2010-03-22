function der = numerical_derivative(timestamp, x)
	% Computes the derivative numerically.
	% timestamp is used to normalize the step size
	
	assert(min(size(x)) == 1);
	if size(x,1) > 1
		x = x';
	end
	
	dt = timestamp(2)-timestamp(1);
%	f = filter([-1 0 1], 1, x) / dt;
	f = gradient(x) / dt;

	der = f ;
%	der = [f(1) f f(end)];
	
	if not(all(size(der)==size(x)))
		der = der';
	end

