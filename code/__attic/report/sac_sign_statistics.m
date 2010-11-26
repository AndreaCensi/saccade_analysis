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
    
        letters = letters_from_saccades(sample_saccades);
			
		stats = compute_seq_statistics(letters);
		assert(stats.N == stats.L + stats.R);
		
		r = stats.L / stats.N; 
		
		pvalue_independence(a) = stats.independent_pvalue;

		significant_pos_corr(a) = stats.independent_rej_pos;
		significant_neg_corr(a) = stats.independent_rej_neg;
		 
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


