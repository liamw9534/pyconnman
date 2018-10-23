from __future__ import unicode_literals

from .interface import ConnInterface


class ConnManager(ConnInterface):
    """
    Wrapper around dbus to encapsulate the net.connman.Manager interface
    which notionally is used to manage all network connections.

    :Properties:

    * **State(str) [readonly]**:
        The global connection state of a system.  Possible values
        are "offline", "idle", "ready" and "online".

        If the device is in offline mode, the value "offline"
        indicates this special global state. It can also be
        retrieved via the OfflineMode property, but is kept
        here for consistency and to differentiate from "idle".

        However when OfflineMode property is true, the State
        property can still be "idle", "ready" or "online"
        since it is possible by the end user to re-enable
        individual technologies like WiFi and Bluetooth while
        in offline mode.

        The states "idle", "ready" and "online" match to
        states from the services. If no service is in
        either "ready" or "online" state it will indicate
        the "idle" state.

        If at least one service is in "ready" state and no
        service is in "online" state, then it will indicate
        the "ready" state.

        When at least one service is in "online" state,
        this property will indicate "online" as well.

    * **OfflineMode(boolean) [readwrite]**:
        The offline mode indicates the global setting for
        switching all radios on or off. Changing offline mode
        to true results in powering down all devices. When
        leaving offline mode the individual policy of each
        device decides to switch the radio back on or not.

        During offline mode, it is still possible to switch
        certain technologies manually back on. For example
        the limited usage of WiFi or Bluetooth devices might
        be allowed in some situations.

    See also :py:class:`.ConnService` and
    :py:class:`.ConnTechnology`
    """

    SIGNAL_TECHNOLOGY_ADDED = 'TechnologyAdded'
    """
    :signal TechnologyAdded(signal_name, user_arg, object_path, props):
        Signal that is sent when a new technology is added.

        It contains the object path of the technology and
        also its properties.
    """

    SIGNAL_TECHNOLOGY_REMOVED = 'TechnologyRemoved'
    """
    :signal TechnologyRemoved(signal_name, user_arg, object_path):
        Signal that is sent when a technology has been removed.

        The object path is no longer accessible after this
        signal and only emitted for reference.
    """

    SIGNAL_SERVICES_CHANGED = 'ServicesChanged'
    """
    :signal ServicesChanged(signal_name, user_arg, \
      array{object, dict}, array{object}):
         Signals a list of services that have been changed
         via the first array. And a list of service that
         have been removed via the second array.

         The list of added services is sorted. The dictionary
         with the properties might be empty in case none of
         the properties have changed. Or only contains the
         properties that have changed.

         For newly added services the whole set of properties
         will be present.

         The list of removed services can be empty.

         This signal will only be triggered when the sort
         order of the service list or the number of services
         changes. It will not be emitted if only a property
         of the service object changes. For that it is
         required to watch the :attr:`.SIGNAL_PROPERTY_CHANGED`
         signal of the service object.
    """

    def __init__(self):
        ConnInterface.__init__(self, '/', 'net.connman.Manager')
        self._register_signal_name(ConnManager.SIGNAL_TECHNOLOGY_ADDED)
        self._register_signal_name(ConnManager.SIGNAL_TECHNOLOGY_REMOVED)
        self._register_signal_name(ConnManager.SIGNAL_SERVICES_CHANGED)

    def get_technologies(self):
        """
        Returns a list of tuples with technology object
        path and dictionary of technology properties.

        :return: List of tuples containing object path,dict
        :rtype: array{object,dict}
        :raises dbus.Exception: net.connman.Manager.Error.InvalidArguments
        """
        return self._interface.GetTechnologies()

    def get_services(self):
        """
        Returns a sorted list of tuples with service
        object path and dictionary of service properties.

        This list will not contain sensitive information
        like passphrases etc.

        :return: List of tuples containing object path,dict
        :rtype: array{object,dict}
        :raises dbus.Exception: net.connman.Manager.Error.InvalidArguments
        """
        return self._interface.GetServices()

    def register_agent(self, path):
        """
        Register new agent for handling user requests.

        :return:
        :raises dbus.Exception: net.connman.Manager.Error.InvalidArguments
        """
        return self._interface.RegisterAgent(path)

    def unregister_agent(self, path):
        """
        Unregister an existing agent.

        :return:
        :raises dbus.Exception: net.connman.Manager.Error.InvalidArguments
        """
        return self._interface.UnregisterAgent(path)
