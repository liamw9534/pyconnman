*************
Configuration
*************

Configuration files
===================

/etc/connman/main.conf
~~~~~~~~~~~~~~~~~~~~~~

``main.conf`` is  a configuration file for ConnMan. The configuration file
is optional but it can be used to set up various aspects  of  ConnMan's
behavior.  The  location  of the file may be changed through use of the
``--config=`` argument to ``connmand``.

.. note:: The settings in ``main.conf`` can not be accessed via dbus.

.. code-block:: python

    [General]
    # Set  input  request  timeout. Default is 120 seconds The request
    # for inputs like passphrase will timeout after certain amount  of
    # time.  Use this setting to increase the value in case of differ‐
    # ent user interface designs.
    InputRequestTimeout=secs

    # Set browser launch timeout. Default is 300 seconds  The  request
    # for launching a browser for portal pages will timeout after cer‐
    # tain amount of time. Use this setting to increase the  value  in
    # case of different user interface designs.
    BrowserLaunchTimeout=secs

    # Enable  background  scanning. Default is true.  Background scan‐
    # ning will start every 5 minutes unless the scan list  is  empty.
    # In that case, a simple backoff mechanism starting from 10s up to
    # 5 minutes will run.
    BackgroundScanning=true|false

    # List of Fallback timeservers  separated  by  ",".   These  time‐
    # servers  are  used for NTP sync when there are no timeserver set
    # by the user or by the service.  These can contain mixed combina‐
    # tion of fully qualified domain names, IPv4 and IPv6 addresses.
    FallbackTimeservers=server1,server2,...

    # List  of  fallback  nameservers separated by "," appended to the
    # list of nameservers given by the service. The nameserver entries
    # must be in numeric format, host names are ignored.
    FallbackNameservers=server1,server2,...

    # List of technologies that are marked autoconnectable by default,
    # separated by commas ",". The default value for this  entry  when
    # empty  is  ethernet,wifi,cellular.   Services that are automati‐
    # cally connected must have been  set  up  and  saved  to  storage
    # beforehand.
    DefaultAutoConnectTechnologies=technology1,technology2,...

    # List  of  preferred  technologies from the most preferred one to
    # the least preferred one separated by commas  ",".   Services  of
    # the listed technology type will be tried one by one in the order
    # given, until one of them gets connected or they are all tried. A
    # service of a preferred technology type in state 'ready' will get
    # the default route when compared to another preferred  type  fur‐
    # ther  down  the  list with state 'ready' or with a non-preferred
    # type; a service of a preferred technology type in state 'online'
    # will  get  the  default route when compared to either a non-pre‐
    # ferred type or a preferred type further down in the list.
    PreferredTechnologies=technology1,technology2,...

    # List of blacklisted network interfaces separated by ",".   Found
    # interfaces  will be compared to the list and will not be handled
    # by connman, if their first characters  match  any  of  the  list
    # entries. Default value is vmnet,vboxnet,virbr,ifb.
    NetworkInterfaceBlacklist=interface1,interface2,...

    # Allow connman to change the system hostname. This can happen for
    # example if we receive DHCP hostname option.   Default  value  is
    # true.
    AllowHostnameUpdates=true|false

    # Keep  only a single connected technology at any time. When a new
    # service is connected by the  user  or  a  better  one  is  found
    # according to PreferredTechnologies, the new service is kept con‐
    # nected and all the other previously connected services are  dis‐
    # connected. With this setting it does not matter whether the pre‐
    # viously connected services are in 'online'  or  'ready'  states,
    # the  newly  connected  service is the only one that will be kept
    # connected. A service connected by the user will  be  used  until
    # going  out of network coverage. With this setting enabled appli‐
    # cations will notice more network  breaks  than  normal.  Default
    # value is false.
    SingleConnectedTechnology=true|false

    # List  of technologies that are allowed to enable tethering sepa‐
    # rated by ",".  The default value is wifi,bluetooth,gadget.  Only
    # those  technologies  listed  here are used for tethering. If one
    # wants to tether ethernet, then add "ethernet" in the list.  NOTE
    # that  if  ethernet  tethering  is enabled, then a DHCP server is
    # started on all ethernet  interfaces.  Tethered  ethernet  should
    # never  be connected to corporate or home network as it will dis‐
    # rupt normal operation of these networks. Due to this ethernet is
    # not  tethered  by  default.  Do  not activate ethernet tethering
    # unless you really know what you are doing.
    TetheringTechnologies=technology1,technology2,...

    # Restore earlier tethering status  when  returning  from  offline
    # mode,  re-enabling a technology, and after restarts and reboots.
    # Default value is false.
    PersistentTetheringMode=true|false


