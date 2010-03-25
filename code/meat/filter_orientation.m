function res = filter_orientation(timestamp, orientation, lambda)
	% returns 
	%  res.timestamp
	%  res.orientation
	%  res.velocity
	%  res.filtered_orientation
	%  res.filtered_velocity
	%  res.filtered_acceleration
	%  res.error
	res.timestamp = timestamp;
	res.lambda = lambda;
	[x,DTx,DDTx,status]  = l1tf(orientation, lambda);
	res.filtered_orientation = x;
	res.energy = sum(abs(DDTx));
	res.DTx = DTx;
	res.DDTx = DDTx;
	res.orientation = orientation;
	res.velocity = numerical_derivative(timestamp, orientation);
	res.acceleration = numerical_derivative(timestamp, res.velocity);
%	res.filtered_velocity = DTx;
	res.filtered_velocity = numerical_derivative(timestamp, res.filtered_orientation);
	res.filtered_acceleration = numerical_derivative(timestamp, res.filtered_velocity);;

	res.error = orientation - res.filtered_orientation;
	res.rmse = sqrt(sum(res.error .^ 2));