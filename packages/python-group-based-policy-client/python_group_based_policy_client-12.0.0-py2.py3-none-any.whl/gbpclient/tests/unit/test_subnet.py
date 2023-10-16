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

from gbpclient.gbp.v2_0 import subnet as subnet_ext
from gbpclient.tests.unit import test_cli20
from openstackclient.network.v2 import subnet
from openstackclient.tests.unit.network.v2 import fakes as network_fakes
from openstackclient.tests.unit.network.v2 import test_subnet


# Tests for subnet create for APIC extensions
#
class TestSubnetCreate(test_subnet.TestSubnet, test_cli20.CLITestV20Base):

    def setUp(self):
        super(TestSubnetCreate, self).setUp()
        self._subnet = network_fakes.FakeSubnet.create_one_subnet(
            attrs={
                'tenant_id': '1',
            }
        )
        self._network = network_fakes.FakeNetwork.create_one_network(
            attrs={
                'id': self._subnet.network_id,
            }
        )
        self.network.create_subnet = mock.Mock(return_value=self._subnet)
        self.network.find_network = mock.Mock(return_value=self._network)
        self.cmd = subnet.CreateSubnet(self.app, self.namespace)

    def test_create_default_options(self):
        arglist = [
            "--subnet-range", self._subnet.cidr,
            "--network", self._subnet.network_id,
            self._subnet.name,
        ]
        verifylist = [
            ('name', self._subnet.name),
            ('network', self._subnet.network_id),
            ('apic_snat_host_pool_enable', None),
            ('apic_active_active_aap_enable', None),
            ('apic_snat_subnet_only_enable', None),
            ('apic_epg_subnet', False)
        ]
        create_ext = subnet_ext.CreateSubnetExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_subnet.assert_called_once_with(**{
            'ip_version': 4,
            'cidr': '10.10.10.0/24',
            'name': self._subnet.name,
            'network_id': self._subnet.network_id,
        })

    def test_create_all_options(self):
        arglist = [
            "--subnet-range", self._subnet.cidr,
            "--network", self._subnet.network_id,
            self._subnet.name,
            "--apic-snat-host-pool-enable",
            "--apic-active-active-aap-enable",
            "--apic-snat-subnet-only-enable",
            "--apic-epg-subnet"
        ]
        verifylist = [
            ('name', self._subnet.name),
            ('network', self._subnet.network_id),
            ('apic_snat_host_pool_enable', True),
            ('apic_active_active_aap_enable', True),
            ('apic_snat_subnet_only_enable', True),
            ('apic_epg_subnet', True)
        ]
        create_ext = subnet_ext.CreateSubnetExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_subnet.assert_called_once_with(**{
            'ip_version': 4,
            'cidr': '10.10.10.0/24',
            'name': self._subnet.name,
            'network_id': self._subnet.network_id,
            'apic:active_active_aap': True,
            'apic:snat_host_pool': True,
            'apic:snat_subnet_only': True,
            'apic:epg_subnet': True
        })


# Tests for subnet set for APIC extensions
#
class TestSubnetSet(test_subnet.TestSubnet, test_cli20.CLITestV20Base):

    _subnet = test_subnet.TestSetSubnet._subnet

    def setUp(self):
        super(TestSubnetSet, self).setUp()
        self.network.update_subnet = mock.Mock(return_value=None)
        self.network.find_subnet = mock.Mock(return_value=self._subnet)
        self.cmd = subnet.SetSubnet(self.app, self.namespace)

    def test_set_no_options(self):
        arglist = [
            self._subnet.name,
        ]
        verifylist = [
            ('subnet', self._subnet.name),
            ('apic_snat_host_pool_enable', None),
            ('apic_snat_subnet_only_enable', None),
        ]
        set_ext = subnet_ext.SetSubnetExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, set_ext)
        result = self.cmd.take_action(parsed_args)

        self.assertFalse(self.network.update_subnet.called)
        self.assertIsNone(result)

    def test_set_all_valid_options(self):
        arglist = [
            self._subnet.name,
            "--apic-snat-host-pool-disable",
            "--apic-snat-subnet-only-disable",
        ]
        verifylist = [
            ('subnet', self._subnet.name),
            ('apic_snat_host_pool_disable', True),
            ('apic_snat_subnet_only_disable', True),
        ]
        set_ext = subnet_ext.SetSubnetExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, set_ext)
        result = self.cmd.take_action(parsed_args)

        attrs = {
            'apic:snat_host_pool': False,
            'apic:snat_subnet_only': False,
        }
        self.network.update_subnet.assert_called_with(self._subnet, **attrs)
        self.assertIsNone(result)
