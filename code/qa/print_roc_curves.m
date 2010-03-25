function print_roc_curve(perf)	
	f=figure; hold on;
	title('ROC')
	xlabel('False positive rate')
	ylabel('True positive rate')
	plot([0 1],[0 1],'k--')
	plot([0 1],[1 1],'k-')
	plot([1 1],[0 1],'k-')
	for i=1:numel(perf)
		x = perf(i).false_positive;
		y = perf(i).true_positive;
		
		plot(x,y,'x');
		text(x+0.05, y-0.05, perf(i).conf_id)
	end

	% axis([0 1 0 1])