function res = colorcorr(R)
	% returns a RGB representation of the correlation matrix R
	
	m = max(max(abs(R)));
	R = R / (m*1.00001);;
	
	positive_part = +max(R, 0);
	negative_part = -min(R, 0);
	anysign = abs(R);


%	fprintf('Maximum abs pos =  %f\n', max(max(abs(positive_part))))
%	fprintf('Maximum abs neg =  %f\n', max(max(abs(negative_part))))
%	fprintf('Maximum abs any =  %f\n', max(max(abs(anysign))))
		
	res = zeros(size(R,1), size(R,2), 3);
	

	res(:,:,1) = -negative_part + 1;
	res(:,:,2) = -anysign + 1;
	res(:,:,3) = -positive_part + 1;
	

	
%	fprintf('Maximum value %f , %f\n', max(max(res)), min(min(res)));
