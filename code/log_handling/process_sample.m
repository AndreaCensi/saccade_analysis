function res = process_sample(filename, configuration)
	
	res = load_log(filename);  
	
	method = configuration.saccade_detection_method;
	if method == 'linear'
	    detected = detect_saccades_linear(res.timestamp, ...
	                                  res.orientation, ...
	                                  configuration);	
    % elseif method == 'ros'
    %     
    %     
    else
	   error(sprintf('I do not know the method "%s".', method)); 
    end
	                                  	
	% add additional information
	saccades = detected.saccades;
	for i=1:numel(saccades)
	    s = saccades(i);
		s.filename = filename;
		s.sample = res.sample;
		res.saccades(i) = s;
	end
	
	res.configuration = configuration;
	
	% add some tracking information
	res.info = get_configuration_info();
	    
    res = rmfield(res, 'timestamp');
    res = rmfield(res, 'orientation');


