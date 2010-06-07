function r = compute_seq_statistics(letters)

	
	r.N = numel(letters);
	r.L = count(letters, 'L');
	r.R = count(letters, 'R');
	r.LL =  count(letters, 'LL');
	r.RL =  count(letters, 'RL');
	r.RR =  count(letters, 'RR');
	r.LR =  count(letters, 'LR');

%	[r.r, r.r_int] = binofit(r.L, r.N, 0.01);

	[r.r, r.r_int] = binofit(r.L, r.N, 0.01);

	r.LL_cdf = binocdf(r.LL, r.L, [r.r r.r_int]);
	r.RL_cdf = binocdf(r.RL, r.R, [r.r r.r_int]);
%	r.LL_pvalue = cdf2pvalue( r.LL_cdf);
%	r.RL_pvalue = cdf2pvalue( r.RL_cdf);

	r.LL_pvalue = binopvalue(r.LL, r.L, [r.r r.r_int]);
	r.RL_pvalue = binopvalue(r.RL, r.R, [r.r r.r_int]);
	
	r.independent_pvalue = max(...
			[min([r.LL_pvalue(1) r.RL_pvalue(1)]), ...
		     min([r.LL_pvalue(2) r.RL_pvalue(2)]), ...
		     min([r.LL_pvalue(3) r.RL_pvalue(3)])] );
		
	% r.independent_pvalue = more_extreme( ...
	% 	[least_extreme(r.LL_cdf), ...
	% 	 least_extreme(r.RL_cdf) ] );
%	r.independent_pvalue = min( max(cdf2pvalue(r.LL_cdf)), ...
%		                        max(cdf2pvalue(r.RL_cdf)) );
		
	r.independent_rejected = r.independent_pvalue < 0.01;
	
	if r.independent_rejected
		r.independent_desc = sprintf('%.4f *', r.independent_pvalue );
	else
		r.independent_desc = sprintf('%.4f  ', r.independent_pvalue);
	end
	r.independent_desc = sprintf('indep: %s  r[%.2f %.2f %.2f] {LL[%d/%d] %.4f %.4f %.4f, RL[%d/%d] %.4f %.4f %.4f}',...
		r.independent_desc,...
		r.r_int(1), r.r, r.r_int(2), ...
		r.LL, r.L, r.LL_cdf(1), r.LL_cdf(2), r.LL_cdf(3), ...
		r.RL, r.R, r.RL_cdf(1), r.RL_cdf(2), r.RL_cdf(3));
	
	
	r.RRL = count(letters, 'RRL');
	r.LRL = count(letters, 'LRL');
	r.RLL = count(letters, 'RLL');
	r.LLL = count(letters, 'LLL');
	
	
	
	[r.p1, r.p1_int] = binofit(r.RL, r.R, 0.01);
	[r.p2, r.p2_int] =  binofit(r.LL, r.L, 0.01);
	r.RRL_cdf = binocdf( r.RRL, r.RR, [r.p1 r.p1_int]);
	r.LRL_cdf = binocdf( r.LRL, r.LR, [r.p1 r.p1_int]);
	r.RLL_cdf = binocdf( r.RLL, r.RL, [r.p2 r.p2_int]);
	r.LLL_cdf = binocdf( r.LLL, r.LL, [r.p2 r.p2_int]);
	
	r.RRL_pvalue = cdf2pvalue(r.RRL_cdf);
	r.LRL_pvalue = cdf2pvalue(r.LRL_cdf);
	r.RLL_pvalue = cdf2pvalue(r.RLL_cdf);
	r.LLL_pvalue = cdf2pvalue(r.LLL_cdf);
	
	% r.firstorder_pvalue = max([...
	% min([r.RRL_pvalue(1) r.LRL_pvalue(1)  r.RLL_pvalue(1) r.LLL_pvalue(1)]), ...
	% min([r.RRL_pvalue(2) r.LRL_pvalue(2)  r.RLL_pvalue(2) r.LLL_pvalue(2)]), ...
	% min([r.RRL_pvalue(3) r.LRL_pvalue(3)  r.RLL_pvalue(3) r.LLL_pvalue(3)])]);

	r.firstorder_pvalue_p1 = max([...
	min([r.RRL_pvalue(1) r.LRL_pvalue(1)  ]), ...
	min([r.RRL_pvalue(2) r.LRL_pvalue(2)  ]), ...
	min([r.RRL_pvalue(3) r.LRL_pvalue(3)  ])]);
	
	r.firstorder_pvalue_p2 = max([...
	min([  r.RLL_pvalue(1) r.LLL_pvalue(1)]), ...
	min([  r.RLL_pvalue(2) r.LLL_pvalue(2)]), ...
	min([  r.RLL_pvalue(3) r.LLL_pvalue(3)])]);
	
	r.firstorder_pvalue = min( r.firstorder_pvalue_p1, r.firstorder_pvalue_p2 );
	r.firstorder_rejected = r.firstorder_pvalue< 0.01;
	if r.firstorder_rejected
		r.firstorder_desc = sprintf('%.4f *', r.firstorder_pvalue );
	else
		r.firstorder_desc = sprintf('%.4f  ', r.firstorder_pvalue);
	end
	r.firstorder_desc = sprintf('firstorder: %s (%.3f,%.3f) p1 [%.2f %.2f %.2f] p2 [%.2f %.2f %.2f] rrl[%.3f %.3f] lrl[%.3f %.3f] rll[%.3f %.3f] lll[%.3f %.3f]',...
	r.firstorder_desc,...
	r.firstorder_pvalue_p1, r.firstorder_pvalue_p2 ,...
		r.p1_int(1), r.p1, r.p1_int(2), r.p2_int(1), r.p2, r.p2_int(2), ...
		r.RRL_cdf(2), r.RRL_cdf(3), ...
		r.LRL_cdf(2), r.LRL_cdf(3), ...
		r.RLL_cdf(2), r.RLL_cdf(3), ...
		r.LLL_cdf(2), r.LLL_cdf(3) );

function  c = count(sequence, sub)
	c = numel(strfind(sequence, sub));

function v = cdf2pvalue(v)
	for i=1:numel(v)
		v(i) = min( v(i), 1-v(i));
	end