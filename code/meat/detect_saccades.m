function res = detect_saccades(params)
	% This is the "meat" routine to detect saccaderes.
	%
	% The input parameters are as follows:
	%   params.timestamps:  timestamps
	%   params.orientation:  original orientation
	%   params.filtered_orientation:  "flatten out"
	%   params.filtered_velocity:  
	%   params.filtered_acceleration:  
	%
	% Output:
	% 
	%    res  contains all fields of params
	% res.timestamp
	% res.orientation
	% res.sac_detect 
	% res.sac_signs 
	% res.saccades_moments
	% res.saccades_intervals


	res = params;

	filtered_velocity_zero_threshold = 10; % deg / s	
	filtered_velocity_significant_threshold = 15; 
    % minimum this much for data
    threshold_minimum_steps = 7;

	f = fspecial('gaussian',10,2);
	res.robust_velocity =  filter2(f, res.velocity .* res.filtered_velocity);
	
	res.sac_maxima = extrema(res.robust_velocity);
	candidates = abs(res.sac_maxima)>0;
	
	fast_enough = abs(res.filtered_velocity) > filtered_velocity_significant_threshold;
	
	res.sac_detect = candidates & fast_enough;
	res.sac_signs = res.sac_maxima(res.sac_detect);	

%	res.sac_letters( res.sac_signs < 0) = 'R';
%	res.sac_letters( res.sac_signs > 0) = 'L';
	
	res.saccades_moments = find(res.sac_detect);
	
	res.saccades_intervals = res.saccades_moments(2:end) - res.saccades_moments(1:end-1);
	
	% This marks the parts that were already considered as part of a saccades
	% so we avoid overlapping detections
	considered = zeros(size(res.sac_maxima));
	
	ns = 1;
	for m=res.saccades_moments
		% already considered
		if considered(m)
			continue
		end
		start = m-1;
		while start > 1
			if (abs(res.filtered_velocity(start)) <=  filtered_velocity_zero_threshold) || ...
                    (considered(max(1,start-1)) )
				break
			end
			start = start - 1;
		end 
		stop = m+1;
        N = numel(res.orientation);
		while stop < N
			if (abs(res.filtered_velocity(stop)) <=  filtered_velocity_zero_threshold) || ...
                    (considered(min(N,stop+1)) )
				break
			end
			stop = stop + 1;
        end 
        
        if min(abs(m-start), abs(m-stop)) < threshold_minimum_steps
           continue 
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
		res.saccades(ns).amplitude = abs(res.orientation(stop) - res.orientation(start));
		res.saccades(ns).duration  = res.saccades(ns).amplitude/		res.saccades(ns).top_velocity;
		ns = ns + 1;
    end
	
    % no saccades detected
    if ns == 1
        res.saccades = [];
    end
	
	
	