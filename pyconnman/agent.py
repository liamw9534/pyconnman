from __future__ import unicode_literals
from .exceptions import ConnCanceledException

import dbus.service


class GenericAgent(dbus.service.Object):
    """
    Generic agent service object class.

    .. note:: GenericAgent can't be directly instantiated.
        It should be sub-classed and provides a template for
        implementing an agent service object.

    :param str obj_path:
        Freely definable object path for the agent service
        e.g., '/agent/netman'.
    """
    def __init__(self, obj_path):
        bus = dbus.SystemBus()
        super(GenericAgent, self).__init__(bus, obj_path)

    """
    This method gets called when the service daemon
    unregisters the agent. An agent can use it to do
    cleanup tasks. There is no need to unregister the
    agent, because when this method gets called it has
    already been unregistered.

    :return:
    """
    @dbus.service.method("net.connman.Agent",
                         in_signature='', out_signature='')
    def Release(self):
        pass

    """
    This method gets called when trying to connect to
    a service and some extra input is required. For
    example a passphrase or the name of a hidden network.

    The return value should be a dictionary where the
    keys are the field names and the values are the
    actual fields. Alternatively an error indicating that
    the request got canceled can be returned.

    Most common return field names are "Name" and of
    course "Passphrase".

    The dictionary arguments contains field names with
    their input parameters.

    In case of WISPr credentials requests and if the user
    prefers to login through the browser by himself, agent
    will have to return a LaunchBrowser error (see below).

    :Examples:

    1. Requesting a passphrase for WPA2 network

        --> RequestInput("/service1",
                { "Passphrase": { "Type": "psk",
                           "Requirement": "mandatory"
                         }
                })
        <-- Returns { "Passphrase" : "secret123" }

    2. Requesting a passphrase after an error on the previous one:

        --> RequestInput("/service1",
                { "Passphrase" : { "Type"        : "psk",
                           "Requirement" : "mandatory"
                         },
                  "PreviousPassphrase" :
                    { "Type"       : "psk",
                      "Requirement : "informational",
                      "Value"      : "secret123"
                    }
                })

    3. Requesting name for hidden network

        --> RequestInput("/service2",
                { "Name" : { "Type"        : "string",
                         "Requirement" : "mandatory",
                         "Alternates"  : [ "SSID" ]
                       },
                  "SSID" : { "Type"        : "ssid",
                         "Requirement" : "alternate"
                       }
                }
        <-- Returns { "Name" : "My hidden network" }

    4. Requesting a passphrase for a WPA2 network with WPS alternative:

        --> RequestInput("/service3",
                { "Passphrase" : { "Type"        : "psk",
                           "Requirement" : "mandatory",
                           "Alternates"  : [ "WPS" ]
                         },
                  "WPS"        : { "Type"        : "wpspin",
                           "Requirement" : "alternate"
                         }
                }

        <-- Returns { "WPS" : "123456" }

    5. Requesting a passphrase for a WPA2 network with WPS alternative
        after an error on the previous one:

        --> RequestInput("/service3",
                { "Passphrase" : { "Type"        : "psk",
                           "Requirement" : "mandatory",
                           "Alternates"  : [ "WPS" ]
                             },
                "WPS"          : { "Type"        : "wpspin",
                           "Requirement" : "alternate"
                         }
                "PreviousPassphrase" :
                        { "Type"       : "wpspin",
                          "Requirement : "informational",
                          "Value"      : "123456"
                        }

    6. Requesting passphrase for a WPA-Enterprise network:

        --> RequestInput("/service4",
                { "Identity"   : { "Type"        : "string",
                           "Requirement" : "mandatory"
                         },
                  "Passphrase" : { "Type"        : "passphrase",
                           "Requirement" : "mandatory"
                         }
                }

        <-- Returns { "Identity" : "alice", "Passphrase": "secret123" }

    7. Requesting challenge response for a WPA-Enterprise network:

        --> RequestInput("/service4",
                { "Identity"   : { "Type"        : "string",
                           "Requirement" : "mandatory"
                         },
                  "Passphrase" : { "Type"        : "response",
                           "Requirement" : "mandatory"
                         }
                }

        <-- Returns { "Identity" : "bob", "Passphrase": "secret123" }

    8. Requesting username and password for a WISPr-enabled hotspot:

            <-- RequestInput("/service5",
                { "Username"   : { "Type"        : "string",
                           "Requirement" : "mandatory"
                         },
                  "Password"   : { "Type"        : "passphrase",
                           "Requirement" : "mandatory"
                         }
                }

            --> { "Username" : "foo", "Password": "secret" }

    :param: string path:
        Object path of service object making the request
    :param: dict fields:
        Allowed field names follow:
        * Type(string):
            Contains the type of a field. For example "psk", "wep"
            "passphrase", "response", "ssid", "wpspin" or plain
            "string".
        * Requirement(string):
            Contains the requirement option. Valid values are
            "mandatory", "optional", "alternate" or
            "informational".

            The "alternate" value specifies that this field can be
            returned as an alternative to another one. An example
            would be the network name or SSID.

            All "mandatory" fields must be returned, while the
            "optional" can be returned if available.

            Nothing needs to be returned for "informational", as it
            is here only to provide an information so a value is
            attached to it.
        * Alternates(array{string}):
            Contains the list of alternate field names this
            field can be represented by.
        * Value(string):
            Contains data as a string, relatively to an
            "informational" argument.

    :return: Allowed field names are:
        * Name(string):
            The name of a network. This field will be requested
            when trying to connect to a hidden network.
        * SSID(array{byte}):
            This field is an alternative to "Name" for WiFi
            networks and can be used to return the exact binary
            representation of a network name.

            Normally returning the "Name" field is the better
            option here.
        * Identity(string):
            Identity (username) for EAP authentication methods.
        * Passphrase(string):
            The passphrase for authentication. For example a WEP
            key, a PSK passphrase or a passphrase for EAP
            authentication methods.
        * PreviousPassphrase(string):
            The previous passphrase successfully saved, i.e.
            which lead to a successfull connection. This field is
            provided as an informational argument when connecting
            with it does not work anymore, for instance when it
            has been changed on the AP. Such argument appears when
            a RequestInput is raised after a retry. In case of WPS
            association through PIN method: when retrying, the
            previous wpspin will be provided.
        * WPS(string):
            This field requests the use of WPS to get associated.
            This is an alternate choice against Passphrase when
            requested service supports WPS. The reply can contain
            either empty pin, if user wants to use push-button
            method, or a pin code if user wants to use the pin
            method.
        * Username(string):
            Username for WISPr authentication. This field will be
            requested when connecting to a WISPr-enabled hotspot.
        * Password(string):
            Password for WISPr authentication. This field will be
            requested when connecting to a WISPr-enabled hotspot.
    :rtype: dict
    :raises dbus.Exception: net.connman.Agent.Error.Canceled
    :raises dbus.Exception: net.connman.Agent.Error.LaunchBrowser
    """
    @dbus.service.method("net.connman.Agent",
                         in_signature='oa{sv}',
                         out_signature='a{sv}')
    def RequestInput(self, path, fields):
        pass

    """
    This method gets called when it is required
    to ask the user to open a website to procceed
    with login handling.

    This can happen if connected to a hotspot portal
    page without WISPr support.

    :return:
    :raises dbus.Exception: net.connman.Agent.Error.Canceled
    """
    @dbus.service.method("net.connman.Agent",
                         in_signature='os',
                         out_signature='')
    def RequestBrowser(self, path, url):
        pass

    """
    This method gets called when an error has to be
    reported to the user.

    A special return value can be used to trigger a
    retry of the failed transaction.

    :return:
    :raises dbus.Exception: net.connman.Agent.Error.Retry
    """
    @dbus.service.method("net.connman.Agent",
                         in_signature='os',
                         out_signature='')
    def ReportError(self, path, error):
        pass

    """
    This method gets called to indicate that the agent
    request failed before a reply was returned.

    :return:
    """
    @dbus.service.method("net.connman.Agent",
                         in_signature='', out_signature='')
    def Cancel(self):
        pass


