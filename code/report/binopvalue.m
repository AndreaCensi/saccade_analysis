function pvalue = binopvalue(X,N,p)
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
		if X > p(i) * N
			pvalue(i) = sum(binopdf(X:N,N,p(i)));
		else			
			% XXX: add other side?
			pvalue(i) = sum(binopdf(0:X,N,p(i)));
		end

	end