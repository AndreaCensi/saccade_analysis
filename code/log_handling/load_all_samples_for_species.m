function res = load_all_samples_for_species(species_dir)
% function res = load_all_samples_for_species(species_dir)
%
%  loads all data in a directory (files data_* )
	d = dir(sprintf('%s/data_*.mat',species_dir));
	for i=1:numel(d)
		filename = sprintf('%s/%s', species_dir, d(i).name);
%		fprintf('Reading %s...\n' , filename);
		res(i) = load_log(filename);
	end