class SimpleWifiAgent(GenericAgent):
    """
    SimpleWifiAgent is a service agent that allows the user
    to join WiFi networks through a variety of different
    WiFi access security schemes.

    The agent is invoked whenever a 'connect' request
    is made on a service using the 'wifi' technology,
    depending on the security policy in place.

    See :class:`.GenericAgent` which describes in more detail
    the different security schemes supported and use-cases.
    """
    def __init__(self, obj_path):
        super(SimpleWifiAgent, self).__init__(obj_path)
        self.service_params = {'*': {}}

    """
    Set the service parameters to use by the WiFi agent
    on a connection request.

    :param string service:
        Use '*' to apply to all services or specify the
        service name which the settings apply to.
    :param string name:
        Network name to join when trying to connect to a
        hidden network
    :param string ssid:
        Alternative to name for exact binary representation
        of a network name
    :param string username:
        User name (for WISPr-enabled hotspot only)
    :param string password:
        User password (for WISPr-enabled hotspot only)
    :param string identity:
        Identity (username) for EAP authentication methods.
    :param string passphrase:
        WPA/WPA2 authentication passphrase.
    :param string wpspin:
        Where the WPS method is used this may be set to the
        PIN code or to '' if the push button method is used.
    :return:
    """
    def set_service_params(self, service, name=None, ssid=None,
                           identity=None, username=None,
                           password=None, passphrase=None,
                           wpspin=None):
        if (self.service_params.get(service) is None):
            self.service_params[service] = {}
        self.service_params[service]['Name'] = name
        self.service_params[service]['SSID'] = ssid
        self.service_params[service]['Identity'] = identity
        self.service_params[service]['Username'] = username
        self.service_params[service]['Password'] = password
        self.service_params[service]['Passphrase'] = passphrase
        self.service_params[service]['WPS'] = wpspin

    @dbus.service.method("net.connman.Agent",
                         in_signature='oa{sv}',
                         out_signature='a{sv}')
    def RequestInput(self, path, fields):

        response = {}

        services = list(self.service_params.keys())
        if (path in services):
            params = self.service_params[path]
        else:
            params = self.service_params['*']

        if ('Error' in fields):
            raise ConnCanceledException('Canceled')
        if ('Name' in fields):
            if (params.get('SSID')):
                response['SSID'] = params.get('SSID')
            if (params.get('Name')):
                response['Name'] = params.get('Name')
        if ('WPS' in fields):
            if (params.get('WPS')):
                response['WPS'] = params.get('WPS')
        if ('Passphrase' in fields):
            if (params.get('Passphrase')):
                response['Passphrase'] = params.get('Passphrase')
        if ('Identity' in fields):
            if (params.get('Identity')):
                response['Identity'] = params.get('Identity')
            else:
                raise ConnCanceledException('Identity not configured by user')
        if ('Username' in fields):
            if (params.get('Username')):
                response['Username'] = params.get('Username')
            else:
                raise ConnCanceledException('Username not configured by user')
        if ('Password' in fields):
            if (params.get('Password')):
                response['Password'] = params.get('Password')
            else:
                raise ConnCanceledException('Password not configured by user')

        if (not list(response.keys())):
            raise ConnCanceledException('Field(s) not configured by user')

        return response
