function results = test02
	% this test shows to show the difference in using different lambdas
	content = load('data/data_Dmelanogaster-20080410-174953');
	data = content.data;
	species = data.species;
	sample = data.sample;
	exp_timestamps = data.exp_timestamps';
	exp_timestamps = exp_timestamps - exp_timestamps(1);
	exp_orientation = data.exp_orientation';

    T = numel(exp_timestamps);
	interval = 1:ceil(T/20);
    
	
	timestamps = exp_timestamps(interval);
	orientation = exp_orientation(interval);

	lambdamax = l1tf_lambdamax(orientation)
%	lambdas = [0.3, 0.1, 0.03, 0.001, 0.0001, 0.00001];
%	lambdas = [0.001];
	lambdas = [0.0005 0.0003 0.0002 0.0001 0.00005 .000025 .00001];
	results = struct;
	
	for i=1:numel(lambdas)
		lambda = lambdas(i) * lambdamax;
		results(i).filter_res = l1filter(timestamps, orientation, lambda);
		results(i).lambda  = lambdas(i);
		results(i).lambda_scaled  = lambda;
		
		results(i).rmse  = results(i).filter_res.rmse;
		results(i).energy = results(i).filter_res.energy;
	end

	
	