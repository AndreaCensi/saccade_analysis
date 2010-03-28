function sac_interval_analysis(saccades, out_dir)

	basename=sprintf('sac_interval_analysis');
	if report_should_I_skip(out_dir, basename), return, end

	f = sac_figure;
	hold on
	
	samples = [saccades.time_passed];
	
	samples = samples(find(samples>0));
	
	from = 0;
	to = 8;
	nbins = 100;
	
	[pdf, bins, fraction_excluded] = compute_pdf(samples, [from to], nbins);
	
	
	[peak_value, peak_indx] = max(pdf);
	peak = bins(peak_indx);

	[muhat, muci] = expfit(samples);
	
%	my_muhat = 1/mean(samples)
	
	start2 = peak;
	samples2=samples(samples>start2);
	[muhat2, muci] = expfit(samples2-start2);

	start3 = 3*peak;
	samples3=samples(samples>start3);
	[muhat3, muci] = expfit(samples3);
	
	mu1 = exponential_fit(bins,pdf,0);
	mu2 = exponential_fit(bins,pdf,start2);
	mu3 = exponential_fit(bins,pdf,start3);
	
%	fprintf(' muhat: %f   mu1: %f \n', muhat, mu1);
	
	h(1)=plot(bins, exppdf(bins, mu1), 'k-');
%	h(2)=semilogx(bins, exppdf(bins-start2, muhat2), 'r-');
%	h(3)=semilogx(bins, exppdf(bins-start3, muhat3), 'g-');
	h(2)=plot(bins, exppdf(bins, mu2), 'r-');
	h(3)=plot(bins, exppdf(bins, mu3), 'g-');
	g=plot(bins, pdf, 'b.');
	set(g,'MarkerSize',6);
%	for i=1:3, set(h(i), 'linewidth', 1), end

	legend('exp. fit', 'exp. fit (>peak)', 'exp. fit (tail)', 'data')
	a=axis(); 
		a(1)=from; a(2)=to;
		a(3) = 0;
		a(4) = 1.1;
	axis(a);
	
	ylabel('density')
	xlabel(sprintf('Interval (s)'))
	ftitle=sprintf('Interval p.d. exponential fit');
	
	sac_print(out_dir, basename, ftitle);
	close(f)

function err = exp_err(x,y,lambda)
	err = 0;
	for i=1:numel(x)
		err = err +  (y(i) - lambda * exp(-lambda * x(i) ))^2;
	end
	
function mu = exponential_fit(bins,pdf,censor)
	valid = bins>censor;
	bins = bins(valid);
	pdf = pdf(valid);
	
	mean = sum(bins .* pdf);
	lambda0 = 1 ;
	lambda = fminsearch( @(lambda) exp_err(bins,pdf,lambda), lambda0);
	
	mu = 1/lambda;
%	fprintf(' Lambda censor=%f  %f -> %f \n',censor,lambda0, lambda )
	
	
	
	