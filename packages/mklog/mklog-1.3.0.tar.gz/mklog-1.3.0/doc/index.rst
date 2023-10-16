Welcome to `mklog`'s documentation!
===================================

`mklog` is a python program that converts standard input, content of files, or
output of a command in a log-like format, i.e. current date and time is
prepended to each line.

Download and install
--------------------

See the `main project page <http://git.framasoft.org/spalax/mklog>`_ for
instructions, and `changelog
<https://git.framasoft.org/spalax/mklog/blob/main/CHANGELOG.md>`_.

Usage
-----

Here are the command line options for `mklog`.

.. argparse::
    :module: mklog.__main__
    :func: commandline_parser
    :prog: mklog

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
