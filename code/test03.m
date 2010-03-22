
% trying to do saccade analysis


log = load_log('data/data_Dmelanogaster-20080626-151946.mat');


interval = 1:10000;
interval = interval + 20000;
interval = 10000:20000;

lambda_max = l1tf_lambdamax(log.orientation(interval))
lambda = .000001 * lambda_max;


res = filter_orientation(log.timestamp(interval), log.orientation(interval), lambda);

res = detect_saccades(res);

detect_saccades_plot(res);