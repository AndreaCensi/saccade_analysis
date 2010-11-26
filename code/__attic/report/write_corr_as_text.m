function s = write_corr_as_text(R)
	m = size(R,1);
	n = size(R,2);
	s = '';
	
	col = 6;
	
	for i=1:m
		for j=1:n
			if i==j
				r='*';
			else
				val = round(R(i,j)*100);
				r = sprintf('%d%%', val);
			end
			
			while numel(r) < col
				r = sprintf(' %s', r);
			end
			
			s = sprintf('%s%s',s, r);
		end
		s = sprintf('%s\n',s);
	end
	