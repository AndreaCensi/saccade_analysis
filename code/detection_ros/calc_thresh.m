function [vel_th, mean_vel] = calc_thresh( vel, vel_thresh_sigma )
% vel_th = calc_thresh( vel )
% [vel_th, ee, gg, sigma, tau] = calc_thresh( vel )
% JAB 6/29/05
%
% [vel_th, mean_vel] = calc_thresh( vel, vel_thresh_sigma );
% sigma from mean added as input
% mean vel added as output
% RWS 06/03/08


% ### JOHN COMMENTS: set dynamic velocity threshold at 1.5 sigma from mean( vel )? (~220)
% ### JOHN COMMENTS: set such that a similar number of bins get excluded? (~305)
% ### JOHN COMMENTS: set 3.7 sigma from mean( vel_trim )? (~255) [now 4 sigma=275 6/14/05]**** this is set in flyanal_constants

% set constants
vel_minmax = 3500; % RWS changes: 1500 too low
vel_binsize = 5;
nsigma_trim = 4; % when taking mean, first remove outliers this many sigma away

vel_bins = round( -vel_minmax/vel_binsize:vel_minmax/vel_binsize ) .* vel_binsize;

% first pass, fit a Gaussian
f = find( abs( vel ) < vel_minmax );
[mn, cv, bv] = gauss_fit_hist( vel(f), nsigma_trim );
mean_vel = mn;
covar_vel = cv;

% bin velocities
% n = hist( vel(f), vel_bins );
[n, vel_dist] = hist( vel(f), vel_bins );
n(find( ~n )) = 0.5; % no zeros!

use_th = vel_thresh_sigma*sqrt( cv );  % # sigma of standard deviation

% find the exponential component
lowbin = min( find( vel_bins >= use_th ) );
warning off
p = polyfit( vel_bins(lowbin:end), log10( mean( [n(lowbin:end); n(length( n ) - lowbin + 1:-1:1)] ) ), 1 );
warning backtrace
ee = zeros( size( vel_bins ) ); % exponential values
f = find( vel_bins == 0 );
ee(1:f) = (vel_bins(1):vel_binsize:0).*-p(1) + p(2);
ee(f:end) = (0:vel_binsize:vel_bins(end)).*p(1) + p(2);

% refit Gaussian after subtracting the exponential
new_n = n - 10.^ee;
new_hist = zeros( 1, sum( new_n(find( new_n > 0 )) ) );
l = 0;
for i=1:length( new_n )
	if new_n(i) > 0
		new_hist(l+1:l+round( new_n(i) )) = vel_bins(i);
		l = l + round( new_n(i) );
	end
end
[new_mn, new_cv, lastv] = gauss_fit_hist( new_hist, nsigma_trim );
vel_th = vel_thresh_sigma*sqrt( new_cv );  % # sigma of standard deviation


