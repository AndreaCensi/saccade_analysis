function res = compute_seq_statistics_test()
	sequence_length = 1000;
	num_sequences = 1000;
	
	% generate data from independent bernouilli
	num_rejected = 0;
 
	for i=1:num_sequences
		independent(i).r = rand_uniform(0.1, 0.9);
		independent(i).sequence = generate_independent(sequence_length, independent(i).r);
		independent(i).letters = seq2letters(independent(i).sequence );
		independent(i).analysis = compute_seq_statistics(independent(i).letters);
		if independent(i).analysis.independent_rejected
			num_rejected = num_rejected + 1;
			
			fprintf('r = %f\n%s\n', independent(i).r, independent(i).analysis.independent_desc);
		end
	end
	
	fprintf('Rejected independences: %d / %d = %f \n', num_rejected, num_sequences, ...
		num_rejected / num_sequences);
	
	for i=1:num_sequences
	end
	
	res = struct;
	res.independent = independent;
	res.num_rejected = num_rejected;
	res.num_sequences = num_sequences;
	
	
function r = rand_uniform(lower, upper)
	r = lower + (upper-lower) * rand;

function v = rand_bernouilli(r)
	v = rand < r;
	
function seq = generate_independent(num, r)
	for i=1:num
		seq(i) = rand_bernouilli(r);
	end
	
function letters = seq2letters(seq)
	for i=1:numel(seq)
		if seq(i)
			letters(i) = 'L';
		else
			letters(i) = 'R';
		end
	end
