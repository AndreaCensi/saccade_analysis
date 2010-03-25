function points = species_roc_curve(species_dir)
	% get all configuration that we used for this species
	processed_dir = path_join(species_dir, 'processed');
	d = dir(processed_dir);
	% 
	np=1;
	for i=1:numel(d)
		conf_id = d(i).name;
		if conf_id(1) == '.'
			continue
		end
		fprintf('Computing for %s - conf %s...\n', species_dir, conf_id)
		%conf_dir = path_join(processed_dir, d(i).name);
		%l = load(path_join(conf_dir, 'saccades.mat'));
		%saccades = l.saccades;
		res = verify_precision(species_dir, conf_id);
		points(np).verify_precision_res = res;
		points(np).false_positive = res.false_positive;
		points(np).true_positive = res.true_positive;
		points(np).false_negative = res.false_negative;
		points(np).conf_id = conf_id;
		np = np + 1;
	end
	
	
