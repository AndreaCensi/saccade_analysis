function create_report_species(species_dir, conf_id)
	% function species_report(species_dir, conf_id)
	%
	%  Runs all the report generators.
	%  loads       directory/processed/<conf_id>/saccades.mat
	%  output in   directory/report/
	
	
	load(sprintf('%s/processed/%s/saccades.mat', species_dir, conf_id));

%	[all_samples, saccades] = add_sample_num(saccades);

	out_dir = path_join(species_dir, 'report');
	my_mkdir(out_dir);

	% Sep'10: temporarely disabled
	% report_roc(species_dir, conf_id, out_dir);
	% sac_raw_distributions(species_dir, out_dir);
	markov_analysis(saccades, out_dir);
	sac_correlation(saccades, out_dir);
	sac_distributions(saccades, out_dir);
	sac_corr_start_and_sign(saccades, out_dir);
	
	sac_interval_analysis(saccades, out_dir);
	
	sac_plot_virtual_trajectories(saccades, out_dir);
	sac_sign_overview(saccades, out_dir);
	sac_sign_statistics(saccades, out_dir);