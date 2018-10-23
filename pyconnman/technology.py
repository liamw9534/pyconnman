from __future__ import unicode_literals

from .interface import ConnInterface


class ConnTechnology(ConnInterface):
    """
    Wrapper around dbus to encapsulate the net.connman.Technology
    interface which notionally is used to manage network technologies
    e.g., ethernet, wifi, bluetooth.

    :param str obj_path:
        Object path pertaining to the interface to open
        e.g., '/net/connman/technology/wifi'

    :Properties:

    * **Powered(boolean) [readwrite]**:

        Boolean representing the power state of the
        technology. False means that the technology is
        off (and is available RF-Killed) while True means
        that the technology is enabled.

    * **Connected(boolean) [readonly]**:

        Boolean representing if a technology is connected.

        This is just a convience property for allowing the
        UI to easily show if this technology has an active
        connection or not.

        If this property is True it means that at least one
        service of this technology is in ready state.

    * **Name(string) [readonly]**:

        Name of this technology.

    * **Type(string) [readonly]**:

        The technology type (for example "ethernet" etc.)

        This information should only be used to determine
        advanced properties or showing the correct icon
        to the user.

    * **Tethering(boolean) [readwrite]**:

        This option allows to enable or disable the support
        for tethering. When tethering is enabled then the
        default service is bridged to all clients connected
        through the technology.

    * **TetheringIdentifier(string) [readwrite]**:

        The tethering broadcasted identifier.

        This property is only valid for the WiFi technology,
        and is then mapped to the WiFi AP SSID clients will
        have to join in order to gain internet connectivity.

    * **TetheringPassphrase(string) [readwrite]**:

        The tethering connection passphrase.

        This property is only valid for the WiFi technology,
        and is then mapped to the WPA pre-shared key clients
        will have to use in order to establish a connection.
    """

    def __init__(self, obj_path):
        ConnInterface.__init__(self, obj_path, 'net.connman.Technology')

    def scan(self):
        """
        Trigger a scan for this specific technology. The
        method call will return when a scan has been
        finished and results are available. So setting
        a longer D-Bus timeout might be a really good
        idea.

        Results will be signaled via the ServicesChanged
        signal from the manager interface.

        In case of P2P technology, results will be signaled
        via the PeersChanged signal from the manager
        interface.

        :return:
        """
        return self._interface.Scan()
