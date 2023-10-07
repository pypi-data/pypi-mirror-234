Installation
############



The search functionality needs a provision of real-time data (data that become available in real time) from a predefined directory. 
This directory needs to be accessible directly from the location where the search scripts will be running. 
Usually the real-time data directory is located in the CIT LIGO cluster and we will use it as the default place to run the search. 
For more information about how to access it see `here <https://computing.docs.ligo.org/guide/computing-centres/ldg/>`_.


Environment and installation of MLy-Pipeline
--------------------------------------------

MLy-Pipeline and MLy need a series of python packages and authentications. It is easy to create an environment that has everything you need to run mly-pipeline. Below we create an environment called `mly-base` for simplicity. You can use any name you want for your environment,

.. code-block:: bash

    conda create -n mly-base python=3.10 pip ; conda activate mly-base ; pip install -r /home/mly/mly-requirements.txt 

This will create and activate a conda environment with all the dependencies needed.

.. note:: From version 0.5 the installation method has changed and now it uses a requiremens file until hermes installation is available through pypi. This restricts the the full running of the search on CIT. If you don't want hermes in your installation you can just use the following: `conda create -n mly-base python=3.10 ; conda activate mly-env ; pip install mly-pipeline`.    

And that's it! You successfully installed MLy-Pipeline and you are ready to run the search. 

Updating MLy-Pipeline
---------------------

If you have already installed the pipeline as described above and you only want to upgrade it to the most recent version run the following commands:

.. code-block:: bash

    conda activate mly-base
    pip install --upgrade mly
    pip install --upgrade mly_pipeline

It is recomended to update mly along with mly_pipeline.
If you want a specific release of the pipeline you type instead:

.. code-block:: bash

    conda activate mly-base
    pip install --upgrade mly
    pip install --upgrade mly_pipeline==<version-number>

Now check :ref:`Setting_up_a_search` to set up your search directory and run the search.
