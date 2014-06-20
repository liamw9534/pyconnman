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
  technology-info <tech path> : Display information about a network technology
  help [command] : Display a list of commands or get help for a specific command
  service-disconnect <service path> : Disconnect a network device
  agent-stop <agent path> : Stop network service authentication agent
  agent-start <agent path> [param=value] ... : Start network service authentication agent
  service-info <service path> : Display information about a network service
  list-services None : Display a list of available network services
  technology-scan <tech path> : Scan a network technology for services
  technology-set <tech path> <property> <value> : Set network technology property by name, value
  technology-get <tech path> [property] : Get network technology property by name
  service-rm <service path> : Remove network service
  service-set <service path> <property> <value> : Set network service property by name, value
  service-connect <service path> : Connect a network service
  service-get <service path> [property] : Get network service property by name
  list-technologies None : Provide a list of available network technologies


Each command implements a legitimate use-case of the pyconnman API.  Following are
some example scenarios to get started.


Get a list of technologies
==========================

You can find out which technologies are available on your system
by using the ``list-technologies`` command.

.. code-block:: python

  CONN> list-technologies
  =========================================================
  /net/connman/technology/bluetooth [Bluetooth]
  /net/connman/technology/wifi [WiFi]
  /net/connman/technology/ethernet [Wired]


Scanning WiFi and getting a list of services
============================================

To get a list of services, it's normally firstly a good idea
to scan to ensure any service updates are reflected in the
service list.  This can be done with the ``technology-scan``
command.

.. note:: Only the WiFi technology supports this feature
	despite the fact that the API is common across all
	technology types.

.. note:: The 'ServicesChanged' signal is posted whenever
    a technology scan is completed.  This signal conveys
    the new service information.


.. code-block:: python

  CONN> technology-scan /net/connman/technology/wifi
  =========================================================
  >>>>> ServicesChanged <<<<<
  (None, dbus.Array([dbus.Struct((dbus.ObjectPath('/net/connman/service/ethernet_b827ebaf24d8_cable'),
  dbus.Dictionary({}, signature=dbus.Signature('sv'))), signature=None),
  dbus.Struct((dbus.ObjectPath('/net/connman/service/wifi_000f1330203f_4254487562352d4e473657_managed_psk'),
  dbus.Dictionary({}, signature=dbus.Signature('sv'))), signature=None),
  dbus.Struct((dbus.ObjectPath('/net/connman/service/wifi_000f1330203f_4254576946692d776974682d464f4e_managed_none'),
  dbus.Dictionary({}, signature=dbus.Signature('sv'))), signature=None),
  dbus.Struct((dbus.ObjectPath('/net/connman/service/wifi_000f1330203f_544e434150374345434535_managed_psk'),
  dbus.Dictionary({}, signature=dbus.Signature('sv'))), signature=None),
  dbus.Struct((dbus.ObjectPath('/net/connman/service/wifi_000f1330203f_4449524543542d376b5b54565d55453430455337303030_managed_psk'),
  dbus.Dictionary({dbus.String(u'Strength'): dbus.Byte(53, variant_level=1),
  dbus.String(u'Nameservers'): dbus.Array([], signature=dbus.Signature('s'), variant_level=1),
  dbus.String(u'State'): dbus.String(u'idle', variant_level=1),
  dbus.String(u'Provider'): dbus.Dictionary({}, signature=dbus.Signature('sv'), variant_level=1),
  dbus.String(u'Type'): dbus.String(u'wifi', variant_level=1),
  dbus.String(u'Security'): dbus.Array([dbus.String(u'psk'),
  dbus.String(u'wps')], signature=dbus.Signature('s'), variant_level=1),
  dbus.String(u'AutoConnect'): dbus.Boolean(False, variant_level=1),
  dbus.String(u'Immutable'): dbus.Boolean(False, variant_level=1),
  dbus.String(u'Proxy'): dbus.Dictionary({}, signature=dbus.Signature('sv'), variant_level=1),
  dbus.String(u'IPv4.Configuration'): dbus.Dictionary({dbus.String(u'Method'): dbus.String(u'dhcp', variant_level=1)},
  signature=dbus.Signature('sv'), variant_level=1),
  dbus.String(u'IPv6.Configuration'): dbus.Dictionary({dbus.String(u'Method'): dbus.String(u'auto', variant_level=1),
  dbus.String(u'Privacy'): dbus.String(u'disabled', variant_level=1)}, signature=dbus.Signature('sv'), variant_level=1),
  dbus.String(u'Name'): dbus.String(u'DIRECT-7k[TV]UE40ES7000', variant_level=1),
  dbus.String(u'Favorite'): dbus.Boolean(False, variant_level=1),
  dbus.String(u'Timeservers'): dbus.Array([], signature=dbus.Signature('s'), variant_level=1),
  dbus.String(u'Domains'): dbus.Array([], signature=dbus.Signature('s'), variant_level=1),
  dbus.String(u'Ethernet'): dbus.Dictionary({dbus.String(u'Interface'): dbus.String(u'wlan0', variant_level=1),
  dbus.String(u'Method'): dbus.String(u'auto', variant_level=1),
  dbus.String(u'Address'): dbus.String(u'00:0F:13:30:20:3F', variant_level=1)}, signature=dbus.Signature('sv'), variant_level=1),
  dbus.String(u'Nameservers.Configuration'): dbus.Array([], signature=dbus.Signature('s'), variant_level=1),
  dbus.String(u'Proxy.Configuration'): dbus.Dictionary({}, signature=dbus.Signature('sv'), variant_level=1),
  dbus.String(u'Domains.Configuration'): dbus.Array([], signature=dbus.Signature('s'), variant_level=1),
  dbus.String(u'Timeservers.Configuration'): dbus.Array([], signature=dbus.Signature('s'), variant_level=1),
  dbus.String(u'IPv4'): dbus.Dictionary({}, signature=dbus.Signature('sv'), variant_level=1),
  dbus.String(u'IPv6'): dbus.Dictionary({}, signature=dbus.Signature('sv'), variant_level=1)}, signature=dbus.Signature('sv'))), signature=None),
  dbus.Struct((dbus.ObjectPath('/net/connman/service/wifi_000f1330203f_534b593344463746_managed_psk'),
  dbus.Dictionary({}, signature=dbus.Signature('sv'))), signature=None),
  dbus.Struct((dbus.ObjectPath('/net/connman/service/wifi_000f1330203f_45452d427269676874426f782d717862363236_managed_psk'), dbus.Dictionary({}, signature=dbus.Signature('sv'))), signature=None)],
  signature=dbus.Signature('(oa{sv})')), dbus.Array([], signature=dbus.Signature('o')))


