from __future__ import unicode_literals

from builtins import object
import dbus


class ConnSignalNameNotRecognisedException(object):
    """
    Exception raised for when a signal name is not recognized.
    Check the originating class for a list of supported signal names
    """
    pass


class ConnCanceledException(dbus.DBusException):
    _dbus_error_name = "net.connman.Error.Canceled"


class ConnLaunchBrowserException(dbus.DBusException):
    _dbus_error_name = "net.connman.Agent.Error.LaunchBrowser"
