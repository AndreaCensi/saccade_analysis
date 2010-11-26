function import_ros_data()
    % Imports the new data from Ros into the old format

% new data position
directory = 'forAndrea_20101114/data/checkered_100fps/';
species = {'Dananassae','Darizonae','Dhydei','Dmelanogaster','Dmojavensis','Dpseudoobscura'};
% old data position
output_dir = 'saccade_data';

assert(exist(directory, 'dir') ~= 0)
assert(exist(output_dir, 'dir') ~= 0)

for p = 1:numel(species)
    pname = path_join(directory, species{p});
    list = dir(sprintf('%s/processed_*.mat', pname));
    for l=1:numel(list)
        fname = path_join(pname, list(l).name);
        assert(exist(fname, 'file') ~= 0)
        fprintf('Importing species %d/%d (%s), sample %d/%d (file %s)\n', ...
            p, numel(species), species{p}, ...
            l, numel(list), list(l).name);
        
        data = load(fname);
        import_sample(output_dir, species{p}, data.magno);
    end
end


function import_sample(output_dir, species, magno)
    % imports one sample
    sample = magno.sample;
    filters = {'unfiltered', 'filt_butter_default', 'filt_butter_challis'};
    for f=1:numel(filters)
        d = magno.(filters{f});
        if ~isstruct(d); continue; end
%        filter_cutoff_freq = d.filter_cutoff_freq;
        thresholds1 = fieldnames(d);
        for t1=1:numel(thresholds1)
            d1 = d.(thresholds1{t1});
            if ~isstruct(d1); continue; end
            thresholds2 = fieldnames(d1);
            for t2=1:numel(thresholds2)
                d2 = d1.(thresholds2{t2});
                ang_vel_thresh = d2.ang_vel_thresh;
                
                configuration = struct;
                configuration.id = sprintf('ros_%s_%s_%s' , ...
                                    filters{f}, thresholds1{t1}, thresholds2{t2});
                configuration.saccade_detection_method = 'ros';
                configuration.filtering = filters{f};
                configuration.threshold1 = thresholds1{t1};
                configuration.threshold2 = thresholds2{t2};                
                
                configuration_dir = sprintf('%s/%s/processed/%s/', ...
                                 output_dir, species, configuration.id);
                my_mkdir(configuration_dir);
                save(sprintf('%s/configuration.mat', configuration_dir), 'configuration');
                
                res = struct;
                res.configuration = configuration;
                res.sample = sample;
                res.info =  get_configuration_info();
                res.saccades = convert_saccades_from_ros_notation(magno, d2);
                
                output = sprintf('%s/processed_data_%s.mat',...
                                 configuration_dir, sample);
    			save(output,'res');
    			
            end
        end
    end
    
         
function saccades = convert_saccades_from_ros_notation(magno, d)
    % sac_index: [2x107 double]                    % 
    %        sac_amp: [1x107 double] % deg
    %   sac_peak_vel: [1x107 double]
    % sac_peak_index: [1x107 double]
    %        sac_dur: [1x107 double] % ms
    %    int_sac_dur: [1x106 double] (ms) int_sac(i) = 1000 * (ts(starts(i+1)) - ts(stops(i))); % now in ms
    
    timestamps = magno.exp_timestamps; 
    rad2deg = 180/pi;
    orientation = rad2deg*(magno.exp_orientation);
    for i=2:numel(d.sac_amp)
        k = i-1;
        saccades(k).sign = sign(d.sac_amp(i));
        saccades(k).amplitude = abs(d.sac_amp(i));
        
        index_start = d.sac_index(1,i);
        index_stop = d.sac_index(2,i);
        
        saccades(k).time_start = timestamps(index_start);
        saccades(k).time_stop = timestamps(index_stop);
        saccades(k).duration = d.sac_dur(i) / 1000; 
        % notice here the different indices
        saccades(k).time_passed = d.int_sac_dur(i-1) / 1000; 
        saccades(k).orientation_start = orientation(index_start);
        saccades(k).orientation_stop = orientation(index_stop);
        saccades(k).top_velocity = d.sac_peak_vel(i);
        saccades(k).top_filtered_velocity = d.sac_peak_vel(i);
        saccades(k).sample = magno.sample;
    end
    
    if numel(d.sac_amp) <= 1 
        saccades = [];
    end
    