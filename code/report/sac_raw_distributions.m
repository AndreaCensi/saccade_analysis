function sac_raw_distribution(species_dir, report_dir)

 	if report_should_I_skip(report_dir, 'sac_raw_orientation'), return, end
		
	logs = load_all_samples_for_species(species_dir);


	f=sac_figure(34); hold on
	colors={'r','g','b','k','m'};
	for i=1:numel(logs)
		orientation = mod(logs(i).orientation,360);
		bins=1:5:360;
		[a,bins]=hist(orientation,bins);
		density = a / (bins(2)-bins(1));
		color_index = 1 + mod(i-1, numel(colors));
		plot(bins, density, colors{color_index});
		xlabel('orientation (deg)')
		ylabel('density (samples/deg)')	
		a=axis;
	end
	ftitle = 'Orientation histogram per log';
	title(ftitle)
	sac_print(report_dir, 'sac_raw_orientation_sample', ftitle)
	close(f)
	


	orientation = [];
	for i=1:numel(logs)
		orientation = [orientation; logs(i).orientation];
	end
	
	fprintf('Total %d samples\n', numel(orientation));
	
	orientation = mod(orientation, 360);
	
	f=sac_figure(34);
	[a,bins]=hist(orientation,360);
	density = a / (bins(2)-bins(1));
	plot(bins, density, 'b-');
	xlabel('orientation (deg)')
	ylabel('density (samples/deg)')	
	a=axis;
	a(1)=0;
	a(2)=360;
	a(3)=0;
	a(4)=50000;
	axis(a)
%	axis([0 360 0 30000/360])
	ftitle = 'Orientation histogram';
	title(ftitle)
	sac_print(report_dir, 'sac_raw_orientation', ftitle)
	
	close(f)