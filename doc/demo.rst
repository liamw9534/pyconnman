****
Demo
****

A demo application is provided under ``demo/demo.py`` with the source code
distribution.  The demo is a simple command-line parser and may be launched by
running:

    ``python demo/demo.py``

The application shows display a command prompt:

.. code-block:: python

  CONN>

At the command-prompt, you can type ``help`` to get a list of commands and their
options.

.. code-block:: python

  CONN> help
  <add commands here>

Each command implements a legitimate use-case of the pyconnman API.  Following are
some example scenarios to get started.


Get a list of technologies
==========================

You can find out which technologies are available on your system
by using the ``list-technologies`` command.

.. code-block:: python

  CONN> list-technologies
  =========================================================
  <add output here>


Scanning WiFi and getting a list of services
============================================

To get a list of services, it's normally firstly a good idea
to scan to ensure any service updates are reflected in the
service list.  This can be done with the ``technology-scan``
command.

.. note:: Only the WiFi technology supports this feature
	despite the fact that the API is common across all
	technology types.


.. code-block:: python

  CONN> technology-scan <technology>
  =========================================================
  <add output here>


The refreshed list of services can be accessed at any time
using the ``list-services`` command.

.. code-block:: python

  CONN> list-services
  =========================================================
  <add output here>


Connecting and disconnecting services
=====================================

Once you have a list of services you may attempt to connect
to one of them using the ``service-connect`` command.

.. note:: If the service requires, for example, WPA authentication
    then you will need to run the WiFi agent first before
    connecting to the service.  See the next section on how to do
    this.


.. code-block:: python

  # The object path will differ on your own system
  CONN> service-connect <name of service>
  =========================================================
  <Add output here>


Setting up an agent to connect to new network services
======================================================

In case that your selected service requires authentication, you
will start a WiFi agent to handle this.  This is done by
running the ``wifi-agent-start`` command.  To stop the agent, you
can use the ``wifi-agent-stop`` command.

.. code-block:: python

  # This registers an agent to handle WiFi service access
  # attempts requiring authentication or additional user
  # information
  CONN> wifi-agent-start /test/wifiagent <params> 

  # Establish the connection now that the agent is running
  CONN> service-connect <service>

  # You can stop the agent now if you wish
  CONN> wifi-agent-stop /test/wifiagent


Switching your WiFi technology on/off
=====================================

.. code-block:: python

  # We just set the 'Powered' attribute to switch off
  # the WiFi technology...
  CONN> technology-set <technology> Powered 0

  # ...and turn it back on again
  CONN> technology-set <technology> Powered 1
