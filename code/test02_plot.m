function test02_plot(results)
	% results: returned from "test02"

	L = [results.lambda];
	R = [results.rmse];
	E = [results.energy];

	f = figure(12);
	subplot(3,1,1)
	semilogx(L, R);
	ylabel('rmse')
	xlabel('fraction of lambda max')

	subplot(3,1,2)
	semilogx(L,  E)
	ylabel('energy')
	xlabel('fraction of lambda max')

	f = figure(13);
	loglog( E, R)
	xlabel('energy')
	ylabel('fit')


	f = figure(14); hold off
	n=numel(results);
	subplot(n+1,1,1)
	plot( results(1).filter_res.orientation, 'b-')
	legend('original')
	
	for i=1:n
		subplot(n+1,1,i+1)
		plot( results(i).filter_res.filtered_orientation, 'r-')
		legend(sprintf(' lambda = %f ', results(i).lambda))
	end
