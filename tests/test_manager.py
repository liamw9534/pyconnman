from __future__ import unicode_literals
from __future__ import print_function
from mock_dbus import MockDBusInterface

import unittest

import pyconnman
import mock
import dbus


class ConnManagerTest(unittest.TestCase):

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

    def test_manager_basic(self):
        manager = pyconnman.ConnManager()
        print(repr(manager))
        print('=========================================================')
        print(manager)
        print('=========================================================')
        print('Technologies:', manager.get_technologies())
        print('Services:', manager.get_services())

    def test_agent_registration(self):
        agent = '/agent/myagent'
        manager = pyconnman.ConnManager()
        exception_raised = False
        try:
            manager.register_agent(agent)
            manager.unregister_agent(agent)
        except dbus.Exception:
            exception_raised = True
        self.assertFalse(exception_raised)
