function species_res = verify_precision(directory, saccades)
	annotations = load_all_qa_data(sprintf('%s/qa',directory));
	fprintf('Found %d annotations.\n', numel(annotations))
%	a = load(sprintf('%s/saccades.mat', directory));
%	saccades = a.saccades;

	annotated_samples = unique({annotations.sample});
	
	species_res.num_missed = 0;
	species_res.num_annotated = 0;

	for i=1:numel(annotated_samples)
		sample = annotated_samples{i};
	
		annotations_for_sample = select_specific_sample(annotations, sample);
		saccades_for_sample = select_specific_sample(saccades, sample);
		
		fprintf('Sample %s: %d annotations, %d detected.\n', sample, numel(annotations_for_sample), numel(saccades_for_sample))
		
		% read the processed 
		processed = load(sprintf('%s/processed_data_%s.mat', directory, sample));
		log = processed.res;
		
		K = numel(log.timestamp);
		detected_saccade = zeros(K,1);
		marked_saccade = zeros(K,1);
		
		detected_saccade = mark_saccades(saccades_for_sample, log.timestamp, detected_saccade);
		
		% mark excluded
		for a=1:numel(annotations_for_sample)
			from = timestamp2index(log.timestamp, annotations_for_sample(a).from_ts);
			to = timestamp2index(log.timestamp, annotations_for_sample(a).to_ts);
			marked_saccade(from:to) = -1;
		end
		% mark annotated
		for a=1:numel(annotations_for_sample)
			marked_saccade = mark_saccades(annotations_for_sample(a).saccades, log.timestamp, marked_saccade);
		end

		already_counted = zeros(numel(saccades_for_sample),1);
		
		sample_res.num_missed = 0;
		sample_res.num_annotated = 0;
		
		% mark excluded
		for a=1:numel(annotations_for_sample)
			for s=1:numel(annotations_for_sample(a).saccades)
				ann_saccade = annotations_for_sample(a).saccades(s);
				middle_time = mean([ann_saccade.time_start ann_saccade.time_stop]);
				middle_index = timestamp2index(log.timestamp, middle_time);
				
				sample_res.num_annotated = sample_res.num_annotated + 1;
				 
				
				ds  = detected_saccade(middle_index);
				if ds == 0
					% we missed this
					sample_res.num_missed = sample_res.num_missed + 1;
				else 
					% check we didn't count it
					if already_counted( ds )
						% we missed this
						sample_res.num_missed = sample_res.num_missed + 1;
					else
						already_counted( ds ) = already_counted( ds )  + 1;
					end
					
				end
			end
%			from = timestamp2index(log.timestamp, annotations_for_sample(a).from_ts);
%			to = timestamp2index(log.timestamp, annotations_for_sample(a).to_ts);
%			marked_saccade(from:to) = -1;
		end
		
		fprintf('Sample %s:  num_missed = %d / %d \n', sample, sample_res.num_missed, sample_res.num_annotated )
		
		species_res.num_missed = species_res.num_missed + sample_res.num_missed;
		species_res.num_annotated = species_res.num_annotated + sample_res.num_annotated;
		
		% figure;
		% subplot(2,1,1);
		% plot(detected_saccade)
		% subplot(2,1,2);
		% plot(marked_saccade)
		% drawnow
		% pause
	end
	
	species_res.false_negative = species_res.num_missed / species_res.num_annotated;

	fprintf('\n\tTotal:  num_missed = %d / %d \n', species_res.num_missed, species_res.num_annotated )
	

function index = timestamp2index(timestamps, time)
	% given array timestamps, find the index corresponding to time
	K = numel(timestamps);
	index = max(1, min(K, round( 1 + (time-timestamps(1))*(K-1)/(timestamps(end)-timestamps(1))   ) ));
	
function marked = mark_saccades(saccades, timestamp, marked)
	% marks the saccades in the array marked
	for i=1:numel(saccades)
		from = timestamp2index(timestamp, saccades(i).time_start);
		to = timestamp2index(timestamp, saccades(i).time_stop);
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
		fprintf('Reading %s...\n' , filename);
		r = load(filename);
		for a=1:numel(r.annotations)
			annotations(na) = r.annotations(a);
			na = na + 1;
		end
	end
