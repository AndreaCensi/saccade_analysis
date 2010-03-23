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
			saccades(ns) = this_saccades(j);
			saccades(ns).filename = filename;
			ns = ns + 1;
		end
	end
	