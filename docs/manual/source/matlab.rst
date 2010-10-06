.. contents:

.. _tethered:

Tethered data analysis
======================

This page explains the conventions used for the tethered saccade data analysis and gives instructions on how to run the annotation and analysis.

The whole process goes like this:

1. Download the data files.

2. In Matlab, create annotations for QA. See section :ref:`create_annotations`.

3. In Matlab, run saccade extraction  (command ``process_data``). See section :ref:`process_data`.

4. In Matlab, create the report figures (command ``create_report``).  See section :ref:`create_report`.

5. Use a python script to create the LaTeX report (command ``create_report``) and compile it.  See section :ref:`python_report`.



.. _create_annotations:

Data annotation
---------------

1. Download the data. Due to the size, it is not committed to the repository.::

	$ cd data/
	$ ./download_datafiles.sh

2. Fire up Matlab. Add all the directories to the path.::

    >> addpath(genpath(pwd)) 

3. Start the annotation tool. The main function is ``annotate_species``
   Give it as the only argument the species directory. ::

    >> annotate_species('data/Dmelanogaster')

You are now inside the tool. 

You are presented with a random slice of data.
Click twice to mark a saccade: at the beginning and the end.
When you have marked all saccades in the current screen, press enter to go to the next screen.

* When you want to exit, press "x"+enter without clicking any point.
* If you want to undo the previous selection, press "u" + enter.  






.. _process_data:

Saccade detection
-----------------

The main method to run the analysis is ::

    process_data('data', conf)

Where ``conf`` is a struct whose fields are described next.
Reference values are also shown.

``conf.id``
  Configuration name. The processed data is created in 
  ``data/<species>/processed/<conf.id>/``

``conf.saccade_detection_method = 'linear'``
  ``linear`` is the only method that works well.

``conf.smooth_steps = 3``
  **to write**

``conf.filtered_velocity_significant_threshold  = 50``
  **to write**

``conf.filtered_velocity_zero_threshold = 15``
  **to write**

``conf.min_significant_amplitude = 5``
  **to write**

``conf.filtered_velocity_significant_threshold = ... ``
  **to write**

This command tries different thresholds. ::

    >> test_different_thresholds

* Create a symbolic link 'use_for_report' for the configuration we are
  going to use in the 





.. _create_report_data:

Create the reort
----------------

Running the analysis: ::

	>> create_report_data('data', 'threshold1')




How to recreate some pictures 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Try this ::

	$ rm data/D*/report/*hist_log*
	>> create_report('data', 'use_for_report')
	$ make -C data/report all.pdf
	

.. _python_report:

Create the PDF report
----------------------------

Run this python script: ::

	$ python code/report/report_generation_utils/create_report_data.py data
	
And then compile the report: ::

	$ make -C data/report all.pdf


 


 