function sac_report_all(directory)
	% function sac_report_all(directory)
	%
	%  Runs all the report generators.
	%  loads       directory/saccades.mat
	%  output in   directory/report/
	load(sprintf('%s/saccades.mat', directory))
	mkdir(directory, 'report')
	out_dir=sprintf('%s/report', directory)
	
	
	
	sac_raw_distributions(directory, out_dir)
	return
	
	markov_analysis(saccades, out_dir)
	sac_correlation(saccades, out_dir)
	sac_distributions(saccades, out_dir)
	sac_corr_start_and_sign(saccades, out_dir)