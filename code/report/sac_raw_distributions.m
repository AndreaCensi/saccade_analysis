function sac_raw_distribution(species_dir, report_dir)

	logs = species_load_all_exp_data(species_dir);

	orientation = [];
	for i=1:numel(logs)
		orientation = [orientation; logs(i).orientation];
	end
	
	fprintf('Total %d samples\n', numel(orientation));
	
	orientation = mod(orientation, 360);
	
	f=figure(34);
	hist(orientation,360)
	
	print('-depsc2', sprintf('%s/sac_raw_orientation.eps', report_dir));
