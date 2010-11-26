function res = detect_saccades_mamarama(timestamp, orientation, configuration) 
% 
	% Parameters we look for in configuration, along with 
	% "reasonable" parameters:
	% Before and after it must remain in var for delta seconds
	%  configuration.robust_amplitude_delta  (0.1 seconds)
	%  configuration.robust_amplitude_var  (5 deg)	
	%  configuration.min_significant_amplitude 
	
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
	
%	res.saccades = [];
	ns = 1;
	
	
	% put quantities that are given in seconds in steps
	dt = timestamp(2)-timestamp(1);
	robust_amplitude_delta_steps = ceil(configuration.robust_amplitude_delta / dt);
	fprintf('steps: %d.\n', robust_amplitude_delta_steps);
	
	% not used for detection, only to fill in fields
	velocity = gaussian_smooth(numerical_derivative2(dt,orientation), 3);
	
	
	% don't start/end right at the border
	% pad = 2*robust_amplitude_delta_steps;
	pad = 7*robust_amplitude_delta_steps;
	i = pad;
	while i <  numel(timestamp) - pad
		% consider it a saccade candidate if the difference is larger than
		% the given parameter

		difference = abs(orientation(i)-orientation(i-1));
%		difference = abs(before_ref - after_ref);

		if difference > configuration.min_significant_amplitude
			before = (i-robust_amplitude_delta_steps):i-1;
			after = i+1:(i+robust_amplitude_delta_steps);

			before_ref = mean(orientation(before));
			after_ref = mean(orientation(after));

			% look before and after and see if the variation is within the bounds
%			before_ref = orientation(i-1);
%			after_ref = orientation(i);
			if orientation(i) > orientation(i-1)
				 % crescente
				monotone = max(orientation(before)) < min(orientation(after));
			else
				monotone = min(orientation(before)) > max(orientation(after));
			end

			err = max(max(abs(orientation(before)-before_ref)), ...
			          max(abs(orientation(after)-after_ref)));
			good = true;
			good = (err < 0.33 * difference);
			
			% good = (err < 0.33 * difference) & (err < 7);
			%good = (err < 0.5 * difference) && (err < 40);
			%good = err < configuration.robust_amplitude_var;
			%good = (err < 0.5 * difference);
			
			amplitude = abs(orientation(i)-orientation(i-1));
			robust_amplitude = abs(before_ref - after_ref);

			good2 = (robust_amplitude > 0.5 * amplitude) & (robust_amplitude < 1.5 * amplitude);
			%good2 = (robust_amplitude > 0.5 * amplitude) & (robust_amplitude > 10);
			%good2 = true;			
			%good2 = robust_amplitude > 0.5*configuration.min_significant_amplitude;
			
			period = (i-robust_amplitude_delta_steps*5):(i+robust_amplitude_delta_steps*5);
			
			period_mov = max(orientation(period)) - min(orientation(period));
			good3 = period_mov < 200;
			%good3 = true;


			
			% before_ok = all(abs(orientation(before)-before_ref) < configuration.robust_amplitude_var);
			% after_ok = all(abs(orientation(after)-after_ref) < configuration.robust_amplitude_var);
			% 
			% if before_ok && after_ok
				% if it is, great!
			if good & good2 & good3 & monotone
				% arbitrary choices here
				start = round(i-1-robust_amplitude_delta_steps/2);
				stop  = round(i+robust_amplitude_delta_steps/2);

				start = round(i-1);
				stop  = round(i+1);

				saccade =fill_in_saccade_data(timestamp, orientation, velocity, start, stop, amplitude) ;

				saccade.robust_amplitude = robust_amplitude;
				saccade.variability = err;
				saccade.period_mov = period_mov;
				res.saccades(ns) = saccade;
					
				ns = ns + 1;
				
				% just skip ahead
				%i = i + ceil(2.1*robust_amplitude_delta_steps);

				i = i + ceil(robust_amplitude_delta_steps);
			else
				% if not, just continue
				i = i + ceil(robust_amplitude_delta_steps);
%				i = i + ceil(2.1*robust_amplitude_delta_steps);
			end
		else
			i = i + 1;
		end
	end
	
	if ns == 1
        res.saccades = [];
    else	     
		% compute the interval between saccades
		res.saccades(1).time_passed = nan;
		for k=2:numel(res.saccades)
			res.saccades(k).time_passed = ...
					res.saccades(k).time_start - res.saccades(k-1).time_stop;
		%	res.saccades(k)
			assert( res.saccades(k).time_passed > 0 )
		end
	end
	
		
function saccade = fill_in_saccade_data(timestamp, orientation, velocity, start, stop, amplitude)
	saccade.start = start;
	saccade.stop = stop;
		
	saccade.sign = sign(orientation(stop) - orientation(start));
	if saccade.sign > 0
		saccade.letter = 'L';
	else
		saccade.letter = 'R';
	end
	saccade.time_start  = timestamp(start);
	saccade.time_stop   =  timestamp(stop);
	saccade.duration = 	saccade.time_stop-saccade.time_start;

	% we don't compute duration, but let's give it some jiggle otherwise
 	% stupid matlab gives us correlation = NaN
	saccade.duration = saccade.duration + randn(1) * 0.01;

	saccade.orientation_start = orientation(start);
	saccade.orientation_stop  = orientation(stop);
	saccade.top_velocity = max( abs(velocity(start:stop)) );
	saccade.top_filtered_velocity =	saccade.top_velocity;
	% saccade.amplitude = abs(orientation(stop) - orientation(start));
	saccade.amplitude = amplitude;
	 
