

x = randn(10000, 1);
interval = [-3 3];
numbins = 100;


f = figure; hold on
plot(bins, normpdf(bins, 0, 1), 'k--')

[pdf, bins, fraction_excluded] = compute_pdf(x, interval, numbins);
plot(bins, pdf, 'b-')

[pdf, bins, fraction_excluded] = compute_pdf(x, interval, numbins/4);
plot(bins, pdf, 'r-')
