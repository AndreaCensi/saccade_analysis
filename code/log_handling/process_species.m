function process_species(directory, configuration)
	%  function process_species(species_dir, configuration)
	%
	%   directory: contains a bunch of data files with pattern 'data_*'
	%   configuration: contains the parameters for the saccades extraction
	%     configuration.id        name of the configuration
	%
	%  The output of the procedure is in a series of files in the directory
	%         <directory>/processed/<configuration.id>/*.mat
	%  
	%  If the configuration parameter is not given, we create a default configuration with id = 'default', lambda = 24
	
	use_cached_results = true;
	
	if nargin == 1
		configuration = default_configuration()
	end
	
	d = dir(sprintf('%s/data_*.mat',directory));

	for i=1:numel(d)
		filename = sprintf('%s/%s', directory, d(i).name);
		
		my_mkdir(sprintf('%s/processed', directory))
		out_dir = sprintf('%s/processed/%s', directory, configuration.id);
		my_mkdir(out_dir)
		out_filename = sprintf('%s/processed_%s', out_dir, d(i).name);
		
		if exist(out_filename, 'file') & use_cached_results
			fprintf('Using cached results for %s \n', out_filename)
		else
			res = process_sample(filename, configuration);
			save(out_filename,'res');
		end
		 
	end

	save(sprintf('%s/configuration.mat', out_dir), 'configuration');
	saccades = gather_all_data(out_dir);

	save(sprintf('%s/saccades.mat', out_dir), 'saccades');
	

function saccades = gather_all_data(directory)
	% function saccades = gather_all_data(directory)
	%
	%  Iterates over all files of pattern 'processed_*mat' in the directory
	%  and collects all the saccades together for further analysis.

	d = dir(sprintf('%s/processed_*.mat',directory));

	ns = 1;
	for i=1:numel(d)
		filename = sprintf('%s/%s', directory, d(i).name);
		fprintf('Reading %s...\n' , filename);
		a = load(filename);
		this_saccades = a.res.saccades;
		% copy in the big array
		for j=1:numel(this_saccades)
            this_saccades(j).filename = filename;
			saccades(ns) = this_saccades(j);
			ns = ns + 1;
		end
	end

    