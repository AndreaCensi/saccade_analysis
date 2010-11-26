function [theta, choice] = line_filter(timestamp, x,y, sigma, interval)
	
	% filter?
	xf = x;
	yf = y;
	
	% find velocity
	vx = numerical_derivative2(1,xf);
	vy = numerical_derivative2(1,yf);
	
	% guess theta using velocity
	f_smooth = fspecial('gaussian', [1 ceil(sigma*6)], sigma);
	f_after = [zeros(1,interval) 0 0 0  ones(1,interval)];
	f_before = [ones(1,interval) 0 0 0  zeros(1,interval)];
	
	theta_smooth = theta_unwrap(atan2(conv_pad(vy, f_smooth), conv_pad(vx, f_smooth)));
	theta_after  = theta_unwrap(atan2(conv_pad(vy, f_after),  conv_pad(vx, f_after)));
	theta_before = theta_unwrap(atan2(conv_pad(vy, f_before), conv_pad(vx, f_before)));

	[theta, choice] = magic_filter(theta_smooth, theta_after, theta_before);
	theta = theta_unwrap(theta);

	if false
	figure; 
	nr=3;nc=2;np=1;
	subplot(nr,nc,np);np=np+1;hold on
	t=timestamp;
	plot(t, rad2deg(same_reference(theta_smooth, theta_smooth)), 'k-')
	plot(t, rad2deg(same_reference(theta_smooth, theta_after)), 'g-')
	plot(t, rad2deg(same_reference(theta_smooth, theta_before)), 'b-')
	plot(t, rad2deg(same_reference(theta_smooth, theta)), 'r-')
	legend('smooth','after','before','result');
	subplot(nr,nc,np);np=np+1;hold on
	plot(t, rad2deg(same_reference(theta_smooth, theta_smooth)), 'k-')
	plot(t, rad2deg(same_reference(theta_smooth, theta)), 'r.')
	legend('smooth','result');
	subplot(nr,nc,np);np=np+1;hold on
	plot(rad2deg(diff(theta)), 'k.')
	subplot(nr,nc,np);np=np+1;hold on
	velocity = sqrt(vx.^2 + vy.^2);
	plot(conv_pad(velocity, f_smooth), 'k-')
	
	subplot(nr,nc,np);np=np+1;hold on
	change = abs([diff(choice) 0]);
	size(change)
	change_avg = conv_pad(change', ones(1,5));
	plot(change, '.');
	plot(change_avg, 'b-')
	ok = change_avg < 2;
	nok  = not(ok);

	subplot(nr,nc,np);np=np+1;hold on
	threshold = deg2rad(20);
	change =  abs([diff(theta) 0]);
	found = change > threshold;
	plot(t,change,'b-')
	plot(t(found),change(found),'r.')

	figure; 
	nr=2;nc=1;np=1;
	
	r = roughness(x,y,1);
	sigma = 4;
	f_smooth = fspecial('gaussian', [1 ceil(sigma*6)], sigma);
	rf = conv_pad(r, f_smooth);
	found = rf > 0.003;

	subplot(nr,nc,np);np=np+1;hold on
	plot_with_arrows(x,y,theta);
	plot(x(found),y(found),'r.')
	axis('equal')

	subplot(nr,nc,np);np=np+1;hold on
	plot(t,100*r)
	plot(t, 100*rf, 'r-')
	ylabel('cm')
	title('roughness')
	
	end
	
function [res, choice] = magic_filter(theta, alt1, alt2)
	% choose between alt1 and alt2 the one closest to theta
	for i=1:numel(theta)
		d1 = theta_dist(alt1(i), theta(i));
		d2 = theta_dist(alt2(i), theta(i));
		if d1 < d2
			res(i) = alt1(i);
			choice(i) = 1;
		else
			res(i) = alt2(i);
			choice(i) = 2;
		end

	end

function theta2r1 = same_reference(theta1, theta2)
	% put theta2 in the same reference as theta1
	theta1n = normalize_pi(theta1);
	theta2n = normalize_pi(theta2);
	theta2r1 = theta2n + (theta1-theta1n);
	theta2r1 = theta2;
	
	
function alpha  = normalize_pi(alpha)
	% normalizes an angle in (-pi,pi)
	alpha = atan2(sin(alpha),cos(alpha));
	
	

function  d = theta_dist(alpha, beta)
	d = 1 - cos(alpha-beta);

