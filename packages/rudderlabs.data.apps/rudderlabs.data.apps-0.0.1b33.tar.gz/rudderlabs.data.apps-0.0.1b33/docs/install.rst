.. vim: set fileencoding=utf-8 :

==============
 Installation
==============

From PyPI:
-----------

Can be installed with pip, first activate the virtual environment in which you want to use it or do the system wide install.

.. code-block:: bash

   #Installing latest version
   $ pip install rudderlabs.data.apps

   #Installing a specific version
   $ pip install rudderlabs.data.apps==0.0.1b3

From Source:
------------

For the source code, you can clone the repository and then install the package with pip.

.. code-block:: bash

   #Installing latest version
   $ git clone git@github.com:rudderlabs/rudderlabs.data.apps.git

   $ cd rudderlabs.data.apps

   #Virtual environment setup
   $ conda env create -f conda/environment.yaml
   $ conda activate rudderlabs

   #Install in edit mode
   $ pip install -e .

For any specific version, checkout the tag and then install the package with pip.
