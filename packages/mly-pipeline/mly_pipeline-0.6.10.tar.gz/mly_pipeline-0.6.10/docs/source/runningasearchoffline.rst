.. _Offline_search_timeline:

Offline search timeline
#######################

For the offline search the timeline is more linear. Remember that you have to specify the **segments** entry in the config file ([start , stop] or path to segments file), for this search to run.


Data Processing
===============

The first step is to get coinsident available segments of the detectors specified. The available segments are processed second by second and saved in hourly groups in dataset objects inside masterdirector/<detector> directories.

Background estimation
=====================

Before we do the search we first create a background estimation using the segments that are downloaded. 
The process of doing that is the same with the online search with the only difference that the time-lagged files generated are finite.
Both continues_FAR -generation and continuous_FAR -inference scripts are running in paralell until all timelagged files have been passed through the models 
and have produced the corresponding inference files. 
There is a timer mechanism build in the runall.sh to stop those two scripts in case not all the files were successfully generated (When condor jobs are 0 for 5 minutes). 

Afte the inference files have been generated a manager function is used to create the FAR_file and the interpolations of the background curve function. 
From them we can calculate the FAR for each event and also the score corresponding to the **threshold** parameter used to separate events.

Zero-lag search
===============

This is just running all the processed data segments through the models.
When an instance has bigger FAR that the threshold it is saved inside the trigger_directory with its own event directory.
All the rest of the instances results are saved in pandas dataframes (.pkl) in chunks of 10000 in output_directory.

Efficiency test (not working yet)
=================================
At the same time as the search, efficiency test script is lunched to produce plots of efficiency tests.

The status page
===============

If you are running the search in one of the LIGO clusters you can generate a status page to see the results. To do that activate the mly-base environment and then run the command:

.. code-block:: bash

    conda activate mly-base
    mly-pipeline-statuspage

This will create a soft link of the search directory in the ``~/publick_html`` directory. There you will find a ``status.html`` file and if you click it, you will see the status page of the search. It includes a false alarm rate plot, a series of efficiency tests and a table with the events and all their links.
