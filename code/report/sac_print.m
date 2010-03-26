function sac_print(report_dir, basename, ftitle)
	title(ftitle);
	output_file =  path_join(report_dir, sprintf('%s.eps', basename) );
	print('-depsc2', output_file);
	f = fopen(path_join(report_dir, sprintf('%s.title', basename) ), 'w');
	fprintf(f, '%s', ftitle);
	fclose(f);