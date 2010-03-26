function f = sac_figure(id)
	% function f = sac_figure
	% Creates a figure of the right dimensions to insert into the report
	f=figure;
	fsize = [8 6];
	set(f,'Units','centimeters'); 
	set(f,'Position',[0 0 fsize]); 
	set(f,'PaperUnits','centimeters'); 
	set(f,'PaperPosition',[0 0 fsize]); 
	set(f,'PaperSize', fsize);