function info = get_configuration_info()    
    % Gets a structure describing the current configuration.
    info.timestamp = now;
    info.os = computer;
    info.matlab_version = version;
	[ret, info.host] = system('hostname');
	if ~ret; info.host = 'unknown'; end
	[ret, info.user] = system('whoami');
	if ~ret; info.user = 'unknown'; end
