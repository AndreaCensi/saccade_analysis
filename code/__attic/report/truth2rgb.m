function rgb = truth2rgb(T)
	
	rgb = zeros(size(T,1),size(T,2),3);
	nans = isnan(T) > 0;
 
	T(nans) = 0; 

	R = zeros(size(T,1), size(T,2));
	G = zeros(size(T,1), size(T,2));
	B = zeros(size(T,1), size(T,2));
	
	R(not(T)) = 1;
	G(not(T)) = 1;
	B(not(T)) = 1;

	ok = not(not(T));
	R(ok) = 0;
	G(ok) = 1;
	B(ok) = 0;
	

	R(nans) = 1;
	G(nans) = 1;
	B(nans) = 0.5;

	rgb( :, :, 1) = R;
	rgb( :, :, 2) = G;
	rgb( :, :, 3) = B;
	
