General usage notes
===================

* Make sure you have all the directories in the path.::
	
  >> addpath(genpath(pwd)) 


How to annotate the data
========================

1. Download the data. Due to the size, it is not committed to the repository.::
   
	$ cd data/
	$ ./download_datafiles.sh

2. Fire up Matlab. Add all the directories to the path.::
    
    >> addpath(genpath(pwd)) 

3. Start the annotation tool. The main function is ``annotate_logs``
   Give it as the only argument the species directory. ::

    >> annotate_species('data/Dmelanogaster')

You are now inside the tool. 

You are presented with a random slice of data.
Click twice to mark a saccade: at the beginning and the end.
When you have marked all saccades in the current screen, press enter to go to the next screen.

* When you want to exit, press "x"+enter without clicking any point.
* If you want to undo the previous selection, press "u" + enter.  


How to run detection and verify the results
===========================================


How to create the report
========================

	>> create_report('data', 'use_for_report')
	$ python code/report/report_generation_utils/create_report_data.py data
	$ make -C data/report all.pdf


How to recreate some pictures 
=============================

	$ rm data/D*/report/*hist_log*
	>> create_report('data', 'use_for_report')
	$ make -C data/report all.pdf
	
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

Configuration record
---------------------


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
	data/<species>/comments/<picture_id>.yaml 
	data/<species>/comments/layout.yaml 
	
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