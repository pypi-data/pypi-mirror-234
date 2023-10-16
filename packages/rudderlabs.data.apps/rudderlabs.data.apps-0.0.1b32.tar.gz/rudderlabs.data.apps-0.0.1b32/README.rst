.. -*- coding: utf-8 -*-

=======================================
 Rudderlabs Data Apps Utility Functions
=======================================

    This package containes scripts for creating new data apps project and running data apps pipeline using amazon sagemaker instance.


Development
-----------

Conda environment setup
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Create the enviroment
    $ conda env create -f conda/environment.yaml
    # Activate and install this repository in edit mode
    $ conda activate rudderlabs
    $ pip install -e .


Code checks
~~~~~~~~~~~

    All the staged code changes needs to be passed pre-commit checks before committed and pushed to the remote repository

.. code-block:: bash

    #Adding all changes to staging
    $ git add --all

    #Running pre-commmit checks
    $ pre-commit run


Publishing new version
~~~~~~~~~~~~~~~~~~~~~~

    To publish a new version of this package, you need to update the version number in `version.txt` file and run the following command

.. code-block:: bash
    
    # Create a new tag
    $ git tag release/<version> # Ex. release/0.0.1b28

    # Push the tag to remote
    $ git push origin main --tags


Documentation
-------------

    All the documentation written in `ReStructuredText`_ markup language, Follow `Data Apps Utils Documentation`_ for generated html pages.

.. Place your references here:
.. _ReStructuredText: https://docutils.sourceforge.io/rst.html
.. _Sphinx: https://www.sphinx-doc.org/en/master
.. _Data Apps Utils Documentation: https://cnu1439.github.io/data-apps-utils-documentation/index.html
