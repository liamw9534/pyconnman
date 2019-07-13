from __future__ import unicode_literals

from .interface import ConnInterface


class ConnService(ConnInterface):
    """
    Wrapper around dbus to encapsulate the net.connman.Service interface
    which notionally is used to manage network services and their
    connections.

    :param str obj_path:
        Object path pertaining to the interface to open
        e.g., '/net/connman/service/ethernet_b827ebaf24d8_cable'

    :Properties:

    * **State(string) [readonly]**:
        The service state information.

        Valid states are "idle", "failure", "association",
        "configuration", "ready", "disconnect" and "online".

        The "ready" state signals a successfully
        connected device. "online" signals that an
        Internet connection is available and has been
        verified.

        See doc/overview-api.txt for more information about
        state transitions.

     * **Error(string) [readonly]**:

        The service error status details.

        When error occur during connection or disconnection
        the detailed information is represented in this
        property to help the user interface to present the
        user with alternate options.

        This property is only valid when the service is in
        the "failure" state. Otherwise it might be empty or
        not present at all.

        Currently defined error code is "dhcp-failed".

    * **Name(string) [readonly]**:

        The service name (for example "Wireless" etc.)

        This name can be used for directly displaying it in
        the application. It has pure informational purpose
        and no attempt should be made to translate it.

       For Ethernet devices and hidden WiFi networks this
       property is not present.

    * **Type(string) [readonly]**:

        The service type (for example "ethernet", "wifi" etc.)

        This information should only be used to determine
        advanced properties or showing the correct icon
        to the user.

        Together with a missing Name property, this can
        be used to identify hidden WiFi networks.

    * **Security(array{string}) [readonly]**:

        If the service type is WiFi, then this property is
        present and contains the list of security methods
        or key management settings.

        Possible values are "none", "wep", "psk", "ieee8021x"
        and also "wps".

        This property might be only present for WiFi
        services.

    * **Strength(uint8) [readonly]**:

        Indicates the signal strength of the service. This
        is a normalized value between 0 and 100.

        This property will not be present for Ethernet
        devices.

    * **Favorite(boolean) [readonly]**:

        Will be true if a cable is plugged in or the user
        selected and successfully connected to this service.

        This value is automatically changed and to revert
        it back to false the Remove() method needs to be
        used.

    * **Immutable(boolean) [readonly]**:

        This value will be set to true if the service is
        configured externally via a configuration file.

        The only valid operation are Connect() and of
        course Disconnect(). The Remove() method will
        result in an error.

    * **AutoConnect(boolean) [readwrite]**:

        If set to true, this service will auto-connect
        when no other connection is available.

        The service won't auto-connect while roaming.

        For favorite services it is possible to change
        this value to prevent or permit automatic
        connection attempts.

    * **Roaming(boolean) [readonly]**:

        This property indicates if this service is roaming.

        In the case of Cellular services this normally
        indicates connections to a foreign provider when
        traveling abroad.

    * **Nameservers(array{string}) [readonly]**:

        The list of currently active nameservers for this
        service. If the server is not in READY or ONLINE
        state than this list will be empty.

        Global nameservers are automatically added to this
        list. The array represents a sorted list of the
        current nameservers. The first one has the highest
        priority and is used by default.

        When using DHCP this array represents the nameservers
        provided by the network. In case of manual settings,
        the ones from Nameservers.Configuration are used.

    * **Nameservers.Configuration(array{string}) [readonly]**:

        The list of manually configured domain name
        servers. Some cellular networks don't provide
        correct name servers and this allows for an
        override.

        This array is sorted by priority and the first
        entry in the list represents the nameserver with
        the highest priority.

        When using manual configuration and no global
        nameservers are configured, then it is useful
        to configure this setting.

        Changes to the domain name servers can be done
        at any time. It will not cause a disconnect of
        the service. However there might be small window
        where name resolution might fail.

    * **Timeservers(array{string}) [readonly]**:

        The list of currently active timeservers for this
        service. If the server is not in READY or ONLINE
        state than this list will be empty.

    * **Timerserves.Configuration(array{string}) [readwrite]**:

        The list of manually configured time servers.

        The first entry in the list represents the
        timeserver with the highest priority.

        When using manual configuration this setting
        is useful to override all the other timeserver
        settings. This is service specific, hence only
        the values for the default service are used.

        Changes to this property will result in restart
        of NTP query.

    * **Domains(array{string}) [readonly]**:

        The list of currently used search domains taken
        from Domains.Configurations if set, otherwise a
        domain name if provided by DHCP or VPNs.

    * **Domains.Configuration(array{string}) [readwrite]**:

        The list of manually configured search domains.

    * **IPv4(dict) [readonly]**:

        * **Method(string) [readonly]**:

            Possible values are "dhcp", "manual"
            and "off".

            The value "fixed" indicates an IP address
            that can not be modified. For example
            cellular networks return fixed information.

        * **Address(string) [readonly]**:

            The current configured IPv4 address.

        * **Netmask(string) [readonly]**:

            The current configured IPv4 netmask.

        * **Gateway(string) [readonly]**:

            The current configured IPv4 gateway.

    * **IPv4.Configuration(dict) [readwrite]**:

        Same values as IPv4 property. The IPv4 represents
        the actual system configuration while this allows
        user configuration.

        Changing these settings will cause a state change
        of the service. The service will become unavailable
        until the new configuration has been successfully
        installed.

    * **IPv6(dict) [readonly]**:

        * **Method(string) [readonly]**:

            Possible values are "auto", "manual", "6to4"
            and "off".

            The value "fixed" indicates an IP address
            that can not be modified. For example
            cellular networks return fixed information.
            The value "6to4" is returned if 6to4 tunnel
            is created by connman. The tunnel can only be
            created if method was set to "auto" by the
            user. User cannot set the method to "6to4".

        * **Address(string) [readonly]**:

            The current configured IPv6 address.

        * **PrefixLength(uint8) [readonly]**:

            The prefix length of the IPv6 address.

        * **Gateway(string) [readonly]**:

            The current configured IPv6 gateway.

        * **Privacy(string) [readonly]**:

            Enable or disable IPv6 privacy extension
            that is described in RFC 4941. The value
            has only meaning if Method is set to "auto".

            Value "disabled" means that privacy extension
            is disabled and normal autoconf addresses are
            used.

            Value "enabled" means that privacy extension is
            enabled and system prefers to use public
            addresses over temporary addresses.

            Value "prefered" means that privacy extension is
            enabled and system prefers temporary addresses
            over public addresses.

            Default value is "disabled".

    * **IPv6.Configuration(dict) [readwrite]**:

        Same values as IPv6 property. The IPv6 represents
        the actual system configuration while this allows
        user configuration.

        Changing these settings will cause a state change
        of the service. The service will become unavailable
        until the new configuration has been successfully
        installed.

    * **Proxy(dict) [readonly]**:

        * **Method(string) [readonly]**:

            Possible values are "direct", "auto" and
            "manual".

            In case of "auto" method, the URL file can be
            provided unless you want to let DHCP/WPAD
            auto-discover to be tried. In such case if DHCP
            and WPAD auto-discover methods fails then
            method will be "direct".

            In case of "direct" no additional information
            are provided. For the "manual" method the
            Servers have to be set, Excludes is optional.

        * **URL(string) [readonly]**:

            Automatic proxy configuration URL. Used by
            "auto" method.

        * **Servers(array{string}) [readonly]**:

            Used when "manual" method is set.

            List of proxy URIs. The URI without a protocol
            will be interpreted as the generic proxy URI.
            All others will target a specific protocol and
            only once.

            Example for generic proxy server entry would
            be like this: "server.example.com:911".

        * **Excludes(array{string}) [readonly]**:

            Used when "manual" method is set.

            List of hosts which can be accessed directly.

    * **Proxy.Configuration(dict) [readwrite]**:

        Same values as Proxy property. The Proxy represents
        the actual system configuration while this allows
        user configuration.

        If "auto" method is set with an empty URL, then
        DHCP/WPAD auto-discover will be tried. Otherwise the
        specified URL will be used.

    * **Provider(dict) [readonly]**:

        * **Host(string) [readonly]**:

            VPN host IP.

        * **Domain(string) [readonly]**:

            VPN Domain.

        * **Name(string) [readonly]**:

            VPN provider Name.

        * **Type(string) [readonly]**:

            VPN provider type.

    * **Ethernet(dict) [readonly]**:

        * **Method(string) [readonly]**:

            Possible values are "auto" and "manual".

        * **Interface(string) [readonly]**:

            Interface name (for example eth0).

        * **Address(string) [readonly]**

            Ethernet device address (MAC address).

        * **MTU(uint16) [readonly]**:

            The Ethernet MTU (default is 1500).

        * **Speed(uint16) [readonly] [deprecated]**:

            Selected speed of the line.

            This information is not available.

        * **Duplex(string) [readonly] [deprecated]**:

            Selected duplex settings of the line.
            Possible values are "half" and "full".

            This information is not available.
    """
    def __init__(self, obj_path):
        ConnInterface.__init__(self, obj_path, 'net.connman.Service')

    def clear_property(self, name):
        """
        Clears the value of the specified property.

        Properties cannot be cleared for hidden WiFi service
        entries or provisioned services.

        :return:
        :raises dbus.Exception: net.connman.Service.Error.InvalidArguments
        :raises dbus.Exception: net.connman.Service.Error.InvalidProperty
        """
        return self._interface.ClearProperty(name)

    def connect(self):
        """
        Connect this service. It will attempt to connect
        WiFi or Bluetooth services.

        For Ethernet devices this method can only be used
        if it has previously been disconnected. Otherwise
        the plugging of a cable will trigger connecting
        automatically. If no cable is plugged in this method
        will fail.

        This method call will only return in case of an
        error or when the service is fully connected. So
        setting a longer D-Bus timeout might be a really
        good idea.

        Calling :meth:`.Connect` on a hidden WiFi service entry will
        query the missing SSID via the Agent API causing a
        WiFi service with the given SSID to be scanned,
        created and connected.

        :return:
        :raises dbus.Exception: net.connman.Service.Error.InvalidArguments
        """
        return self._interface.Connect()

    def disconnect(self):
        """
        Disconnect this service. If the service is not
        connected an error message will be generated.

        On Ethernet devices this will disconnect the IP
        details from the service. It will not magically
        unplug the cable. When no cable is plugged in this
        method will fail.

        This method can also be used to abort a previous
        connection attempt via the Connect method.

        Hidden WiFi service entries cannot be disconnected
        as they always stay in idle state.

        :return:
        :raises dbus.Exception: net.connman.Service.Error.InvalidArguments
        """
        return self._interface.Disconnect()

    def remove(self):
        """
        A successfully connected service with Favorite=true
        can be removed this way. If it is connected, it will
        be automatically disconnected first.

        If the service requires a passphrase it will be
        cleared and forgotten when removing.

        This is similar to setting the Favorite property
        to false, but that is currently not supported.

        In the case a connection attempt failed and the
        service is in the State=failure, this method can
        also be used to reset the service.

        Calling this method on Ethernet devices, hidden WiFi
        services or provisioned services will cause an error
        message. It is not possible to remove these kind of
        services.

        :return:
        :raises dbus.Exception: net.connman.Service.Error.InvalidArguments
        """
        return self._interface.Remove()

    def move_before(self, obj_path):
        """
        If a service has been used before, this allows a
        reorder of the favorite services.

        :param string obj_path:
            Service's object path to move this object before
        :return:
        :raises dbus.Exception: net.connman.Service.Error.InvalidArguments
        """
        return self._interface.MoveBefore(obj_path)

    def move_after(self, obj_path):
        """
        If a service has been used before, this allows a
        reorder of the favorite services.

        :param string obj_path:
            Service's object path to move this object before
        :return:
        :raises dbus.Exception: net.connman.Service.Error.InvalidArguments
        """
        return self._interface.MoveAfter(obj_path)

    def reset_counters(self):
        """
        [experimental] Reset the counter statistics.
        """
        return self._interface.ResetCounters()
