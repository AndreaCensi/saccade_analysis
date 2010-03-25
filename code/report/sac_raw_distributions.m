function sac_raw_distribution(directory, report_dir)

	logs = load_all_data(directory);

	orientation = [];
	for i=1:numel(logs)
		orientation = [orientation; logs(i).orientation];
	end
	
	fprintf('Total %d samples\n', numel(orientation));
	
	orientation = mod(orientation, 360);
	
	f=figure(34);
	hist(orientation,360)
	
	print('-depsc2', sprintf('%s/sac_raw_orientation.eps', report_dir));
	


function res = load_all_data(directory)
% loads all data in a directory (files data_* )
	d = dir(sprintf('%s/data_*.mat',directory));
	for i=1:numel(d)
		filename = sprintf('%s/%s', directory, d(i).name);
		fprintf('Reading %s...\n' , filename);
		res(i) = load_log(filename);
	end