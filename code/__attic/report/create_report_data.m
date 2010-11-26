function create_report_data(data_dir, conf_id)
	species = list_species_in_data(data_dir);
	
	for i=1:numel(species)
		species_dir = path_join(data_dir, species{i});
		create_report_species(species_dir, conf_id);
	end