The refreshed list of services can be accessed at any time
using the ``list-services`` command.

.. code-block:: python

  CONN> list-services
  =========================================================
  /net/connman/service/ethernet_b827ebaf24d8_cable [Wired]
  /net/connman/service/wifi_000f1330203f_4254487562352d4e473657_managed_psk [BTHub5-NG6W]
  /net/connman/service/wifi_000f1330203f_4254576946692d776974682d464f4e_managed_none [BTWiFi-with-FON]
  /net/connman/service/wifi_000f1330203f_544e434150374345434535_managed_psk [TNCAP7CECE5]
  /net/connman/service/wifi_000f1330203f_4449524543542d376b5b54565d55453430455337303030_managed_psk [DIRECT-7k[TV]UE40ES7000]
  /net/connman/service/wifi_000f1330203f_534b593344463746_managed_psk [SKY3DF7F]
  /net/connman/service/wifi_000f1330203f_45452d427269676874426f782d717862363236_managed_psk [EE-BrightBox-qxb626]

Connecting and disconnecting services
=====================================

Once you have a list of services you may attempt to connect
to one of them using the ``service-connect`` command.

.. note:: If the service requires, for example, WPA authentication
    then you will need to run the WiFi agent first before
    connecting to the service.  See the next section on how to do
    this.

.. code-block:: python

  # The service object path will differ on your own system
  CONN> service-get /net/connman/service/wifi_000f1330203f_4254487562352d4e473657_managed_psk State
  =========================================================
  idle
  CONN> service-connect /net/connman/service/wifi_000f1330203f_4254487562352d4e473657_managed_psk
  ....
  CONN> service-get /net/connman/service/wifi_000f1330203f_4254487562352d4e473657_managed_psk State
  =========================================================
  ready

Setting up an agent to connect to new network services
======================================================

In case that your selected service requires authentication, you
will start a WiFi agent to handle this.  This is done by
running the ``agent-start`` command.  To stop the agent, you
can use the ``agent-stop`` command.

.. code-block:: python

  # This registers an agent to handle WiFi service access
  # attempts requiring authentication or additional user
  # information
  CONN> agent-start /test/agent ssid=BTHub5-NG6W passphrase=secret123

  # Establish the connection now that the agent is running
  CONN> service-connect /net/connman/service/wifi_000f1330203f_4254487562352d4e473657_managed_psk

  # You can stop the agent now if you wish
  CONN> agent-stop /test/agent


Switching your WiFi technology on/off
=====================================

.. code-block:: python

  # We just set the 'Powered' attribute to switch off
  # the WiFi technology...
  CONN> technology-set /net/connman/technology/wifi Powered 0

  # ...and turn it back on again
  CONN> technology-set /net/connman/technology/wifi Powered 1

.. note:: Previously active services must be reconnected by
    the user following a power-cycle of the underlying technology.
