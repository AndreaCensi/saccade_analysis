function s = extrema(x)
% function s = extrema(x)
%  Finds the extrema (minima and maxima) of a sequence
%  Returns a sequence of the same length of input x.
%    s(i) == 1   if x(i) is a strict local maximum
%    s(i) == -1  if x(i) is a strict local minimum
%    s(i) == 0   otherwise
%  Note that plateaus are not detected as minima/maxima.

	s = zeros(size(x));
	for i=2:(numel(x)-1)
		d1 = x(i)-x(i-1);
		d2 = x(i+1)-x(i);
		% if we are an extrema
		if d1*d2 < 0
			extrema_sign = sign(d1);
		
			% make sure we get rid of local minima
			if extrema_sign	 == sign(x(i))
				s(i) = extrema_sign;
			end
		end
	end


