function [ang_vel_thresh, sac_index, sac_amp, sac_peak_vel, sac_peak_index,...
    sac_dur, int_sac_dur] = find_sacades( ts, or, vel, vel_thresh_sigma, sac_amp_thresh );


% RWS 11/08/2010 Version.

% Function: Find saccades given the std from mean threshold for angular
% velocity and minimum saccade amplitude threshold.

% INPUTS:
% or: filtered orientation data,
% vel: angular velocity data,
% vel_thresh_sigma: sigma; std from mean threshold for angular velocity
% sac_amp_thresh: degrees; minimum saccade amplitude threshold

%OUTPUTS:
% ang_vel_thresh: calculated angular velocity threshold defining saccade,
% sac_index: saccade start and stop index,
% sac_amp: saccade amplitude,
% sac_peak_vel: saccade peak angular velocity,
% sac_peak_index: saccade peak angular velocity index,
% sac_dur: saccade duration,
% int_sac_dur: inter-saccade duration or interval


% CALCULATE ADAPTIVE VELOCITY THRESHOLD

% Calculate adaptive threshold velocity
[vel_th, mean_vel] = calc_thresh( vel, vel_thresh_sigma );  % # sigma from mean, added vel_thresh_sigma as input

% Calculate saccade refractory period
Fs = round(length(ts)/(ts(end) - ts(1)));
ms = round( 1000 / Fs ); % ms per frame

% frames two saccades must have in between them
sac_refract = 1; % RWS 2009: change to next frame, originally 20·ms window, sac_refract = 20/ms
[starts, stops] = match_endpoints( abs( vel ) > vel_th, sac_refract ); % assumes mean = 0!

if isempty(starts) && isempty (stops)
    
    ang_vel_thresh = [];
    sac_index = [];
    sac_amp = [];
    sac_peak_vel = [];
    sac_peak_index = [];
    sac_dur = [];
    int_sac_dur = [];
    
else
    
    % define minimum saccade amplititude threshold
    min_amp = sac_amp_thresh;
    
    % find times where saccades begin and end, calculate metrics
    
    % set initial values
    peak_vel = zeros( size( starts ) );
    peak_index = zeros( size( starts ) );
    dur = zeros( size( starts ) );
    amp = zeros( size( starts ) );
    ok = zeros( size( starts ) );
    a=0; b=0; c=0; d=0; e=0; f=0; g=0;
    
    
    for i = 1:length( starts ),
        ok(i) = 1;
        
        % Find saccade peak angular velocity
        [peak_vel(i), ind] = max( abs( vel(starts(i):stops(i)) ) );
        
        % RWS 2009: REMOVED MAXIMUM SACCADE PEAK VELOCITY THRESHOLD %%%%%%%
        %         % check peak velocity, probably tracking error if too high
        %         max_vel = 3500;
        %         if peak_vel(i) > max_vel,
        %             ok(i) = 0; a = a + 1;
        %             continue;
        %         end
        
        % Find index of saccade peak angular velocity.
        peak_index(i) = ind + starts(i) - 1;
        
        % RWS 2009: REMOVED REFRACTORY PERIOD BETWEEN SACCADES, setting sac_refract = 1 %%%%%%%
        if i > 1 && starts(i) < stops(i-1) + sac_refract,
            stops(i-1) = stops(i);
            ok(i) = 0; c = c + 1;
            continue
        end
        
        % Find saccade duration as the time interval over which the angular velocity
        % exceeded one-quarter of its maximum value for that event.
        dur(i) = 1000*(ts(stops(i)) - ts(starts(i))); % now in ms
        
        % RWS 2009: REMOVED MINIMUM & MAXIMUM SACCADE DURATION THRESHOLD %%%%%%%
        %         % check for acceptable values of dur
        %         min_dur = 0; max_dur = 250; % ms
        %         if dur(i) < min_dur | dur(i) >= max_dur, ok(i) = 0; f = f + 1;
        %             continue;
        %         end
        
        % Find saccade amplitude using difference of the fly’s median orientations during two 50·ms windows
        % one window before and one after the fly’s angular velocity exceeded one-quarter of its maximum value
        amp_prewnd = 50/ms; % how large window to average orientation when calculating sac amp
        amp_postwnd = 50/ms;
        amp_starts(i) = median( or(max( [starts(i)-amp_prewnd 1] ):starts(i)) );
        amp_stops(i) = median( or(stops(i):min( [stops(i)+amp_postwnd length( or )] )) );
        amp(i) = amp_stops(i) - amp_starts(i);
        
        % RWS 2009: REMOVED MAXIMUM SACCADE AMPLITUDE THRESHOLD
        %         % positive amplitude is clockwise in arena
        %         % check for acceptable values of amp
        %         min_amp = 15; max_amp = 150; % deg
        %         if abs( amp(i) ) < min_amp | abs( amp(i) ) >= max_amp, ok(i) = 0;
        %             g = g + 1;
        %         end
        
        % RWS 2009: USE ONLY MINIMUM SACCADE AMPLITUDE THRESHOLD
        % find saccade exceeding the given minimum saccade amplitude
        if abs( amp(i) ) < min_amp, ok(i) = 0;
            g = g + 1;
        end
        
    end
    
    % for each putative starting time
    ok = find( ok );
    starts = starts(ok);
    stops = stops(ok);
    peak_vel = peak_vel(ok);
    peak_index = peak_index(ok);
    dur = dur(ok);
    amp = amp(ok);
    
    % OUTPUTS
    
    ang_vel_thresh = vel_th;
    sac_index = [starts; stops];
    sac_amp = amp;
    sac_peak_vel = peak_vel;
    sac_peak_index = peak_index;
    sac_dur = dur;
    
    %   Find distribution of intersaccade interval using interval between starts and stops
    dim = size(sac_index);
    if isempty(sac_index)
        int_sac = [];
    elseif dim(2) == 1
        int_sac = [];
    else
        for i = 1:dim(2)-1
            int_sac(i) = 1000 * (ts(starts(i+1)) - ts(stops(i))); % now in ms
        end
    end
    int_sac_dur = int_sac;
    
end

