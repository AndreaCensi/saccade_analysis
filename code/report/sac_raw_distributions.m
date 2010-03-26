function sac_raw_distribution(species_dir, report_dir)

 	if report_should_I_skip(report_dir, 'sac_raw_orientation'), return, end
		

	logs = load_all_samples_for_species(species_dir);

	orientation = [];
	for i=1:numel(logs)
		orientation = [orientation; logs(i).orientation];
	end
	
	fprintf('Total %d samples\n', numel(orientation));
	
	orientation = mod(orientation, 360);
	
	f=sac_figure(34);
	hist(orientation,360)
	xlabel('orientation (deg)')
	ylabel('density')
	ftitle = 'Orientation histogram';
	title(ftitle)
	sac_print(report_dir, 'sac_raw_orientation', ftitle)
	
	close(f)