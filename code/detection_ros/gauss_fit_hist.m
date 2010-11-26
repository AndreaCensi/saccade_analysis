function [mn, covr, data] = gauss_fit_hist( data, nsigma, niter )
% [mean, covariance, data] = gauss_fit_hist( data, nsigma )
%
% iterates to remove all outliers outside NSIGMA deviations [default 4]
% returns the mean and covariance of the remaining data
%
% JAB 9/15/03

if nargin < 2, 
	nsigma = 4;
end
if nargin < 3,
	niter = 1000;
end

% remove outliers
l = 1; % number of points removed
i = 1; % iteration number
while l >= 1 & i < niter,
	l = length( data );
	mn = mean( data );
	st = std( data );
	data = data(find( data < mn + nsigma*st & data > mn - nsigma*st ));
	l = l - length( data );
	i = i + 1;
end

if i == niter, warning( 'maximum iterations reached -- outliers remain\n' ); end

mn = mean( data );
covr = cov( data );

%fprintf( 1, 'n=%d, m = %.1f, s=%.1f\n', length( data ), mn, sqrt( covr ) );
