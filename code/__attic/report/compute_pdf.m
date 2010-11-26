function [pdf, bins, fraction_excluded] = compute_pdf(samples, interval, numbins)
	% function pdf_plot(samples, bins)
	% 
	
	assert(numbins>1)
	
	% first of all, remove samples
	xmin = interval(1);
	xmax = interval(end);
	invalid = (samples <= xmin) | (samples >= xmax);
	valid = not(invalid);
	x = samples(find(valid));

	binsize = (xmax-xmin) / numbins;
	bins =  xmin:binsize:xmax;
	[N, bins] = hist(x, bins);
	pdf = (N / numel(x)) / binsize;
	
	if nargout == 3
		fraction_excluded = numel(invalid) / numel(samples);
	end
	
	