function saccade_analysis

% RWS 11/08/2010 Comprehensive version. Saccade analysis using different
% data filters, angular velocity thresholds & saccadea amplitude
% thresholds.

clear all

directory = 'forAndrea_20101114/data/checkered_100fps/';
species_list = {'Dananassae','Darizonae','Dhydei','Dmelanogaster','Dmojavensis','Dpseudoobscura'};

for p = 1:6

    pname = path_join(directory, species_list{p});

    fprintf('p = %d  %s\n', p, pname);
    assert(exist(pname, 'dir') ~= 0);
    
    
    list = dir(pname);

    for n = 1:length(list)-2
        fname = list(n+2).name;
        
        fprintf('fname %s\n', fname)

        if fname(1:5) == 'magno'
            sample = fname(7:end-4);
            
            mat_pname_fname = path_join(pname, strcat('processed_',sample,'.mat'));
            if exist(mat_pname_fname)
                fprintf('Using cached results for %s\n', mat_pname_fname);
                continue
            else
               fprintf('Processing %s\n', mat_pname_fname) ;
            end

            clear magno
            load(path_join(pname,fname));
            species = magno.species;
            sample = magno.sample;
            ts = magno.exp_timestamps;
            or_raw = magno.exp_orientation;
            
            Fs = round(length(ts)/(ts(end) - ts(1)));
            magno.Fs = Fs;            

            %%%%%%%%%% APPLY FILTER TO DATA %%%%%%%%%%%%
            
            % 1: filt_type = 'unfiltered' -- unfiltered data
            % 2: filt_type = 'filt_butter_default' -- butterworth with fixed cut-off freq
            % 3: filt_type = 'filt_butter_challis' -- butterworth with optimal cut-off freq via Challis method
            % 4: filt_type = 'filt_kalman' -- kalman filter
                        
            % for filt_type = 1:4
            % XXX get kalman_smoother.m
            for filt_type = 1:3
                
                [filter, or, vel] = apply_filters2data(sample, or_raw, ts, filt_type);
                method = filter.method;
                
               %%%%%%%%% FIND SACCADE magno AT DIFFERENT ANGULAR VELOCITY AND SACCADE AMPLITUDE THRESHOLDS %%%%%%%%%
               
                if isempty(or);
                    magno.(genvarname(method)) = [];
                elseif ~isempty(or);
                    for at = [ 0,5,10:10:50 ]; % degrees; minimum saccade amplitude threshold

                        sac_amp_thresh = at;

                        for vt = 2:5; % sigma; std from mean threshold for angular velocity 

                            vel_thresh_sigma = vt;

                            [ang_vel_thresh, sac_index, sac_amp, sac_peak_vel, sac_peak_index,...
                                sac_dur, int_sac_dur] = find_saccades( ts, or, vel, vel_thresh_sigma, sac_amp_thresh );
                           
                            if filt_type == 2 && 3
                                filter_cutoff_freq = filter.filt_rate;
                                magno.(genvarname(method)).filter_cutoff_freq = filter_cutoff_freq;
                            end
                            magno.(genvarname(method)).(genvarname(strcat('amp_th_', num2str(at)))).(genvarname(strcat('th_', num2str(vt)))).ang_vel_thresh = ang_vel_thresh;
                            magno.(genvarname(method)).(genvarname(strcat('amp_th_', num2str(at)))).(genvarname(strcat('th_', num2str(vt)))).sac_index = sac_index;
                            magno.(genvarname(method)).(genvarname(strcat('amp_th_', num2str(at)))).(genvarname(strcat('th_', num2str(vt)))).sac_amp = sac_amp;
                            magno.(genvarname(method)).(genvarname(strcat('amp_th_', num2str(at)))).(genvarname(strcat('th_', num2str(vt)))).sac_peak_vel = sac_peak_vel;
                            magno.(genvarname(method)).(genvarname(strcat('amp_th_', num2str(at)))).(genvarname(strcat('th_', num2str(vt)))).sac_peak_index = sac_peak_index;
                            magno.(genvarname(method)).(genvarname(strcat('amp_th_', num2str(at)))).(genvarname(strcat('th_', num2str(vt)))).sac_dur = sac_dur;
                            magno.(genvarname(method)).(genvarname(strcat('amp_th_', num2str(at)))).(genvarname(strcat('th_', num2str(vt)))).int_sac_dur = int_sac_dur;

                        end
                    end
                end
            end

            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

            magno
            save(mat_pname_fname, 'magno');

            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        end

    end

end