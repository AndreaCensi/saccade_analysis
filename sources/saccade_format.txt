
.. _saccade_format:


Saccade format description
--------------------------

Note: all angle-related quantities are in **degrees**, not radians.

The format is compatible with the one used by the `Geometric Saccade Detector`_, albeit some fields are specific to only one of the packages.
 

The following are the most important fields: 

``time_start``
  Timestamp at which the saccade started (seconds)  

``orientation_start``, ``orientation_stop``
  Initial and final orientation (degrees)  

``time_passed``
  Time since last saccade (seconds).

``amplitude``
  Saccade amplitude (degrees). This is always positive.

``sign``
  Saccade direction (+1: left, -1: right)

``top_velocity``
  Top  angular velocity estimated during saccade (degrees/second). 

``duration``
  Saccade duration (computed as amplitude/top_velocity).


There are other fields used for DB purposes:

``sample``
  The timestamp describing the sample. Format: ``YYYYMMDD_HHmmSS``.

``sample_num``
  Index associated to a sample. 
 

Some other fields used during the computation: 

``letter``
  Either 'L' (left) or 'R' (right). This is the same info as the
  ``sign`` field.




