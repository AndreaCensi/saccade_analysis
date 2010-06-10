function B = make_mosaic(X, mini_rows, mini_cols)
	rows = size(X,1);
	cols = size(X,2);
	nsamples = size(X,3);
	assert(mini_rows * mini_cols >= nsamples);

	B = nan*zeros(rows * mini_rows, cols * mini_cols);


	for k=1:nsamples
		u = mod(k-1, mini_cols);
	    v = floor( (k-1)/mini_cols);
	for i=1:rows
	for j=1:cols
	    m = 1+(i-1)*mini_cols + u;
	    n = 1+(j-1)*mini_cols + v;
	    B(m,n) = X(i,j,k);
	end
	end
	end

