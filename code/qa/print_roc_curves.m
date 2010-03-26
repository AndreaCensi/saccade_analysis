function print_roc_curve(perf)	
	f=figure; hold on;
	title('ROC')
	xlabel('False positive rate')
	ylabel('True positive rate')
	plot([0 1],[0 1],'k--')
	plot([0 1],[1 1],'k-')
	plot([1 1],[0 1],'k-')
	
	o = [perf.true_positive] - 0.1 * [perf.false_positive];
	[Y,sorted_indices] = sort(o, 'ascend')

	for a=1:numel(sorted_indices)
		i = sorted_indices(a);
		x = perf(i).false_positive;
		y = perf(i).true_positive;
	
		h = plot(x,y,'k.');
%		set(h, 'MarkerSize', 15)
		
		x1 = 0.5;
		y1 = 0.7 - 0.05 * a;
		plot([x x1],[y y1],'g-')
		label = strrep(perf(i).conf_id, '_', '\_');
		text(x1, y1, label)
	end
