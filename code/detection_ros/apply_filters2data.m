function [filter, or, vel] = apply_filters2data(sample, or_raw, ts, filt_type)

% RWS 11/08/2010 Version. 

% Function: Calculates angular velocity via central difference method. 
% Applies 1 of 3 filters to data depending on filt_type: 
% butterworth with fixed cut-off freq, 
% butterworth with optimal cut-off freq via Challis method,
% kalman filter.

% INPUTS 
% sample: sample name, 
% ts: data timestamps, 
% or_raw: unfiltered orientation data, 
% filter type: number 1-4 corresponding to defined filter method

% OUTPUTS
% filter: filter method, if applicaple filter cutoff freq,
% or: filtered orientation data,
% vel: angular velocity data,


% unwrap angles using JAB unwrap code
or_unwrap = jb_unwrap( or_raw, pi/4 );     % unwrapping at pi/4 deletes all steps > 45 deg in a single frame... probably OK
or_unwrap = or_unwrap*180/pi;

order = 2;

switch num2str(filt_type)
    
    case '1'
        filter.method = 'unfiltered';
        
        or_unfilt = or_unwrap;
        % central difference method
        vel_unfilt = zeros( size( or_unfilt ) );
        vel_unfilt(2:end-1) = or_unfilt(3:end) - or_unfilt(1:end-2);
        vel_unfilt(2:end-1) = vel_unfilt(2:end-1) ./ (ts(3:end) - ts(1:end-2));
        
        % repeat first and last points to keep size constant
        vel_unfilt(1) = vel_unfilt(2);
        vel_unfilt(end) = vel_unfilt(end-1);
        
        vel = vel_unfilt;
        or = or_unfilt;
        
    case '2'
        filter.method = 'filt_butter_default';
        
        filt_rate = 0.4; %1/5 sampling rate
        % NOTE: for [b,a] = butter(n,Wn), Wn is the normalized cut-off
        % frequency, filt_rate = ((Fs/5)*2*pi)/(pi*Fs);
        filter.filt_rate = filt_rate;
        
        or_unfilt = or_unwrap;
        [b, a] = butter( order, filt_rate );
        or_filt = filtfilt( b, a, or_unfilt );
        % central difference method
        vel_filt = zeros( size( or_filt ) );
        vel_filt(2:end-1) = or_filt(3:end) - or_filt(1:end-2);
        vel_filt(2:end-1) = vel_filt(2:end-1) ./ (ts(3:end) - ts(1:end-2));
        
        % repeat first and last points to keep size constant
        vel_filt(1) = vel_filt(2);
        vel_filt(end) = vel_filt(end-1);
        
        vel = vel_filt;
        or = or_filt; 
        
    case '3'
        filter.method = 'filt_butter_challis';
        
        [filt_rate] = define_challis_filter(sample);
        filter.filt_rate = filt_rate;
               
        if filt_rate ~= 0
            or_unfilt = or_unwrap;
            [b, a] = butter( order, filt_rate );
            or_filt = filtfilt( b, a, or_unfilt );
            % central difference method
            vel_filt = zeros( size( or_filt ) );
            vel_filt(2:end-1) = or_filt(3:end) - or_filt(1:end-2);
            vel_filt(2:end-1) = vel_filt(2:end-1) ./ (ts(3:end) - ts(1:end-2));
            
            % repeat first and last points to keep size constant
            vel_filt(1) = vel_filt(2);
            vel_filt(end) = vel_filt(end-1);
            
            vel = vel_filt;
            or = or_filt;
        else
            vel = [];
            or = [];
        end
                
    case '4'
        filter.method = 'filt_kalman';
        
        or_unfilt = or_raw;  % use raw orientation, wrapped
        
        % define sampling rate
      	Fs = round(length(ts)/(ts(end) - ts(1)));
        dt = 1/Fs;
        
        % kalman filter for or raw data, unwrap & convert to degrees
        
        y = [ cos(or_unfilt); sin(or_unfilt) ];
        A = [ 1 0 dt 0; 0 1 0 dt; 0 0 1 0; 0 0 0 1 ];
        Q = eye(4);
        C = [ 1 0 0 0; 0 1 0 0 ];
        R = eye(2);
        
        initx = [ cos(or_unfilt(1)); sin(or_unfilt(1)); 0; 0 ];
        initP = eye(4);
        
        [xsmooth, Psmooth] = kalman_smoother(y, A, C, Q, R, initx, initP);
        
        or_kalman = atan2(xsmooth(2,:),xsmooth(1,:));
        or_kalman = mod(or_kalman,2*pi);
        
        % unwrap angles using JAB unwrap code
        or_kalman = jb_unwrap( or_kalman, pi/4 );     % unwrapping at pi/4 deletes all steps > 45 deg in a single frame... probably OK
        or_kalman = or_kalman*180/pi;
        
        % calculate vel from kalman or data using central difference method
        vel_kalman = zeros( size( or_kalman ) );
        vel_kalman(2:end-1) = or_kalman(3:end) - or_kalman(1:end-2);
        vel_kalman(2:end-1) = vel_kalman(2:end-1) ./ (ts(3:end) - ts(1:end-2));
        
        % repeat first and last points to keep size constant
        vel_kalman(1) = vel_kalman(2);
        vel_kalman(end) = vel_kalman(end-1);
        
        vel = vel_kalman;
        or = or_kalman;
        
end
