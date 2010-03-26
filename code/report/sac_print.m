function sac_print(report_dir, basename, ftitle)
	title(ftitle);
	print('-depsc2', path_join(report_dir, sprintf('%s.eps', basename) ));
	f = fopen(path_join(report_dir, sprintf('%s.title', basename) ), 'w');
	fprintf(f, '%s', ftitle);
	fclose(f);