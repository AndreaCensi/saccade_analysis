

x = abs(randn(1000,1));
y = 0.5 * x + randn(1000,1);

figure; hold on
[N,C]=plot_log_hist3(x,y,[0.01 1000],[0.01 1000],100,50);