/var/lib/connman/settings
~~~~~~~~~~~~~~~~~~~~~~~~~

The top-level configuration is defined in here.  The
``settings`` file is read by ``connmand`` on start-up.

.. code-block:: python

    [global]
    # OfflineMode is effectively the same as the flight mode
    # on your mobile phone.  It overrides all other settings.
    # It can be set using dbus through the ConnManager
    # class which has the 'OfflineMode' property.
    OfflineMode=false

    # The name of the network and description of the network
    # can be optionally included.
    #Name=
    #Description

    [Wired]
    # Enable/Disable feature for wired networks e.g., ethernet.
    # It can be set using dbus through the ConnTechnology
    # class which has the 'Powered' property.
    Enable=true

    [WiFi]
    # Enable/Disable feature for WiFi networks.
    # It can be set using dbus through the ConnTechnology
    # class which has the 'Powered' property.
    Enable=true

    [Bluetooth]
    # Enable/Disable feature for bluetooth devices's supporting
    # the PAN profile.  Please be warned that this will kill
    # the adapter's RF thus no other bluetooth profiles can
    # be used either by other system services.
    # It can be set using dbus through the ConnTechnology
    # class which has the 'Powered' property.
    Enable=false


.. warning:: If you set the bluetooth technology ``Enable`` to false
	then this will effectively RF-Kill the device.  This will
	cause a failure of any attempts to access other bluetooth
	profiles.  This can be recovered by using the rfkill
	application to 'unblock' the bluetooth RF i.e.,
	``rfkill unblock bluetooth``.


Service settings files
~~~~~~~~~~~~~~~~~~~~~~

Whenever a service is connected for the first-time, it will
have its own configuration area for ensuring the previous
settings are persistent across boots.

As an example, here is a settings file for an wired network
found under ``/var/lib/connman/ethernet_b827ebaf24d8_cable/settings``:

.. code-block:: python

    [ethernet_b827ebaf24d8_cable]
    Name=Wired
    AutoConnect=true
    Modified=2014-06-19T05:52:09.522465Z
    IPv4.method=dhcp
    IPv4.DHCP.LastAddress=192.168.1.79
    IPv6.method=auto
    IPv6.privacy=disabled


Configuring individual services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The files under ``/var/lib/connman/<service>`` should not be edited.
It is however possible to configure an individual service as
part of the ``/var/lib/connman/settings`` file.  Below is an
example of how this might be done for a wired and WiFi network.

.. code-block:: python

    [service_home_ethernet]
    Type = ethernet
    IPv4 = 192.168.1.42/255.255.255.0/192.168.1.1
    IPv6 = 2001:db8::42/64/2001:db8::1
    MAC = 01:02:03:04:05:06
    Nameservers = 10.2.3.4,192.168.1.99
    SearchDomains = my.home,isp.net
    Timeservers = 10.172.2.1,ntp.my.isp.net
    Domain = my.home

    [service_home_wifi]
    Type = wifi
    Name = my_home_wifi
    Passphrase = secret
    IPv4 = 192.168.2.2/255.255.255.0/192.168.2.1
    MAC = 06:05:04:03:02:01
