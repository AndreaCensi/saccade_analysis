function process_data(data_dir, configurations)
%	function process_data(data_directory, configuration)
%
%    runs the processing on all the species with a given configuration
%
%    data_directory:  should contain species folders with name starting with 'D'.

species = list_species_in_data(data_dir);

for c=1:numel(configurations)
	configuration = configurations(c);
	for i=1:numel(species)
		species_directory = path_join(data_dir, species{i});
		process_species(species_directory, configuration);
	end
end



