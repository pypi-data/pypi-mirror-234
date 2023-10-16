Install guide
=============

PyPI
----

Kernax can be installed with pip as follows:

.. code::

    pip install kernax


Conda
-----

A conda package will soon be available on the conda-forge channel.


From source
-----------

To install from source, clone this repository, then add the package to your **PYTHONPATH** or simply do

.. code::

    pip install -e .

All the requirements are listed in the file `env.yml`. It can be used to create a conda environement as follows.

.. code::

    cd kernax-main
    conda env create -n kernax -f env.yml

Activate the new environment:

.. code::

    conda activate kernax

And test if it is working properly:

.. code::

    python -c "import kernax; print(dir(kernax))"


Windows support
===============

JAX is now available on Windows, see JAX's official documentation.