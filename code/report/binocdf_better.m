function cdf = binocdf_better(X,N,p)
	% Returns p-values for one-sided test
	% p can be an array
	assert(X>=0);
	assert(N>0);
	assert(X<=N);
	assert(all(0<=p));
	assert(all(p<=1));
	assert(round(X)==X)
	assert(round(N)==N)
	
	% we transform to a problem where X is small

	for i=1:numel(p)
		cdf(i) = sum(binopdf(0:X,N,p(i)));
	end