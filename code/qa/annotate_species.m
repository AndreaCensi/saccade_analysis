function annotate_species(species_dir)
% function annotate_species(species_dir)
%
% Annotates the data in directory

display_interval_s = 4;

logs = load_all_samples_for_species(species_dir);

fprintf('- Click twice to mark a saccade: at the beginning and the end. \n')
fprintf('- When you are done, press enter to go to the next screen. \n')
fprintf('- When you want to exit, press "x"+enter without clicking any point. \n')
fprintf('- If you want to undo the previous selection, press "u" + enter.  \n')

nd = 1;

while true
	% choose a random log
	i = rand_in(1, numel(logs));
	
	% choose a random time
	timestamp = logs(i).timestamp; 
	orientation = logs(i).orientation; 
	dt = timestamp(2)-timestamp(1);
	display_interval_steps = ceil(display_interval_s / dt); 
	K = numel(timestamp);
    
    if K < 3*display_interval_steps
       T = K * dt;
       fprintf('Log is too small (%.1f seconds). Skipping. \n.', T);
       continue
    end
	k = rand_in(1+display_interval_steps, K-display_interval_steps-10);
	
	from = k - display_interval_steps;
	to = k + display_interval_steps;
%	orientation0 = orientation(from);
	
	f = figure(32); 
	set(f, 'Position', [100 200 1000 400])
	hold off
	plot(timestamp(from:to), orientation(from:to) , 'r.')
	xlabel('time (s)')
	ylabel('orientation (deg)')
	a = axis();
	min_y = 180;
	if abs(a(4)-a(3)) < min_y
		a(3) = a(3) - min_y / 2;
		a(4) = a(4) + min_y / 2;
		axis(a)
	end
	
	annotations(nd).species = logs(i).species;
	annotations(nd).sample = logs(i).sample;
	annotations(nd).filename = logs(i).filename;
	annotations(nd).from = from;
	annotations(nd).to = to;
	annotations(nd).from_ts = timestamp(from);
	annotations(nd).to_ts = timestamp(to);
%	annotations(nd).orientation0 = orientation0;
	annotations(nd).saccades = [];

	finished = false;
	
	while true
		hold off
		plot(timestamp(from:to), orientation(from:to), 'r.')
		hold on
		plot_saccade_delimiters(annotations(nd).saccades, 100)
		axis(a)
		drawnow
		
		[x,y, u] = ginput(2);
	
		% exit when pressing 'x'
		if any(u == 120)
			fprintf('X pressed. Finishing...\n')
			finished = true;
			break
		end
		
		% undo the previous one 
		if any(u == 117)
			if numel(annotations(nd).saccades) == 0
				fprintf('! Could not undo: this is the first selection. \n')
				continue
			end
			fprintf('undoing the previous selection.\n')
			annotations(nd).saccades(end) = [];
			continue
		end
	
		if numel(x) == 0
			fprintf('Finished for this screen. \n')
			break
		end
		
		if not(numel(x) == 2)
			fprintf('I expect two points!\n')
			continue
		end
		
		if x(2) < x(1)
%			fprintf('Please click first the start and then the end point.\n')
			x = x([2 1]);
			y = y([2 1]);
		end
		sac = numel(annotations(nd).saccades) + 1;
		annotations(nd).saccades(sac).time_start = x(1);
		annotations(nd).saccades(sac).time_stop = x(2);
		annotations(nd).saccades(sac).orientation_start = y(1);
		annotations(nd).saccades(sac).orientation_stop = y(2);
	end
	
	if finished
		% remove last one
		annotations(end) = [];
		break
	end
	
	annotations(nd)
	
	nd = nd + 1;
end

fprintf('Recorded a total of %d screens. \n', numel(annotations))
mkdir(species_dir,'qa')
time = datestr(now, 'yyyymmdd-HHMMSS');
filename = sprintf('%s/qa/qa_%s.mat', species_dir, time );
save(filename,'annotations')

fprintf('Results saved as %s\n', filename)

fprintf('Thanks for helping!\n')
close(f)

function r = rand_in(from, to)
% returns a random integer between from an to	
	r = max(from, min(to, round(from + rand * (to-rand)) ));	

function plot_saccade_delimiters(saccades, ybarsize)
	% expects saccades.time_start, saccades.time_stop, orientation_start, orientation_stop
	
	for i=1:numel(saccades)
		x1 = saccades(i).time_start;
		y1 = saccades(i).orientation_start;
		x2 = saccades(i).time_stop;
		y2 = saccades(i).orientation_stop;

		plot( [x1 x1], [y1-ybarsize y1+ybarsize] , 'g-')
		plot( [x2 x2], [y2-ybarsize y2+ybarsize] , 'b-')
		plot( [x1 x2], [y1-ybarsize y2-ybarsize] , 'r-')
	end	
	
		
