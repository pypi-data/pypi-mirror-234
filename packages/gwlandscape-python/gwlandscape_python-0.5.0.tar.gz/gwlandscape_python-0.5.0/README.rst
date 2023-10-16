GWLandscape Python API
======================

`GWLandscape <https://gwlandscape.org.au/>`_ is a service used to handle both the creation of publication datasets and the submission of COMPAS jobs (todo).

Check out the `documentation <https://gwlandscape-python.readthedocs.io/en/latest/>`_ for more information.

Installation
------------

The gwlandscape-python package can be installed with

::

    pip install gwlandscape-python


Example
-------

::

    >>> from gwlandscape_python import GWLandscape
    >>> gwl = GWLandscape(token='<user_api_token_here>')

