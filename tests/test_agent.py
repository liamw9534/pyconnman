from __future__ import unicode_literals

from builtins import str
import unittest

import pyconnman
import mock
import dbus


class AgentTest(unittest.TestCase):

    @mock.patch('dbus.SystemBus')
    def test_simple_wifi_agent(self, patched_system_bus):
        mock_system_bus = mock.MagicMock()
        patched_system_bus.return_value = mock_system_bus
        mock_system_bus.get_object.return_value = \
            dbus.ObjectPath('/net/connman')
        obj_path = '/test/agent'
        agent = pyconnman.SimpleWifiAgent(obj_path)

        # Raise an error
        path = '/service1'
        fields = {'Error': 'An error has occurred'}
        str_error = ""
        exception_raised = False
        try:
            agent.RequestInput(path, fields)
        except pyconnman.ConnCanceledException as error:
            exception_raised = True
            str_error = str(error)
        self.assertTrue(exception_raised)
        self.assertEqual(str_error, 'net.connman.Error.Canceled: Canceled')

        # Requesting a passphrase for WPA2 network
        #
        # --> RequestInput('/service1',
        #        { 'Passphrase': { 'Type': 'psk',
        #                   'Requirement': 'mandatory'
        #                 }
        #        })
        # <-- Returns { 'Passphrase' : 'secret123' }
        path = '/service1'
        fields = {'Passphrase': {'Type': 'psk',
                                 'Requirement': 'mandatory',
                                 }
                  }
        agent.set_service_params('/service1', passphrase='secret123')
        resp = agent.RequestInput(path, fields)
        self.assertEqual(resp.get('Passphrase'), 'secret123')

        agent.set_service_params('/service1')  # Clear all params
        str_error = ""
        exception_raised = False
        try:
            resp = agent.RequestInput(path, fields)
        except pyconnman.ConnCanceledException as error:
            exception_raised = True
            str_error = str(error)
        self.assertTrue(exception_raised)
        self.assertEqual(str_error,
                         'net.connman.Error.Canceled: '
                         'Field(s) not configured by user')

        #  Requesting name for hidden network
        #
        # --> RequestInput('/service2',
        #         { 'Name' : { 'Type'        : 'string',
        #                  'Requirement' : 'mandatory',
        #                  'Alternates'  : [ 'SSID' ]
        #                },
        #           'SSID' : { 'Type'        : 'ssid',
        #                  'Requirement' : 'alternate'
        #                }
        #         }
        # <-- Returns { 'Name' : 'My hidden network' }
        path = '/service2'
        fields = {'Name': {'Type': 'string',
                           'Requirement': 'mandatory',
                           'Alternates': ['SSID']
                           },
                  'SSID': {'Type': 'ssid',
                           'Requirement': 'alternate'
                           }
                  }

        agent.set_service_params('/service2', name='My hidden network')
        resp = agent.RequestInput(path, fields)
        self.assertEqual(resp.get('Name'), 'My hidden network')

        agent.set_service_params('/service2')  # Clear params
        str_error = ""
        exception_raised = False
        try:
            resp = agent.RequestInput(path, fields)
        except pyconnman.ConnCanceledException as error:
            exception_raised = True
            str_error = str(error)
        self.assertTrue(exception_raised)
        self.assertEqual(str_error,
                         'net.connman.Error.Canceled: '
                         'Field(s) not configured by user')

        # Requesting a passphrase for a WPA2 network with WPS alternative:
        #
        # --> RequestInput('/service3',
        #         { 'Passphrase' : { 'Type'        : 'psk',
        #                    'Requirement' : 'mandatory',
        #                    'Alternates'  : [ 'WPS' ]
        #                  },
        #           'WPS'        : { 'Type'        : 'wpspin',
        #                    'Requirement' : 'alternate'
        #                  }
        #         }
        # <-- Returns { 'WPS' : '123456' }
        path = '/service3'
        fields = {'Passphrase': {'Type': 'psk',
                                 'Requirement': 'mandatory',
                                 'Alternates': ['WPS']
                                 },
                  'WPS': {'Type': 'wpspin',
                          'Requirement': 'alternate'
                          }
                  }

        agent.set_service_params('/service3', wpspin='123456')
        resp = agent.RequestInput(path, fields)
        self.assertEqual(resp.get('WPS'), '123456')

        agent.set_service_params('/service3')  # Clear params
        exception_raised = False
        str_error = ""
        try:
            resp = agent.RequestInput(path, fields)
        except pyconnman.ConnCanceledException as error:
            exception_raised = True
            str_error = str(error)
        self.assertTrue(exception_raised)
        self.assertEqual(str_error,
                         'net.connman.Error.Canceled: '
                         'Field(s) not configured by user')

        # Requesting passphrase for a WPA-Enterprise network:
        #
        # --> RequestInput('/service4',
        #         { 'Identity'   : { 'Type'        : 'string',
        #                    'Requirement' : 'mandatory'
        #                  },
        #           'Passphrase' : { 'Type'        : 'passphrase',
        #                    'Requirement' : 'mandatory'
        #                  }
        #         }
        #
        # <-- Returns { 'Identity' : 'alice', 'Passphrase': 'secret123' }

        path = '/service4'
        fields = {'Identity': {'Type': 'string',
                               'Requirement': 'mandatory'
                               },
                  'Passphrase': {'Type': 'passphrase',
                                 'Requirement': 'mandatory'
                                 }
                  }

        agent.set_service_params('/service4', identity='alice',
                                 passphrase='secret123')
        resp = agent.RequestInput(path, fields)
        self.assertEqual(resp.get('Identity'), 'alice')
        self.assertEqual(resp.get('Passphrase'), 'secret123')

        agent.set_service_params('/service4')  # Clear params
        exception_raised = False
        str_error = ""
        try:
            resp = agent.RequestInput(path, fields)
        except pyconnman.ConnCanceledException as error:
            exception_raised = True
            str_error = str(error)
        self.assertTrue(exception_raised)
        self.assertEqual(str_error,
                         'net.connman.Error.Canceled: '
                         'Identity not configured by user')

        # Requesting username and password for a WISPr-enabled hotspot:
        #
        #    <-- RequestInput('/service5',
        #        { 'Username'   : { 'Type'        : 'string',
        #                   'Requirement' : 'mandatory'
        #                 },
        #          'Password'   : { 'Type'        : 'passphrase',
        #                   'Requirement' : 'mandatory'
        #                 }
        #        }
        #
        #    --> { 'Username' : 'foo', 'Password': 'secret' }
        path = '/service5'
        fields = {'Username': {'Type': 'string',
                               'Requirement': 'mandatory'
                               },
                  'Password': {'Type': 'passphrase',
                               'Requirement': 'mandatory'
                               }
                  }
        agent.set_service_params('/service5', username='foo',
                                 password='secret')
        resp = agent.RequestInput(path, fields)
        self.assertEqual(resp.get('Username'), 'foo')
        self.assertEqual(resp.get('Password'), 'secret')

        agent.set_service_params('/service5')
        exception_raised = False
        str_error = ""
        try:
            resp = agent.RequestInput(path, fields)
        except pyconnman.ConnCanceledException as error:
            exception_raised = True
            str_error = str(error)
        self.assertTrue(exception_raised)
        self.assertEqual(str_error,
                         'net.connman.Error.Canceled: '
                         'Username not configured by user')

        agent.set_service_params('/service5', username='foo')
        exception_raised = False
        str_error = ""
        try:
            resp = agent.RequestInput(path, fields)
        except pyconnman.ConnCanceledException as error:
            exception_raised = True
            str_error = str(error)
        self.assertTrue(exception_raised)
        self.assertEqual(str_error,
                         'net.connman.Error.Canceled: '
                         'Password not configured by user')

        agent.Cancel()
        agent.RequestBrowser(path, 'url')
        agent.Release()
        agent.ReportError(path, 'An error')
