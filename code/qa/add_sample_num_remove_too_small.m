function [selected_samples, saccades] = add_sample_num_remove_too_small(saccades, N)
	% [all_samples, saccades] = add_sample_num_remove_too_small(saccades, N)
	%
	%  all_samples: cell of strings
	%
	%  does not consider samples with few saccades
	
	all_samples = unique( {saccades.sample} );
	selected_samples = {};

	for a=1:numel(all_samples)
		k = 0;
		for i=1:numel(saccades)
			if strcmp(all_samples{a}, saccades(i).sample)
				k = k + 1;
			end
		end	

		if k > N
			selected_samples{end+1} = all_samples{a};
			id = numel(selected_samples);
			fprintf('Accepting sample %s with %d saccades, id = %d.\n',...
				all_samples{a}, k, id); 
			for i=1:numel(saccades)
				if strcmp(all_samples{a}, saccades(i).sample)	
					saccades(i).sample_num = id;
				end
			end
		else
			fprintf('Discarding sample %s with %d < %d saccades.\n', all_samples{a},...
				k, N);
		end
	end

