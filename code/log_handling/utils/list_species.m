function species = list_species(data_directory)
	% species = list_species(data_dir)
	%   Lists all species in the given data directory.
	%   Returns a cell-array of strings.
	
	d = dir(sprintf('%s/D*',data_directory));

	if numel(d) == 0
		error(sprintf('Directory "%s" does not contain any species directory', data_directory))
	end

	for i=1:numel(d)
		species{i} = d(i).name;
	end
	
