function [starts, stops] = match_endpoints( tharr, event_dist, e2 )
% [starts, stops] = match_endpoints( thresh_array, event_dist )
%
% THRESH_ARRAY is a 1-D array containing 0s and 1s, such as:
%   [a, b] = match_endpoints( array > threshold );
%
% Function returns the indices of beginning and endpoints of
% transitions from 0 to 1 (where an above-threshold event occurred).
% So starts(i) is the first point above threshold, and stops(i)
% is the first successive point below threshold for that event.
%
% Function attempts to make numel( starts ) == numel( stops )
% merely by checking to see if an event started before starts(1)
% or ended after stops(end).  An error is raised if the number
% of 'starts' cannot be easily equated to the number of 'stops'.
%
% Then it combines events that overlap or neighbor by less than
% EVENT_DIST [default 5].
%
% Explicitly setting EVENT_DIST = [] tells the function that THARR
% is a 2-row vector already containing starting and stopping times,
% and therefore they will only be modified to match and not
% recalculated.  In this case an event distance can be sent as a third
% argument to the function if desired.
%
% JAB 11/13/04

if nargin < 2, event_dist = 5; end

if isempty( event_dist ),
	% starts and stops already sent -- don't recalculate
	starts = tharr(1,:);
	stops = tharr(2,:);
	if nargin < 3, event_dist = 5;
	else event_dist = e2; end
else
	events = diff( tharr );
	starts = find( events > 0 ) + 1; % starting indices
	stops = find( events < 0 ) + 1; % stopping indices
end

if numel( starts ) == 0 | numel( stops ) == 0, return; end
% if numel( starts ) == 0 | numel( stops ) == 0, error( 'threshold not reached' ); end

if length( starts ) ~= length( stops ) | starts(1) > stops(1) | starts(end) > stops(end),
	fix_flag = 0;
	% check to see if it's easily fixable
	if length( stops ) > 1 & stops(1) < starts(1) & stops(2) > starts(1),
		if starts(1) - stops(1) < stops(1) - 1
			% delete first stop if it's close to first start
	  		stops(1) = [];
		else
			% otherwise, add a start at the beginning
			starts = [1 starts];
		end
		fix_flag = 1;
	end
	if length( starts ) > 1 & starts(end) > stops(end) & starts(end-1) < stops(end),
		if starts(end) - stops(end) < length( tharr ) - starts(end)
			% delete last start if it's close to last stop
	 		starts(end) = [];
		else
			% otherwise, add a stop at the end
			stops = [stops length( tharr )];
		end
		fix_flag = 1;
	end
	if length( starts ) ~= length( stops ), fix_flag = 0; end

	if ~fix_flag,
		error( 'unmatched saccade begin/endpoints' );
	end
end

% combine adjoining or overlapping events
i = 2;
while i <= length( starts ),
	while i > 1 & starts(i) <= stops(i-1) + event_dist,
		starts(i) = [];
		stops(i-1) = [];
		i = i - 1;
	end
	i = i + 1;
end
