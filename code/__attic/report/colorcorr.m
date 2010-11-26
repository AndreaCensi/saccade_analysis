function rgb = colorcorr(R)
	% returns a RGB representation of the correlation matrix R
	
	nans = isnan(R);
	R(nans) = 0;
	
	m = max(max(abs(R)));
	R = R / (m*1.00001);;
	
	positive_part = +max(R, 0);
	negative_part = -min(R, 0);
	anysign = abs(R);


%	fprintf('Maximum abs pos =  %f\n', max(max(abs(positive_part))))
%	fprintf('Maximum abs neg =  %f\n', max(max(abs(negative_part))))
%	fprintf('Maximum abs any =  %f\n', max(max(abs(anysign))))
		
	

	R = -negative_part + 1;
	G = -anysign + 1;
	B = -positive_part + 1;
	
	R(nans) = 1;
	G(nans) = 1;
	B(nans) = 0.5;
	
	rgb = zeros(size(R,1), size(R,2), 3);
	rgb(:,:,1)=R;
	rgb(:,:,2)=G;
	rgb(:,:,3)=B;
	
	