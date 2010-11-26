% trying to fit something with fixed lambda

T0  = 20000;
T1 = 30000;
lambda = 1000;


content = load('data/data_Dmelanogaster-20080410-174953');
data = content.data;
species = data.species;
sample = data.sample;
exp_timestamps = data.exp_timestamps;
exp_orientation = data.exp_orientation;

% normalize to 0
exp_timestamps = exp_timestamps - exp_timestamps(1);



interval = T0:T1;

orientation = exp_orientation(interval);
timestamps = exp_timestamps(interval);
filtered_orientation = l1tf(orientation', lambda);

velocity = filter([-1 0 1], 1, orientation);
filtered_velocity = filter([-1 0 1], 1, filtered_orientation);
filtered_velocity(1) = 0;

f=figure(100); 
subplot(1,2,1); hold off
plot(timestamps, orientation)
hold on
h=plot(timestamps, filtered_orientation, 'r-')
set(h,'LineWidth',3)

subplot(1,2,2); hold off
plot(timestamps, velocity)
hold on
plot(timestamps, filtered_velocity, 'r.')

