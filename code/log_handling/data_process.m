function run_all_species(data_directory, configurations)
%	function run_all_species(data_directory, configuration)
%
%    runs the processing on all the species with a given configuration
%
%    data_directory:  should contain species folders with name starting with 'D'.

d = dir(sprintf('%s/D*',data_directory));

if numel(d) == 0
	error(sprintf('Directory "%s" does not contain any species directory', data_directory))
end

for c=1:numel(configurations)
configuration = configurations(c);
for i=1:numel(d)
	species_directory = sprintf('%s/%s', data_directory, d(i).name);
	process_all_data(species_directory, configuration);
end
end



