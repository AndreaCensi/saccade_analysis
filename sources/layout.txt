.. _layout:

Directory layout for data and code
==================================



The Matlab code assumes that the files are arranged according to 
a particular layout.

All input and processed data is kept in the ``data/`` subdirectory. ::



    data/                           Contains the data files, one directory per species.
    data/download_datafiles.sh      Script to download the original data files from website.
    data/<species>/data_*.mat       Data files
    data/<species>/qa/              Contains the saccade annotation files
    data/<species>/processed/       Contains the processed files, one directory
                                    per configuration.
    data/<species>/processed/<conf_id>/processed_*.mat  
    data/<species>/processed/<conf_id>/saccades.mat 
    data/<species>/processed/<conf_id>/configuration.mat    

    data/<species>/report/       Contains all the output pictures (.eps)

    data/comments/                  Contains comments to the figures.
    data/comments/<picture_id>.tex 
    data/comments/layout.yaml       Specifies which figures go into the report.

    data/report/                 The big PDF gets created here.



Code organization
------------------

The Matlab code is the ``code/`` directory. Make sure you have all the directories in the path. ::

    >> addpath(genpath(pwd))

Source code layout: ::

    code/log_handling     Routines for writing from/to files and running batch jobs

        default_configuration()

        process_all_data(species_dir, conf)
            Run with one configuration, one species.

        run_all_species(data_dir, conf)  
            Run all species with given configuration.

    code/log_handling     Routines for writing from/to files and running batch 


