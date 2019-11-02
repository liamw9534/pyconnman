from __future__ import unicode_literals
from __future__ import print_function
from mock_dbus import MockDBusInterface

import unittest

import pyconnman
import mock
import dbus


class ConnServiceTest(unittest.TestCase):

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

    def test_service_basic(self):
        manager = pyconnman.ConnManager()
        services = manager.get_services()
        serv = pyconnman.ConnService(services[0][0])
        print("Serv:", serv)
        print('=========================================================')
        serv.connect()
        serv.disconnect()
        serv.move_before('a service')
        serv.move_after('a service')
        serv.reset_counters()
        serv.remove()
        serv.clear_property('a property')
