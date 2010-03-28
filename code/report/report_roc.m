function report_roc(species_dir, conf_id, out_dir)
	basename = 'roc';
	
	if report_should_I_skip(out_dir, basename), return, end
	
	roc_analysis_file = path_join(out_dir, 'roc_analysis.mat');
	if exist(roc_analysis_file, 'file')
		fprintf('Using cached %s \n ', roc_analysis_file);
		load(roc_analysis_file)
	else
		roc_analysis = roc_analysis_species(species_dir);
		save(roc_analysis_file, 'roc_analysis');
	end
	
	configuration_file = sprintf('%s/processed/%s/configuration.mat', species_dir, conf_id);
	load(configuration_file);
	conf_id = configuration.id
	
	f=sac_figure; 
	hold on;
	title('ROC')
	xlabel('False positive rate')
	ylabel('True positive rate')
%	plot([0 1],[0 1],'k--')
%	plot([0 1],[1 1],'k-')
%	plot([1 1],[0 1],'k-')
	for i=1:numel(roc_analysis)
		x = roc_analysis(i).false_positive;
		y = min(roc_analysis(i).true_positive,1);
		if not(strcmp(roc_analysis(i).conf_id, conf_id))
			h = plot(x,y,'k.');
			set(h, 'MarkerSize', 8)
		end
	end
	
	for i=1:numel(roc_analysis)
		x = roc_analysis(i).false_positive;
		y = min(roc_analysis(i).true_positive,1);
		if strcmp(roc_analysis(i).conf_id, conf_id)
			h = plot(x,y,'r.');
			set(h, 'MarkerSize', 12)
		end
	end

%		x1 = x+0.5;
%		y1 = y-0.5;
%		plot([x x1],[y y1],'g-')
%		label = strrep(roc_analysis(i).conf_id, '_', '\_');
%		text(x1, y1, label)
	
	a = axis();
	a(1) = 0;
	a(2) = 0.08;
	a(3) = 0.87;
	a(4) = 1.01;
	
	axis(a);
	drawnow

	ftitle = 'ROC';
	sac_print(out_dir, basename, ftitle);
	close(f);
	