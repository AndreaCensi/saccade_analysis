function sac_sign_overview(saccades, out_dir)
	basename = 'sac_sign_overview';
	if report_should_I_skip(out_dir, basename), return, end

	[all_samples, saccades] = add_sample_num(saccades);
	num_samples = numel(all_samples);
	
	width = 100;
	M = [];
	pad = zeros(1,width);
	
	for a=1:num_samples
		sample_saccades = saccades([saccades.sample_num] == a);
	
		S = [sample_saccades.sign];
		Ma = reshape_fluid(S, width);
		M = [M;pad;Ma]; 
	end
	
	f=sac_figure(33);  
	hold on
	ftitle='Sign overview';
%	axis('off')
	imagesc(M);
	sac_print(out_dir,basename, ftitle);
	close(f); 

