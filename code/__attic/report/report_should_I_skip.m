function skip = report_should_I_skip(report_dir, basename)
% function res = report_should_I_skip(report_dir, basename)
%
%  Returns true if the output image  basename+.eps or the text file (+.txt) is already present
%  and skipping is enabled.

	skip_if_possible = true;

	output_file1 =  path_join(report_dir, sprintf('%s.eps', basename) );
	output_file2 =  path_join(report_dir, sprintf('%s.txt', basename) );
	file_is_there = exist(output_file1, 'file') |  exist(output_file2, 'file') ;
	
	skip = file_is_there & skip_if_possible;
	
	if skip
	%	fprintf('Skipping creation of %s. \n', basename)
	else
		fprintf('Creating %s  %s \n', report_dir, basename)
	end