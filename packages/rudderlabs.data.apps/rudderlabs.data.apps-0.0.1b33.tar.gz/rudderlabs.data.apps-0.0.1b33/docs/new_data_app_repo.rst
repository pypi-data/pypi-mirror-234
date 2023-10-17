.. vim: set fileencoding=utf-8 :

===============================
 New Data Apps Project
===============================

New Project
-----------

New data apps project from template can be created by running the following command

.. code-block:: bash

   #Example 1:
   $ rlabs new -vv data-apps-leadscoring -t "Lead Scoring" -o ~/Projects

   #Example 2:
   $ rlabs new -vv data-apps-attribution --title "User Attribution" --output-dir ~/Projects


.. note::
   Params:
      - ``-t``, ``--title``: Project title. The project title should be a few words only.  It will appear at the description of your project and as the title of your documentation  [default: New project]
      - ``-o``, ``--output-dir``: Output directory where the project will be created. this directory must not exist before creating the project.

.. note::
   All ``rudderlabs.data.apps`` package scripts comes with custom verbose levels.

      - ``-v``, ``--verbose``: Increase the verbosity level from 0 (only error messages) to 1 (warnings), 2 (infomessages), 3 (debug information) by adding the --verbose option as often as desired (e.g. '-vvv' for debug).

Folder Structure
----------------

Intiall project folder structure

.. code-block:: bash

   data-apps-sample
    ├── conda
      └── environment.yml
    ├── config
      └── sample.yaml
    ├── credentials_template.yaml
    ├── data
    ├── data_loader.py
    ├── __init__.py
    ├── notebooks
      └── sample_notebook.ipynb
      └── __init__.py
    ├── pipelines
      └── sample_pipeline.yaml
    ├── README.md
    ├── requirements.txt
    ├── run_notebook_wrapper.py


Pipeline Configuration
----------------------

Data apps project requires multiple of data processing steps to achieve desired output. This can be provided writing pipeline configuration files, where user can specify the pipeline steps and their parameters.

Sample pipeline configuration file

.. code-block:: yaml

  #Pipeline steps to be executed
  pipeline:
    #Name should satisfy ^[a-zA-Z0-9](-*[a-zA-Z0-9]){0,62}
    - name: "sample-step"
      job_suffix: "S"
      #Entry point for the sagemaker job
      code: "run_notebook_wrapper.py"
      #location of input data to be passed for processing it
      #can be relative to repository or absolute path
      input_data: "data/<job_id>"
      #Once the process is done
      #sagemaker output data will gets downloaded here
      output_path: "data"
      #These params will get passed to `code` script as command line arguments
      params:
        --notebook-path: "notebooks/sample_notebook.ipynb"
        --train-id: "1"
  #Folders to exclude while compresing source code for sagemaker job
  exclude_folders:
    - "data"
  #Files to exclude while compressing source code for sagemaker job
  exclude_files:
    - "*.gitignore"

.. note::

   **<job_id>** will get replaced by actual job ID. while running the pipeline step.
