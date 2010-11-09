function res = detect_saccades_linear(timestamp, orientation, configuration) 
	% Parameters we look for in configuration, along with 
	% "reasonable" parameters:
	%  configuration.robust_amplitude_delta  (0.1 seconds)
	%  configuration.smooth_steps
	%  configuration.filtered_velocity_significant_threshold
	%  configuration.filtered_velocity_zero_threshold
	%  configuration.min_significant_amplitude 
	%  configuration.debug   print figures and pause
	% Returns res.saccades
	% Output:
	% 
	%    res  contains all fields of params
	% res.timestamp
	% res.orientation
	% res.sac_detect 
	% res.sac_signs 
	% res.saccades_moments
	% res.saccades_intervals
	
	assert(numel(orientation) == numel(timestamp)) 
	
	res.orientation = orientation;
	res.timestamp = timestamp;

	% We create a discrete derivative filter
	dt = timestamp(2)-timestamp(1);
	derivative_filter = [-1 0 1] / (2*dt);
	% With that, we estimate velocity from orientation
	res.velocity = conv_pad(res.orientation, derivative_filter);
	% We create a smoothing filter where sigma is given
	% by the input parameter "smooth_steps"
	sigma = configuration.smooth_steps;
	filter_g = fspecial('gaussian', [1 ceil(sigma*6)], sigma);
	
	% With this filter, we smooth the orientation to create
	% "filtered_orientation".
	res.filtered_orientation = conv_pad(orientation, filter_g);
	
	% Then, we compute the corresponding filtered velocity and acceleration
	res.filtered_velocity = conv_pad(res.filtered_orientation, derivative_filter);
	res.filtered_acceleration = conv_pad(res.filtered_velocity,derivative_filter);
	
	% We take the filtered velocity and compute the extrema.
	% These are the local maxima and minima.
	% extrema() returns either [+1,0,-1] (maximum, none, minimum)
	res.sac_maxima = extrema(res.filtered_velocity);
	% The candidates are either maxima or minima.
	candidates = abs(res.sac_maxima)>0;
	% We select the points which have filtered_velocity bigger
	% then a threshold.
	fast_enough = abs(res.filtered_velocity) > configuration.filtered_velocity_significant_threshold;
	% These are the "centers" of the saccades.
	res.sac_detect = candidates & fast_enough;
	res.saccades_moments = find(res.sac_detect);
 

	% At this point, most of the program logic is needed
	% to avoid to detect merged saccades.
	
	% This marks the parts that were already considered as part of a saccades
	% so we avoid overlapping detections
	considered = zeros(size(res.sac_maxima));
	
	% current saccade
	ns = 1;
	% Look at all the candidates
	for m=res.saccades_moments'
		% Skip if the moment is already part of a detected saccade
		if considered(m)
			continue
		end
		% Now let's find the starting moment for the saccade
		% as the first point which either:
		% - the velocity drops below the param filtered_velocity_zero_threshold
		% - it is part of another saccade
		start = m-1;
		while start > 1
			if (abs(res.filtered_velocity(start)) <=  configuration.filtered_velocity_zero_threshold) || ...
                    (considered(max(1,start-1)) )
				break
			end
			start = start - 1;
		end 
		
		% The same thing forward in time to find the saccade end
		stop = m+1;
        N = numel(res.orientation);
		while stop < N
			if (abs(res.filtered_velocity(stop)) <=  configuration.filtered_velocity_zero_threshold) || ...
                    (considered(min(N,stop+1)) )
				break
			end
			stop = stop + 1;
        end 
        duration = timestamp(stop) - timestamp(start);
		if duration > 0.7 % remove ridicously large saccades, here the fly is moving slowly
			continue
		end

		% We compute the orientation using the filtered orientation
		amplitude = abs(res.filtered_orientation(stop) - res.filtered_orientation(start));
		% If this is below a threshold, we ignore it
		if amplitude <  configuration.min_significant_amplitude 
			continue
		end
		
		% Then we make sure this is not only an oscillation.
		% The need for this might not be apparent, but it was
		% inspired by looking at the results on the data.
		% To decide whether this is just an oscillation or 
		% a real saccade, we define a delta of time, and we consider
		% it a real saccade if the fly kept the orientation for the whole
		% delta.

		delta_steps = ceil(configuration.robust_amplitude_delta / (timestamp(2)-timestamp(1)));
		if (start > delta_steps + 1) && (stop < numel(timestamp) - delta_steps - 1)
		if res.filtered_orientation(stop) > res.filtered_orientation(start)
			robust_amplitude =...
			 +min(res.orientation(stop:(stop+delta_steps))) ...
			 -max(res.orientation((start-delta_steps):start));
		else
			robust_amplitude =...
			 -max(res.orientation(stop:(stop+delta_steps))) ...
			 +min(res.orientation((start-delta_steps):start));
		end
    	if robust_amplitude < configuration.min_significant_amplitude 
			continue
		end
		end
    
		% We mark the span of this saccade as "considered"
		considered(start:stop) = 1;
        
        % for mamarama, july 2010
        considered(max(start-3,1):min(numel(considered),stop+3)) = 1;
        		
		% From now on, we just create the saccade structure.
        
		res.saccades(ns).maximum = m;
		res.saccades(ns).start = start;
		res.saccades(ns).stop = stop;
		
		res.saccades(ns).sign = sign(res.orientation(stop) - res.orientation(start));
		if res.saccades(ns).sign > 0
			res.saccades(ns).letter = 'L';
		else
			res.saccades(ns).letter = 'R';
		end
		res.saccades(ns).time_start  = res.timestamp(start);
		res.saccades(ns).time_stop  = res.timestamp(stop);
		if ns > 1
			res.saccades(ns).time_passed = ...
				res.saccades(ns).time_start - res.saccades(ns-1).time_stop;
				
			assert( res.saccades(ns).time_passed > 0 )

            % TODO: add other computation here
		else
			res.saccades(ns).time_passed = nan;
		end
		
		res.saccades(ns).orientation_start  = res.orientation(start);
		res.saccades(ns).orientation_stop  = res.orientation(stop);
		res.saccades(ns).top_velocity = max( abs(res.velocity(start:stop)) );
		res.saccades(ns).top_filtered_velocity = max( abs(res.filtered_velocity(start:stop)) );
		res.saccades(ns).amplitude = amplitude;
