function [all_samples, saccades] = add_sample_num(saccades)
	% [all_samples, saccades] = add_sample_num(saccades)
	%
	%  all_samples: cell of strings
	
	all_samples = unique( {saccades.sample} );
	for i=1:numel(saccades)
		for a=1:numel(all_samples)
			if strcmp(all_samples{a}, saccades(i).sample)
				saccades(i).sample_num = a;
			end
		end	
	end