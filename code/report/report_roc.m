function report_roc(species_dir, conf_id, out_dir)
	perf = species_roc_curve(species_dir);

	f=sac_figure; 
	hold on;
	title('ROC')
	xlabel('False positive rate')
	ylabel('True positive rate')
	plot([0 1],[0 1],'k--')
	plot([0 1],[1 1],'k-')
	plot([1 1],[0 1],'k-')
	for i=1:numel(perf)
		x = perf(i).false_positive;
		y = perf(i).true_positive;
		if strcmp(perf(i).conf_id, conf_id)
			h = plot(x,y,'r.');
			set(h, 'MarkerSize', 12)
		else
			plot(x,y,'kx');
		end
		x1 = x+0.5;
		y1 = y-0.5;
		plot([x x1],[y y1],'g-')
		label = strrep(perf(i).conf_id, '_', '\_');
		text(x1, y1, label)
	end
	
	ftitle = 'ROC';
	basename = 'roc';
	sac_print(out_dir, basename, ftitle);
	
	close(f);
	