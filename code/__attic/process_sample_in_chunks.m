function res = process_sample(filename, configuration)
	
	res = load_log(filename);
	
	n = numel(res.timestamp);
	
	chunk_length = 200000;
	num_chunks = ceil(n / chunk_length);
	
	for i = 1:num_chunks
		start = 1+ (i-1) * chunk_length;
		finish = min(start + chunk_length - 1, n);
		
		fprintf('file %s  chunk %d  [%d,%d] / %d \n', filename, i, start, finish, n)
		
		interval = start:finish;
		timestamp = res.timestamp(interval);
		orientation = res.orientation(interval);
	
		if strcmp(configuration.saccade_detection_method, 'l1tf')
			lambda_max = l1tf_lambdamax(orientation);
			lambda = configuration.lambda * lambda_max;
		
			res_chunk = filter_orientation(timestamp, orientation, lambda);
			res_chunk.min_significant_amplitude = configuration.min_significant_amplitude;
	        res_chunk = detect_saccades(res_chunk);
			res.chunk(i) = res_chunk; 
		elseif strcmp(configuration.saccade_detection_method, 'linear')
			res_chunk = detect_saccades_linear(timestamp, orientation, configuration);
			res.chunk(i) = res_chunk; 
		elseif strcmp(configuration.saccade_detection_method, 'mamarama')
			res_chunk = detect_saccades_mamarama(timestamp, orientation, configuration);
			res.chunk(i) = res_chunk; 
		else
			error(sprintf('Method "%s" not known',configuration.saccade_detection_method ) );
		end
			
			
		res.configuration = configuration;
    end
    
	ts = 1;
	for i = 1:num_chunks
		for np=1:numel(res.chunk(i).saccades)
			s = res.chunk(i).saccades(np); 
			s.species = res.species;
			s.filename = filename;
			s.sample = res.sample;
			res.saccades(ts) = s;
			ts = ts + 1;
		end
	end

    % TODO: at this point recompute the intra-saccade stats
