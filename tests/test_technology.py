from __future__ import unicode_literals
from __future__ import print_function
from mock_dbus import MockDBusInterface

import unittest

import pyconnman
import mock
import dbus


class ConnTechnologyTest(unittest.TestCase):

    def setUp(self):
        patcher = mock.patch('dbus.Interface', MockDBusInterface)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch('dbus.SystemBus')
        patched_system_bus = patcher.start()
        self.addCleanup(patcher.stop)
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = dbus.ObjectPath('/')
        self.mock_system_bus = mock_system_bus

    def test_scan(self):
        manager = pyconnman.ConnManager()
        technologies = manager.get_technologies()
        tech = pyconnman.ConnTechnology(technologies[0][0])
        print(repr(tech))
        print('=========================================================')
        print(tech)
        print('=========================================================')
        added = 'Added'
        removed = 'Removed'
        signal = pyconnman.ConnManager.SIGNAL_SERVICES_CHANGED
        user = mock.MagicMock()
        manager.add_signal_receiver(user.callback_fn, signal, self)
        tech.scan()
        self.mock_system_bus.add_signal_receiver.assert_called()
        cb = self.mock_system_bus.add_signal_receiver.call_args_list[0][0][0]
        cb(added, removed)
        user.callback_fn.assert_called_with(signal, self, added, removed)
        user.callback_fn.assert_called()
        manager.remove_signal_receiver(signal)
        self.mock_system_bus.remove_signal_receiver.assert_called()
