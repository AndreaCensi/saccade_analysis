function skip = report_should_I_skip(report_dir, basename)
% function res = report_should_I_skip(report_dir, basename)
%
%  Returns true if the output image  basename+.eps is already present
%  and skipping is enabled.

	skip_if_possible = true;

	output_file =  path_join(report_dir, sprintf('%s.eps', basename) );
	file_is_there = exist(output_file, 'file');
	
	skip = file_is_there & skip_if_possible;
	
	if skip
	%	fprintf('Skipping creation of %s. \n', basename)
	else
		fprintf('Creating %s  %s \n', report_dir, basename)
	end