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


