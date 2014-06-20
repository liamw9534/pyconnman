********
Glossary
********

.. glossary::
	:sorted:

    dbus
		A message bus system providing a simple way for applications
		to talk to one another.  :term:`connmand` provides dbus hooks
		allowing applications to manage network devices and
		connections.

    connmand
		The daemon process that is launched in order to provide all
		the network management services and dbus service API.

    service
		A means of network connectivity through a specific access
		technology.  A given technology may offer multiple services
		e.g., WiFi can often connect to one more more services by
		their SSID.

    technology
		Refers to an underlying access technology such as Wired,
		WiFi and Bluetooth.  Each access technology will typically
		have slightly different configuration attributes and
		security policies.

    agent
		An entity that negotiates network access on behalf of the user
		to a given set of network services by exchanging user
		and/or security information e.g., wireless encryption passphrase.

    SSID
		Service Set Identifier.  A 1 to 32 bytes string that is generally
		human readable and thus often called a network name.  The SSID
		may be hidden on some networks, thus discouraging open access
		usage.
