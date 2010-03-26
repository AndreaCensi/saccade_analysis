function my_mkdir(d)
	if not(exist(d, 'dir'))
		mkdir(d)
	end
