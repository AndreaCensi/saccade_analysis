function points = roc_analysis_species(species_dir)
	% function points = roc_analysis_species(species_dir)
	%  get all configuration that we used for this species
	processed_dir = path_join(species_dir, 'processed');
	d = dir(processed_dir);
	% 
	np=1;
	for i=1:numel(d)
		conf_id = d(i).name;
		if conf_id(1) == '.' % skip '.','..', etc.
			continue
		end
		fprintf('Computing for %s - conf %s...\n', species_dir, conf_id)
		res = roc_analysis_species_conf(species_dir, conf_id, false);
		points(np).verify_precision_res = res;
		points(np).false_positive = res.false_positive;
		points(np).true_positive = res.true_positive;
		points(np).false_negative = res.false_negative;
		points(np).conf_id = conf_id;
		np = np + 1;
	end
	
	
