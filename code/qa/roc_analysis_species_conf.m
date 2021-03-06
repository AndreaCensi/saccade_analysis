function species_res = roc_analysis_species_conf(directory, configuration_id, display)
	% function species_res = roc_analysis_species_conf(species_dir, conf_id, display)
	% 
	%  loads saccades.mat from 
	%      <species_dir>/processed/<configuration_id>
	%  and compares from the hand-annotated files in
	%      <species_dir>/qa/*mat
	%
	%  if display is true, interactively display failures
	%
	%  if configuration_id is omitted, it deafults to 'default'.
	%  if display is omitted, it defaults to 'false'.
	
	if nargin < 2
		configuration_id = 'default';
	end
	if nargin < 3
		display = false;
	end
	
	% we don't consider annotations which are closer to the annotation screen margin
	marking_safety = 1;
	% ignore errors if the annotated saccade is less than this
	minimum_significant_amplitude = 7;
	
	% display interval
	delta = 5; 
	display_misses = display;
	display_extra = display;
	
	
	saccades_files = sprintf('%s/processed/%s/saccades.mat', directory, configuration_id);
	l = load(saccades_files);
	saccades = l.saccades;
	
	
	annotations = load_all_qa_data(sprintf('%s/qa',directory));
    for i=1:numel(annotations)
    % jul10, mamarama data: annotated some samples with the wrong naming convention
        if strcmp(annotations(i).sample(end-3:end), '.fh5')
            annotations(i).sample = annotations(i).sample(5:end-4);
        end    
    end
%	fprintf('Found %d annotations.\n', numel(annotations));
%	a = load(sprintf('%s/saccades.mat', directory));
%	saccades = a.saccades;

	annotated_samples = unique({annotations.sample});
	
	species_res.num_missed = 0;
	species_res.num_annotated = 0;
    species_res.num_detected_where_annotated = 0;
    species_res.num_extra = 0;

	for i=1:numel(annotated_samples)
		sample = annotated_samples{i}; 
		original = load(sprintf('%s/data_%s.mat', directory, sample));
		timestamp =  original.data.exp_timestamps;
		orientation = original.data.exp_orientation;
%		fprintf('Timestamp %f - %f\n' , timestamp(1), timestamp(end));
		
	
		annotations_for_sample = select_specific_sample(annotations, sample);
		saccades_for_sample = select_specific_sample(saccades, sample);
		
		saccades_for_sample = fix_saccades_timestamp(timestamp, saccades_for_sample);
			
%		fprintf('Sample %s: %d annotations, %d detected.\n', sample, numel(annotations_for_sample), numel(saccades_for_sample))
		
		
		% We keep two arrays that we use to detect hit & misses
        K = numel(timestamp);
		% This is initially 0 and it gets marked for each annotated saccade
		marked_saccade = zeros(K,1);
		
		% This is normally 0 and it gets marked for each saccade detected
		detected_saccade =  zeros(K,1);
		detected_saccade = mark_saccades(saccades_for_sample, timestamp, detected_saccade);
		
		% mark excluded
		for a=1:numel(annotations_for_sample)
			% It's hard to mark the saccades at beginning and end of the screen
			from = timestamp2index(timestamp, annotations_for_sample(a).from_ts + marking_safety);
			to = timestamp2index(timestamp, annotations_for_sample(a).to_ts-marking_safety);
			
			previous = max(marked_saccade(from:to));
			if previous > 0
				fprintf('Found overlap in QA data (annotation %d and previous %d in sample %s).\n', a, previous, annotations_for_sample(a).sample)
				annotations_for_sample(a).ignore = true;
			else
				annotations_for_sample(a).ignore = false;
			end
			marked_saccade(from:to) = -1;
		end
		% mark annotated
		for a=1:numel(annotations_for_sample)
			if annotations_for_sample(a).ignore
				continue
			end
			annotations_for_sample(a).saccades = fix_saccades_timestamp(timestamp, ...
			    annotations_for_sample(a).saccades);
			marked_saccade = mark_saccades(annotations_for_sample(a).saccades, timestamp, marked_saccade);
		end

		already_counted = zeros(numel(saccades_for_sample),1);
		
		sample_res.num_missed = 0;
		sample_res.num_annotated = 0;
		
		% count the number of saccades we missed
		for a=1:numel(annotations_for_sample)
			if annotations_for_sample(a).ignore
				continue
			end
			
			for s=1:numel(annotations_for_sample(a).saccades)
				ann_saccade = annotations_for_sample(a).saccades(s);
				middle_time = mean([ann_saccade.time_start ann_saccade.time_stop]);
				middle_index = timestamp2index(timestamp, middle_time);
				index_start = timestamp2index(timestamp, ann_saccade.time_start );
				index_stop = timestamp2index(timestamp, ann_saccade.time_stop );
				
				amplitude = abs(orientation(index_start)-orientation(index_stop));
				% ignore annotated saccades less that the significant amplitude
				if amplitude < minimum_significant_amplitude
					continue
				end
					
				sample_res.num_annotated = sample_res.num_annotated + 1;
				 
				missed = false;
				% only check the middle
				% ds  = detected_saccade(middle_index);
				ds = max(detected_saccade(index_start:index_stop) );
				if ds == 0
					% we missed this
					if display_misses
						fprintf('\tMissed.\n')
					end
					missed = true;
				else 
					% check we didn't count it
					if already_counted( ds )
						if display_misses
							fprintf('\tMissed (already counted).\n')
						end
						% we missed this
						% Jul 2010, this is not relevant to mamarama
						% missed = true;
					else
						already_counted( ds ) = already_counted( ds )  + 1;
					end
				end

				if missed
					sample_res.num_missed = sample_res.num_missed + 1;
				end

				if display_misses & missed
					display_situation(timestamp, orientation, saccades_for_sample, annotations_for_sample, middle_time, delta)
				end
			end
		end % count the number of saccades we missed
		
		% count the number of extra saccades
		% For each detected saccade, we look at what the user marked in the 
		% interval of the detected saccade. 
		% This is an extra saccade if:
		%  1) it is not all 0, meaning the user looked at this interval
		%  2) and there is not anything more than 0, meaning the user did not
		%     mark anything
		
		sample_res.num_extra = 0;
		sample_res.num_detected_where_annotated = 0;
		for a=1:numel(saccades_for_sample)
			s = saccades_for_sample(a);
			start_index = timestamp2index(timestamp,s.time_start);
			stop_index  = timestamp2index(timestamp,s.time_stop);
			
			user_looked_here = any(not(marked_saccade(start_index:stop_index)==0));
			user_marked_something = any(marked_saccade(start_index:stop_index)> 0);
			if user_looked_here & not(user_marked_something)
				sample_res.num_extra = sample_res.num_extra + 1;
				
				if display_extra
					fprintf('\tExtra saccade #%d detected.\n', a)
					middle_time = mean([s.time_start s.time_stop]);
					display_situation(timestamp, orientation, saccades_for_sample,   annotations_for_sample, middle_time, delta)
				end
			end
			
			if user_looked_here
				sample_res.num_detected_where_annotated = ...
					sample_res.num_detected_where_annotated + 1;
			end
		end
		
%		fprintf('Sample %s:  num_missed = %d / %d \n', sample, sample_res.num_missed, sample_res.num_annotated )
		
		species_res.num_missed = species_res.num_missed + sample_res.num_missed;
		species_res.num_annotated = species_res.num_annotated + sample_res.num_annotated;
		species_res.num_detected_where_annotated = species_res.num_detected_where_annotated + sample_res.num_detected_where_annotated;
		species_res.num_extra = species_res.num_extra + sample_res.num_extra;
	end
	
	species_res.false_negative = species_res.num_missed / species_res.num_annotated;
	% note that we divide by num_annotated
	species_res.false_positive = species_res.num_extra / species_res.num_detected_where_annotated; 
	species_res.true_positive = (species_res.num_detected_where_annotated - species_res.num_extra) / species_res.num_annotated; 

%	fprintf('\n\tTotal:  num_missed = %d / %d  \n', species_res.num_missed, species_res.num_annotated )
%	fprintf('\n\tTotal:  num_extra = %d / %d  \n', species_res.num_extra, species_res.num_annotated )
	

function index = timestamp2index(timestamps, time)
	% given array timestamps, find the index corresponding to time
	K = numel(timestamps);
	
	index = round( 1 + (time-timestamps(1))*(K-1)/(timestamps(end)-timestamps(1))   ); 
	index = max(1, min(K, index ));
	
function marked = mark_saccades(saccades, timestamp, marked)
	% marks the saccades in the array marked
	for i=1:numel(saccades)
	    time_start = saccades(i).time_start;
	    time_stop = saccades(i).time_stop;
	    if (time_start < timestamp(1)) | (time_start > timestamp(end))
	       msg = sprintf('Error in timestamp data: [%f %f] saccade: [%f %f].\n',...
	        timestamp(1),timestamp(end),time_start,time_stop);
	        error(msg)
        end
		from = timestamp2index(timestamp, time_start);
		to = timestamp2index(timestamp, time_stop);
        % fprintf('Marking %d %f %f [%d, %d] / %d\n', ...
        %     i, saccades(i).time_start, saccades(i).time_stop,...
        %     from, to, numel(timestamp));
		marked(from:to) = i;
	end
	

function selection = select_specific_sample(list, sample)
	ns = 1;
	for i=1:numel(list)
		if list(i).sample == sample
			selection(ns) = list(i);
			ns = ns + 1;
		end
	end
	
	
function annotations = load_all_qa_data(directory)
% loads all data in a directory (files qa_* in directory )
	na = 1;
	d = dir(sprintf('%s/qa_*.mat',directory));
	for i=1:numel(d)
		filename = sprintf('%s/%s', directory, d(i).name);
		% fprintf('Reading %s...\n' , filename);
		r = load(filename);
		for a=1:numel(r.annotations)
			annotations(na) = r.annotations(a);
			na = na + 1;
		end
	end

	if na == 1
		annotations = [];
	end 

function display_situation(timestamp, orientation, saccades, annotations, time, delta)
	f = figure(45);
	subplot(2,1,1); hold off
	time_from = time-delta;
	time_to = time+delta;
	from = timestamp2index(timestamp, time_from);
	to = timestamp2index(timestamp, time_to);
	
	plot( timestamp(from:to), orientation(from:to), 'r.');
	hold on
	
	plot_90deg_lines();

	for i=1:numel(saccades)
		if abs(saccades(i).time_start - time) < delta + 2
			plot_saccade_delimiters(saccades(i), 50)
		end
	end
	title('Detected saccades')
	a = axis;
	plot([ time time], [a(3) a(4)], 'k--')
		
	a(1) = time_from;
	a(2) = time_to;
	a(3) = a(3) - 20;

	axis(a);
	
	a = axis;

	subplot(2,1,2); hold off
	plot( timestamp(from:to), orientation(from:to), 'r.');
	hold on
	
	plot_90deg_lines();

	plot([ time time], [a(3) a(4)], 'k--')
	
	min_orientation = min(orientation(from:to));
	
	for an=1:numel(annotations)
		for i=1:numel(annotations(an).saccades)
			% added jul2010
%			if annotations(an).saccades(i).ignore
%				continue
%			end
			
			plot([ annotations(an).from_ts annotations(an).to_ts], [min_orientation, min_orientation]-10, 'b--')
			if abs(annotations(an).saccades(i).time_start - time) < delta + 1
				plot_saccade_delimiters(annotations(an).saccades(i), 50)
			end
		end
	end
	axis(a);
	
	title('Annotated saccades')
	drawnow
	pause
	
function plot_saccade_delimiters(saccade, ybarsize)
	% expects saccades.time_start, saccades.time_stop, orientation_start, orientation_stop
		x1 = saccade.time_start;
		y1 = saccade.orientation_start;
		x2 = saccade.time_stop;
		y2 = saccade.orientation_stop;

		plot( [x1 x1], [y1-ybarsize y1+ybarsize] , 'g-')
		plot( [x2 x2], [y2-ybarsize y2+ybarsize] , 'b-')
		plot( [x1 x2], [y1-ybarsize y2-ybarsize] , 'r-')


function saccades = fix_saccades_timestamp(timestamp, saccades)
    warned = false;
    for i=1:numel(saccades)
        if saccades(i).time_start < 100000
            saccades(i).time_start = saccades(i).time_start + timestamp(1);
            saccades(i).time_stop = saccades(i).time_stop + timestamp(1);
            if not(warned)
              %  fprintf('Fixing saccade timestamp, now %f.\n', saccades(i).time_start);
%                warned = true;
            end
        end
    end