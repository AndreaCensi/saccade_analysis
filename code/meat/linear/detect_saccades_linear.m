function res = detect_saccades_linear(timestamp, orientation, configuration) 
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
	
	%orientation = orientation(100:800);

	sigma = configuration.smooth_steps;
	
	assert(numel(orientation) == numel(timestamp))
	
	res.orientation = orientation;
	res.timestamp = timestamp;
	
	filter_g = fspecial('gaussian', [1 sigma*6], sigma);
	res.filtered_orientation = conv_pad(orientation, filter_g);
	dt = timestamp(2)-timestamp(1);
	derivative_filter = [-1 0 1] / (2*dt);
	res.velocity = conv_pad(res.orientation, derivative_filter);
	res.filtered_velocity = conv_pad(res.filtered_orientation, derivative_filter);
	res.filtered_acceleration = conv_pad(res.filtered_velocity,derivative_filter);
	
	
	res.sac_maxima = extrema(res.filtered_velocity);
	candidates = abs(res.sac_maxima)>0;
	fast_enough = abs(res.filtered_velocity) > configuration.filtered_velocity_significant_threshold;
	res.sac_detect = candidates & fast_enough;
	res.saccades_moments = find(res.sac_detect);

	
	% alternative filter
	
	% This marks the parts that were already considered as part of a saccades
	% so we avoid overlapping detections
	considered = zeros(size(res.sac_maxima));
	
	ns = 1;
	for m=res.saccades_moments'
		% already considered
		if considered(m)
			continue
		end
		start = m-1;
		while start > 1
			if (abs(res.filtered_velocity(start)) <=  configuration.filtered_velocity_zero_threshold) || ...
                    (considered(max(1,start-1)) )
				break
			end
			start = start - 1;
		end 
		stop = m+1;
        N = numel(res.orientation);
		while stop < N
			if (abs(res.filtered_velocity(stop)) <=  configuration.filtered_velocity_zero_threshold) || ...
                    (considered(min(N,stop+1)) )
				break
			end
			stop = stop + 1;
        end 
        
%        if min(abs(m-start), abs(m-stop)) < threshold_minimum_steps
%           continue 
%        end

		amplitude = abs(res.filtered_orientation(stop) - res.filtered_orientation(start));
		if amplitude <  configuration.min_significant_amplitude 
			continue
		end
		
		% make sure this is not only an oscillation
		delta = 0.1;
		delta_steps = ceil(delta / (timestamp(2)-timestamp(1)));
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
    
		considered(start:stop) = 1;
        
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
		else
			res.saccades(ns).time_passed = nan;
		end
		
		res.saccades(ns).orientation_start  = res.orientation(start);
		res.saccades(ns).orientation_stop  = res.orientation(stop);
		res.saccades(ns).top_velocity = max( abs(res.velocity(start:stop)) );
		res.saccades(ns).amplitude = amplitude;
		res.saccades(ns).duration  = res.saccades(ns).amplitude/ res.saccades(ns).top_velocity;
		ns = ns + 1;
    end
	
    % no saccades detected
    if ns == 1
        res.saccades = [];
    end	% 
		% figure; nr=3;nc=1;np=1;
		% subplot(nr,nc,np); np=np+1;
		% hold on
		% plot(res.orientation, 'r.')
		% plot(res.filtered_orientation, 'b-')
		% subplot(nr,nc,np); np=np+1;
		% hold on
		% plot(res.filtered_velocity, 'b-')
		% subplot(nr,nc,np); np=np+1;
		% hold on
		% plot(res.filtered_acceleration, 'b-')
		% title('acceleration')
		% 
	
%	pause
	
function y = conv_pad(x, f)
	pad = numel(f)*2;
	x1 = [x(1)*ones(pad,1); x;  x(end)*ones(pad,1)];
	y1 = conv(x1, f, 'same');
	y = y1((pad+1):(end-pad));
	assert(numel(x) == numel(y))
	
	
	
	