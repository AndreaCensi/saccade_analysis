function M = reshape_fluid(v, rows)
	n = numel(v);
	cols = ceil(n/rows);
	n2 = rows * cols;
	nextra = n2-n;
	v(n+1:n2) = 0;
	
	M = reshape(v, rows, cols)';