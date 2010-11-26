function [theta2] = theta_unwrap(theta)
theta2(1) = theta(1);
for i=2:numel(theta)
	diff = theta(i)-theta(i-1);
	increment = atan2(sin(diff),cos(diff));
	theta2(i) = theta2(i-1) + increment;
	difference2 = theta2(i)-theta2(i-1);
	
	if 0
		fprintf('theta %.1f theta-1 %.1f diff %.1f increment: %.1f deg\n', rad2deg(theta(i)), rad2deg(theta(i-1)), rad2deg(diff), rad2deg(increment) )
	
		fprintf(' theta (%.2f, %.2f) theta2 (%.2f, %.2f) abs(diff): %.2f deg\n',...
			cos(theta(i)),sin(theta(i)), ...
			cos(theta2(i)),sin(theta2(i)),...
			rad2deg(difference2))
	end
	
	assert(abs(cos(theta2(i)) - cos(theta(i)))< 1e-3)
	assert(abs(sin(theta2(i)) - sin(theta(i)))< 1e-3)
	assert(abs(difference2) <= 1.001 *pi)
	
end