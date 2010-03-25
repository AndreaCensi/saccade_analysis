How to annotate the data
========================

1. Download the data. Due to the size, it is not committed to the repository.
   
	$ cd data/
	$ ./download_datafiles.sh

2. Fire up Matlab. Add all the directories to the path.
    
    >> addpath(genpath(pwd)) 

3. Start the annotation tool. The main function is ``annotate_logs``
   Give it as the only argument the species directory. 

    >> annotate_logs('data/Dmelanogaster')

You are now inside the tool. 

Data description
================

Saccade record
--------------

Saccade record description:

- time_start       time event
- time_stop        time event
- side             L=1 or R=-1
- amplitude        >0
- top_velocity     top velocity measured in the saccade       
- time_passed      time passed since last saccade

Directory layout
================

Directory Layout, data files:
------------------------------

	data/      Contains the data files, one directory per species.
	data/download_datafiles.sh      Script to download the original data files from website.
	data/<species>/data_*.mat       Data files
	data/<species>/qa/              Contains the saccade annotation files
	data/<species>/processed/       Contains the processed files, one directory
	                                per configuration.
	data/<species>/processed/<conf_id>/processed_*.mat	
	data/<species>/processed/<conf_id>/saccades.mat	
	data/<species>/processed/<conf_id>/configuration.mat	

	data/<species>/report/       Contains all the output pictures (.eps)
	data/<species>/comments/     Contains comments to the figures.
	
Directory Layout, source code
-----------------------------

	code/log_handling     Routines for writing from/to files and running batch jobs
	
		default_configuration()
		
		process_all_data(species_dir, conf)
			Run with one configuration, one species.
			
		run_all_species(data_dir, conf)  
			Run all species with given configuration.
		
	code/log_handling     Routines for writing from/to files and running batch 

Configuration



How to check that saccades are detected correctly

Load processed 