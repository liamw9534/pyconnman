****************************
pyconnman
****************************

.. image:: https://pypip.in/version/pyconnman/badge.png?update
    :target: https://pypi.python.org/pypi/pyconnman/
    :alt: Latest PyPI version

.. image:: https://pypip.in/download/pyconnman/badge.png?update
    :target: https://pypi.python.org/pypi/pyconnman/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/liamw9534/pyconnman.png?branch=master
    :target: https://travis-ci.org/liamw9534/pyconnman
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/liamw9534/pyconnman/badge.png?branch=master
   :target: https://coveralls.io/r/liamw9534/pyconnman?branch=master
   :alt: Test coverage

A library for managing network connectivity using Python, ConnMan and DBus.

Installation
============

Install the python library by running:

    pip install pyconnman


Documentation
=============

Documentation is hosted at https://pythonhosted.org/pyconnman


Project resources
=================

- `Source code <https://github.com/liamw9534/pyconnman>`_
- `Issue tracker <https://github.com/liamw9534/pyconnman/issues>`_
- `Download development snapshot <https://github.com/liamw9534/pyconnman/archive/master.tar.gz#egg=pyconnman-dev>`_


Changelog
=========

v0.2.0
------

Adds Python3 support

v0.1.0
------

Initial release supporting ConnMan v1.24 dbus API with following interfaces:

- ConnManager (net.connman.Manager)
- ConnService (net.connman.Service)
- ConnTechnology (net.connman.Technology)

Services:

- SimpleWifiAgent (net.connman.Agent)
