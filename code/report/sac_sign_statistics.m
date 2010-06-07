function sac_sign_statistics(saccades, out_dir)
	basename = 'sac_sign_stats';
	if report_should_I_skip(out_dir, basename), return, end

	[all_samples, saccades] = add_sample_num(saccades);
	num_samples = numel(all_samples);

	f_comments = fopen(path_join(out_dir, 'sac_sign_stats-misc.txt' ), 'w');
	fprintf(f_comments, '%s - misc comments \n', saccades(1).species);
	
	threshold = 0.01;
	
	for a=1:num_samples
		sample_saccades = saccades([saccades.sample_num] == a);
	
		S = [sample_saccades.sign];

		N(a) = numel(S);
		L(a) = numel(find(S==+1));
		R(a) = numel(find(S==-1));
		m(a) = min([L(a) R(a)]);
		pvalue(a) = binocdf(m(a),N(a),0.5);
		
		skewed_left(a) =  binocdf(L(a),N(a),0.5) > 1- threshold;
		skewed_right(a) =  binocdf(R(a),N(a),0.5) > 1- threshold;
		
	%	fprintf('- sample %3d:  N = %4d , L = %4d, R = %4d, m=%4d, p = %f\n',...
	%		a,N(a),L(a),R(a),m(a),pvalue(a));
			
		stats = compute_seq_statistics([sample_saccades.letter]);
		assert(stats.N == stats.L + stats.R);
		
		r = stats.L / stats.N;
		% stats.LL ~ Binomial( x, stats.L, r)
		% stats.LR ~ Binomial( x, stats.L, 1-r) --- but dependent on the previous
		% stats.RL ~ Binomial( x, stats.R, r)
		% stats.RR ~ Binomial( x, stats.R, 1-r) --- but dependent on the previous
		
		cdf_LL = binocdf( stats.LL, stats.L, r);
		pvalue_LL(a) = min( [cdf_LL, 1-cdf_LL] );
		cdf_RL = binocdf( stats.RL, stats.R, r);
		pvalue_RL(a) = min( [cdf_RL, 1-cdf_RL] );
		pvalue_independence(a) = min(pvalue_LL(a), pvalue_RL(a));

		LL_neg(a) = cdf_LL < threshold;
		LL_pos(a) = cdf_LL > 1 - threshold;
		RL_neg(a) = cdf_RL < threshold;
		RL_pos(a) = cdf_RL > 1 - threshold;
		
		significant_pos_corr(a) = LL_pos(a) | RL_neg(a);
		significant_neg_corr(a) = LL_neg(a) | RL_pos(a);
		
%		fprintf(f_comments, 'LL %.4f  RL %.4f  ind %.4f   LL+ %d  LL- %d  RL+ %d  RL- %d \n', ...
%			pvalue_LL(a), pvalue_RL(a),	pvalue_independence(a),...
%			LL_pos(a),LL_neg(a),RL_pos(a),RL_neg(a) );
			
		fprintf(f_comments, '%s %s\n', stats.independent_desc, stats.firstorder_desc);
		fprintf('%s %s\n', stats.independent_desc, stats.firstorder_desc);
	end
	% TODO: save data to disk
	
	% Creating dummy file
	f = fopen(path_join(out_dir, sprintf('%s.txt', basename) ), 'w');
	fclose(f);
	
	f = fopen(path_join(out_dir, sprintf('sac_sign_stats_pvalue.txt', basename) ), 'w');
	fprintf(f, '%s - p-values\n', saccades(1).species);
	for a=1:num_samples
		if pvalue(a) < threshold
			tag = '*';
		else
			tag = ' ';
		end
		why = '';
		if skewed_left(a)
			why = 'left ';
		end
		if skewed_right(a)
			why = '      right';	
		end
		fprintf(f, '%f%s %s\n', pvalue(a), tag, why);
	end

	f = fopen(path_join(out_dir, 'sac_sign_stats_pvalue-indep.txt' ), 'w');
	fprintf(f, '%s - p-values for independence\n', saccades(1).species);
	for a=1:num_samples
		why ='';
		if significant_neg_corr(a)
	 		why = '     neg';
		end
		if significant_pos_corr(a)
	 		why = 'pos';
		end
		if pvalue_independence(a) < threshold
			tag = '*';
		else
			tag = ' ';
		end
		fprintf(f, '%f%s  %s \n', pvalue_independence(a), tag, why);
	end
	
	fclose(f);



function r = compute_seq_statistics(letters)
	r.N = numel(letters);
	r.L = count(letters, 'L');
	r.R = count(letters, 'R');
	r.LL =  count(letters, 'LL');
	r.RL =  count(letters, 'RL');
	r.RR =  count(letters, 'RR');
	r.LR =  count(letters, 'LR');

	[r.r, r.r_int] = binofit(r.L, r.N, 0.01);

	r.LL_cdf = binocdf(r.LL, r.L, [r.r r.r_int]);
	r.RL_cdf = binocdf(r.RL, r.R, [r.r r.r_int]);
	r.LL_pvalue = cdf2pvalue( r.LL_cdf);
	r.RL_pvalue = cdf2pvalue( r.RL_cdf);
	
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
	r.independent_desc = sprintf('indep: %s  r[%.2f %.2f %.2f] {%.4f %.4f %.4f, %.4f %.4f %.4f}',...
		r.independent_desc,...
		r.r_int(1), r.r, r.r_int(2), ...
		r.LL_cdf(1), r.LL_cdf(2), r.LL_cdf(3), r.RL_cdf(1), r.RL_cdf(2), r.RL_cdf(3));
	
	
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