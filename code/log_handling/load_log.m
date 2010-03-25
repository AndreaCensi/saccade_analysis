function res = load_log(filename)
	% Load and prepare data from a log file
	%
	%  res.t0            absolute date 
	%  res.timestamp     starts from 0
	%  res.orientation
	%  res.species
	%  res.sample
	
	content = load(filename);
	data = content.data;
	res.species = data.species;
	res.sample = data.sample;
	exp_timestamps = data.exp_timestamps';
		res.t0 = exp_timestamps(1);
		res.timestamp = exp_timestamps - res.t0;
	res.orientation = data.exp_orientation';
	res.filename = filename;