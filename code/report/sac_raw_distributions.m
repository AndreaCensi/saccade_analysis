function sac_raw_distribution(species_dir, report_dir)

	logs = species_load_all_exp_data(species_dir);

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