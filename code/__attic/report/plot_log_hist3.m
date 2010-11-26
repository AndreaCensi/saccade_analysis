function [N,C] = plot_log_hist3(x,y,x_interval, y_interval, nxbins, nybins)

	xedges = 10.^( linspace( log10(x_interval(1)), log10(x_interval(2)), nxbins) ); 
	yedges = 10.^( linspace( log10(y_interval(1)), log10(y_interval(2)), nybins) ); 

	valid = (x>x_interval(1))&(x<x_interval(2))&...
	        (y>y_interval(1))&(y<y_interval(2));

	x=x(valid);
	y=y(valid);

	[N,C] = hist3([x y], {xedges, yedges} );
	cx=C{1}; cy=C{2};
	
	
	w=max(cx)-min(cx);
	h=max(cy)-min(cy); 
	
	w=0;h=0;
	a=log10([min(cx)  max(cx)  min(cy) max(cy)]);
%	axis(a)
%	h=loglog(a(1),a(3),'.');

%	h=loglog(x,y,'r.','MarkerSize',0.1);

%	set(h,'MarkerSize',0.001);
	hold on;
	imagesc(log10(cx), log10(cy), -N');
	
	% make sure we are doing it right
	% plot(log10(x),log10(y),'r.','MarkerSize',0.5)
	
	yticks = get(gca,'YTick');
	yticklabel = get(gca,'YTickLabel');
	ylabels = {};
	for i=1:numel(yticks)
		ylabels{i} =   10 ^  yticks(i);
	end
	set(gca,'YTick',yticks)
	set(gca,'YTickLabel',ylabels)
	xticks = get(gca,'XTick');
	xticklabel = get(gca,'XTickLabel');
	xlabels = {};
	for i=1:numel(xticks)
		xlabels{i} =   10 ^  xticks(i);
	end
	set(gca,'XTick',xticks)
	set(gca,'XTickLabel',xlabels)
	axis(a)
	
	
%	xlabel(sprintf('%s (%s)', var1.name, var1.unit))
%	ylabel(sprintf('%s (%s)', var2.name, var2.unit))
	colormap('bone')
