function report_species(species_dir, conf_id)
	% function species_report(species_dir, conf_id)
	%
	%  Runs all the report generators.
	%  loads       directory/saccades.mat
	%  output in   directory/report/
	
	load(sprintf('%s/processed/%s/saccades.mat', directory, conf_id))
	mkdir(directory, 'report')
	out_dir = path_join(species_dir, 'report')
	
	sac_raw_distributions(species_dir, out_dir)
	
	markov_analysis(saccades, out_dir)
	sac_correlation(saccades, out_dir)
	sac_distributions(saccades, out_dir)
	sac_corr_start_and_sign(saccades, out_dir)