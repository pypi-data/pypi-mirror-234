#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

from unittest import mock

from gbpclient.gbp.v2_0 import port as port_ext
from gbpclient.tests.unit import test_cli20
from openstackclient.network.v2 import port
from openstackclient.tests.unit.network.v2 import fakes as network_fakes
from openstackclient.tests.unit.network.v2 import test_port


# Tests for port create with APIC extensions
#
class TestPortCreate(test_port.TestPort, test_cli20.CLITestV20Base):

    _port = test_port.TestCreatePort._port
    extension_details = (
        network_fakes.FakeExtension.create_one_extension()
    )

    def setUp(self):
        super(TestPortCreate, self).setUp()
        self.app.client_manager.network.find_extension = mock.Mock(
            return_value=self.extension_details)
        fake_net = network_fakes.create_one_network({
            'id': self._port.network_id,
        })
        self.network.find_network = mock.Mock(return_value=fake_net)
        self.network.create_port = mock.Mock(
            return_value=self._port)
        self.cmd = port.CreatePort(self.app, self.namespace)

    def test_create_default_options(self):
        arglist = [
            self._port.name,
            "--network", self._port.network_id,
        ]
        verifylist = [
            ('name', self._port.name),
            ('apic_erspan_config', None),
            ('no_apic_erspan_config', False),
        ]
        create_ext = port_ext.CreateAndSetPortExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_port.assert_called_once_with(**{
            'admin_state_up': True,
            'name': self._port.name,
            'network_id': self._port.network_id,
        })

    def test_create_all_options(self):
        arglist = [
            self._port.name,
            "--network", self._port.network_id,
            "--apic-erspan-config", "dest-ip=10.0.0.0,flow-id=1,direction=in",
        ]
        verifylist = [
            ('name', self._port.name),
            ('apic_erspan_config', [{'dest-ip': '10.0.0.0',
                                     'flow-id': '1',
                                     'direction': 'in'}]),
        ]
        create_ext = port_ext.CreateAndSetPortExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_port.assert_called_once_with(**{
            'admin_state_up': True,
            'name': self._port.name,
            'apic:erspan_config': [{"dest_ip": "10.0.0.0",
                                    "flow_id": "1",
                                    "direction": "in"}],
            'network_id': self._port.network_id,
        })


# Tests for port set with APIC extensions
#
class TestPortSet(test_port.TestPort, test_cli20.CLITestV20Base):

    _port = test_port.TestSetPort._port

    def setUp(self):
        super(TestPortSet, self).setUp()
        self.network.update_port = mock.Mock(return_value=None)
        self.network.find_port = mock.Mock(return_value=self._port)
        self.cmd = port.SetPort(self.app, self.namespace)

    def test_set_no_options(self):
        arglist = [
            self._port.name,
        ]
        verifylist = [
            ('port', self._port.name),
            ('apic_erspan_config', None),
            ('no_apic_erspan_config', False),
        ]
        set_ext = port_ext.CreateAndSetPortExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, set_ext)
        result = self.cmd.take_action(parsed_args)

        self.assertFalse(self.network.update_port.called)
        self.assertIsNone(result)

    def test_set_all_valid_options(self):
        arglist = [
            self._port.name,
            "--apic-erspan-config", "dest-ip=10.0.0.0,flow-id=1,direction=in",
        ]
        verifylist = [
            ('port', self._port.name),
            ('apic_erspan_config', [{'dest-ip': '10.0.0.0',
                                     'flow-id': '1',
                                     'direction': 'in'}]),
        ]
        set_ext = port_ext.CreateAndSetPortExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, set_ext)
        result = self.cmd.take_action(parsed_args)

        attrs = {
            'apic:erspan_config': [{"dest_ip": "10.0.0.0",
                                    "flow_id": "1",
                                    "direction": "in"}],
        }

        self.network.update_port.assert_called_once_with(
            self._port, **attrs)
        self.assertIsNone(result)
