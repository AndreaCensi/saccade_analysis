function sac_plot_virtual_trajectories(saccades, out_dir)
	basename = 'sac_virtual_traj';
	if report_should_I_skip(out_dir, basename), return, end
	

	[all_samples, saccades] = add_sample_num(saccades);
	num_samples = numel(all_samples);
	
	colors = {'r','g','b','m','k','y'};
	
	f=sac_figure(35);  
	hold on
	for a=1:num_samples
		sample_saccades = saccades([saccades.sample_num] == a);
	
		linear_speed = 0.2;
		[time,x,y,orientation] = simulate_trajectory(sample_saccades, linear_speed);
		color_index = 1 + mod(a-1, numel(colors));
		color = colors{color_index};
		plot(x,y,color);
	end
	axis('equal')
	axis([-5,5,-5,5])
	ftitle='Virtual trajectories';
	sac_print(out_dir,basename, ftitle);
	close(f);

	f=sac_figure(35);  
	hold on
	for a=1:num_samples
		sample_saccades = saccades([saccades.sample_num] == a);
	
		linear_speed = 0.2;
		[time,x,y,orientation] = simulate_trajectory_random(sample_saccades, linear_speed);
		color_index = 1 + mod(a-1, numel(colors));
		color = colors{color_index};
		plot(x,y,color);
	end
	axis('equal')
	axis([-5,5,-5,5])
	ftitle='Virtual random trajectories';
	sac_print(out_dir,'sac_virtual_traj_2', ftitle);
	close(f);
	
	
function [time,x,y,orientation]= simulate_trajectory(saccades, linear_speed)
	time(1)=0;
	x(1)=0;
	y(1)=0;
	orientation(1)=0;
	k=2;
	for i=2:numel(saccades)
		delta = saccades(i).time_passed;
		x(k) = x(k-1) + cos(orientation(k-1)) * linear_speed * delta;
		y(k) = y(k-1) + sin(orientation(k-1)) * linear_speed * delta;
		orientation(k) = saccades(i).orientation_stop;
		k=k+1;
	end
	
	
function [time,x,y,orientation]= simulate_trajectory_random(saccades, linear_speed)
	time(1)=0;
	x(1)=0;
	y(1)=0;
	orientation(1)=0;
	k=2;
	for i=2:numel(saccades)
		delta = saccades(i).time_passed;
		x(k) = x(k-1) + cos(orientation(k-1)) * linear_speed * delta;
		y(k) = y(k-1) + sin(orientation(k-1)) * linear_speed * delta;
		
		amplitude = sign(rand-0.5) * saccades(i).amplitude;
		orientation(k) = orientation(k-1)  + amplitude;
		k=k+1;
	end