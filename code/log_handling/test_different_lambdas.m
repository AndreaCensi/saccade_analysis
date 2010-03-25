
lambdas = [1e-7 3e-7 5e-7 8e-7 1e-6 2e-6 3e-6 5e-6];
lambda_conf = [];
for i=1:numel(lambdas)
	lambda_conf(i).id = sprintf('test_lambda%d', i);
	lambda_conf(i).lambda = lambdas(i);
end

run_all_species('data', lambda_conf)