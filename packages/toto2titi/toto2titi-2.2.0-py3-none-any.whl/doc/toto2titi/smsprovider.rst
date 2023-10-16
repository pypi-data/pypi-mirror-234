.. _smsprovider:

Cell phone providers
====================

Here is the list of supported cell phone providers.

Right now, the only supported one is the one I use. `Pull requests <https://framagit.org/spalax/paste2sms/merge_requests>`__ are welcome!

.. toctree::
   :maxdepth: 1
   :glob:

   smsprovider/*

A `sendsms` command line program is also provided by this package,.

.. argparse::
    :module: toto2titi.sendsms.__main__
    :func: commandline_parser
    :prog: sendsms

