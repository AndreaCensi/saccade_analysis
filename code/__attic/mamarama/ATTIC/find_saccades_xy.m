function res = find_saccades_xy(data)
% data.timestamp
% data.position
% data.debug
% data.decimate 

res = data;

% first, decimate data
	n = numel(data.timestamp);
	selection = 1:data.decimate:n;
	data.position = data.position(selection,:);
	data.timestamp = data.timestamp(selection);

	dt = data.timestamp(2) - data.timestamp(1);
	
% filter and estimate velocity

	x = data.position(:,1);
	y = data.position(:,2);

	sigma = 0.001;
	filter_g = fspecial('gaussian', [1 ceil(sigma*6)], sigma);
	xf = conv_pad(x, filter_g);
	yf = conv_pad(y, filter_g);
	res.vx = numerical_derivative2(dt,xf);
	res.vy = numerical_derivative2(dt,yf);
	
	velocity = sqrt(res.vx.^2 + res.vy.^2);
	fast_enough = velocity > data.min_velocity;

	thetaf = atan2(res.vy,res.vx);
	thetaf2 = theta_unwrap(thetaf);
	
	interval=3;
	sigma=2;
	[theta, choice] = line_filter(data.timestamp, x,y,sigma,interval);
	
	
	figure
%	plot_with_arrows(x,y,thetaf2);
	plot_with_arrows(x,y,theta);
	axis('equal')
	title('orientation')
	
	return
	% n=2; 
	% 
	% filter_g = [ones(1,n) 1 zeros(1,n)];	
	% res.vxf = conv_pad(res.vx, filter_g);
	% res.vyf = conv_pad(res.vy, filter_g);
	% res.theta3 = theta_unwrap(atan2(res.vyf, res.vxf));
	% 
	% filter_g = [zeros(1,n) 1 ones(1,n)];	
	% res.vx4 = conv_pad(res.vx, filter_g);
	% res.vy4 = conv_pad(res.vy, filter_g);
	% res.theta4 = theta_unwrap(atan2(res.vy4, res.vx4));
	% 
	% res.theta5 = magic_filter(thetaf, res.theta4, res.theta3);
	% 
	% % XXX: do with the cos,sin distance?
	% res.ev = abs(res.theta3-res.theta4);


if data.debug
	figure;
	hold on
	plot(velocity);
	a =axis();
	plot(a(1:2), [1 1]*data.min_velocity, 'r--')
	title('linear velocity')

	w = fast_enough;
	nw = not(w);

	figure; 
	nr=3;nc=1;np=1;
	subplot(nr,nc,np);np=np+1;hold on
	t=data.timestamp;
	plot(t(w), rad2deg(thetaf2(w)), 'k-')
	plot(t(nw), rad2deg(thetaf2(nw)), 'r.')
	title('theta')
	subplot(nr,nc,np);np=np+1;hold on
	plot(t(w), rad2deg(res.theta3(w)), 'g-')
	plot(t(w), rad2deg(res.theta4(w)), 'b-')
	plot(t(w), rad2deg(thetaf2(w)), 'r-')
	plot(t(w), rad2deg(res.theta5(w)), 'r-')
	
	%	plot(t(nw), rad2deg(thetaf2(nw)), 'r.')
	title('theta')
	subplot(nr,nc,np);np=np+1;hold on
	plot(t(w), rad2deg(res.ev(w)), 'g-')
	plot(t(nw), rad2deg(res.ev(nw)), 'r.')

	figure;
	hold on
	
	plot(x,y,'b-');
	plot(xf(w),yf(w),'k-');
	plot(x(not(w)),y(not(w)),'r.');
		axis('equal')
	plot(x(1),y(1),'m.','MarkerSize',4)
	legend('original','filtered','not fast enough')
	title('trajectory')
	
	
	figure
%	plot_with_arrows(x,y,thetaf2);
	plot_with_arrows(x,y,res.theta5);
	axis('equal')
	title('orientation')
		% 
		% figure
		% plot(res.vx,res.vy,'k-')
		% axis('equal')
		% 
		% figure; hold on
		% plot(res.vx,res.vy,'k-')
		% plot(res.vxf,res.vyf,'r-')
		% 
		% axis('equal')
	
end

function res = magic_filter(theta, alt1, alt2)
	% choose between alt1 and alt2 the one closest to theta
	for i=1:numel(theta)
		d1 = theta_dist(alt1(i), theta(i));
		d2 = theta_dist(alt2(i), theta(i));
		if d1 < d2
			res(i) = alt1(i);			
		else
			res(i) = alt2(i);
		end
		
	end
	
function  d = theta_dist(alpha, beta)
	d = 1 - cos(alpha-beta);
	
	

