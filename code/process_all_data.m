function process_all_data(directory)
	%  directory contains a bunch of data files
	d = dir(sprintf('%s/data_Dmelanogaster-*.mat',directory));

	for i=1:numel(d)
%	for i=1
		filename = sprintf('%s/%s', directory, d(i).name);
		res = process_sample(filename);

		out_filename = sprintf('%s/processed_%s', directory, d(i).name);
		save(out_filename,'res');
	end

function res = process_sample(filename)
	res = load_log(filename);
	
	n = numel(res.timestamp);
	
	chunk_length = 10000;
	num_chunks = ceil(n / chunk_length);
	
	for i = 1:num_chunks
		start = 1+ (i-1) * chunk_length;
		finish = min(start + chunk_length - 1, n);
		
		fprintf('file %s  chunk %d  [%d,%d] / %d \n', filename, i, start, finish, n)
		
		interval = start:finish;
		timestamp = res.timestamp(interval);
		orientation = res.orientation(interval);
	
		lambda_max = l1tf_lambdamax(orientation);
		lambda = .000001 * lambda_max;
		res_chunk = filter_orientation(timestamp, orientation, lambda);
		res.chunk(i) = detect_saccades(res_chunk);
    end
    
	ts = 1;
	for i = 1:num_chunks
		for np=1:numel(res.chunk(i).saccades)
			res.saccades(ts) = res.chunk(i).saccades(np);
			ts = ts + 1;
		end
	end


    