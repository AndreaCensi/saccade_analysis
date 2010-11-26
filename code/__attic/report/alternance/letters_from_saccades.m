function letters = letters_from_saccades(saccades)
	for i=1:numel(saccades)
		if saccades(i).sign > 0
			letters(i) = 'L';
		else
			letters(i) = 'R';
		end
	end