%		res.saccades(ns).duration  = res.saccades(ns).amplitude/ res.saccades(ns).top_velocity;
		res.saccades(ns).duration = duration; 
		ns = ns + 1;
    end
	
    % no saccades detected
    if ns == 1
        res.saccades = [];
%    else
        % remove first saccade
        % because we cannot compute the intra-saccade statistics
 %       res.saccades(1) = [];
    end


	% if debug is active plot 
	if configuration.debug
		plot_debug_info(res, configuration);
		pause
	end

function y = conv_pad(x, f)
	% convolves with a filter, preserving distance
	pad = numel(f)*2;
	x1 = [x(1)*ones(pad,1); x;  x(end)*ones(pad,1)];
	y1 = conv(x1, f, 'same');
	y = y1((pad+1):(end-pad));
	assert(numel(x) == numel(y))
	
	
function plot_debug_info(res, configuration)
	figure;
	nr=2;nc=2;np=1;
	subplot(nr,nc,np); np=np+1; hold on
	plot(res.timestamp, res.orientation, 'r.');
	legend('theta')
	
	k = [res.saccades.start];
	plot(res.timestamp(k), res.orientation(k), 'b.');
	
	subplot(nr,nc,3); np=np+1; hold on
	plot(res.timestamp, abs(res.filtered_velocity), '-');
	plot(res.timestamp, ones(size(res.timestamp)) * 	configuration.filtered_velocity_significant_threshold, 'g--')
	plot(res.timestamp, ones(size(res.timestamp)) * 	configuration.filtered_velocity_zero_threshold, 'r--')
	legend('filtered velocity','threshold sign', 'theshold 0')
