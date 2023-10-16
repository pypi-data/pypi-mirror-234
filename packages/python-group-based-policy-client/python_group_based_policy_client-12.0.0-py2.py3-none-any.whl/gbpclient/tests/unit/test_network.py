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

from gbpclient.gbp.v2_0 import network as network_ext
from gbpclient.tests.unit import test_cli20
from openstackclient.network.v2 import network
from openstackclient.tests.unit.network.v2 import test_network


# Tests for network create with APIC extensions
#
class TestNetworkCreate(test_network.TestNetwork, test_cli20.CLITestV20Base):

    _network = test_network.TestCreateNetworkIdentityV3._network

    def setUp(self):
        super(TestNetworkCreate, self).setUp()
        self.network.create_network = mock.Mock(
            return_value=self._network)
        self.cmd = network.CreateNetwork(self.app, self.namespace)

    def test_create_default_options(self):
        arglist = [
            self._network.name,
            "--external",
        ]
        verifylist = [
            ('name', self._network.name),
            ('apic_nested_domain_name', None),
            ('apic_nested_domain_type', None),
            ('apic_distinguished_names', None),
            ('apic_nat_type', None),
            ('apic_external_cidrs', None),
            ('apic_svi_enable', None),
            ('apic_bgp_enable', None),
            ('apic_bgp_asn', None),
            ('apic_bgp_type', None),
            ('apic_nested_domain_infra_vlan', None),
            ('apic_nested_domain_allowed_vlans', None),
            ('apic_nested_domain_service_vlan', None),
            ('apic_nested_domain_node_network_vlan', None),
            ('apic_extra_provided_contracts', None),
            ('apic_extra_consumed_contracts', None),
            ('apic_policy_enforcement_pref', None),
            ('apic_no_nat_cidrs', None),
            ('apic_multi_ext_nets', None),
        ]
        create_ext = network_ext.CreateNetworkExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_network.assert_called_once_with(**{
            'admin_state_up': True,
            'name': self._network.name,
            'router:external': True,
        })

    def test_create_all_options(self):
        arglist = [
            self._network.name,
            "--external",
            "--apic-nested-domain-name", "dntest1",
            "--apic-nested-domain-type", "dntype1",
            "--apic-distinguished-names", 'ExternalNetwork=test1',
            "--apic-nat-type", "edge",
            "--apic-external-cidrs", '20.20.20.0/8',
            "--apic-svi-enable",
            "--apic-bgp-enable",
            "--apic-bgp-asn", '1',
            "--apic-bgp-type", "bgptest1",
            "--apic-nested-domain-infra-vlan", '1',
            "--apic-nested-domain-allowed-vlans", '2',
            "--apic-nested-domain-service-vlan", '3',
            "--apic-nested-domain-node-network-vlan", '4',
            "--apic-extra-provided-contracts", 'pcontest1',
            "--apic-extra-consumed-contracts", 'contest1',
            "--apic-policy-enforcement-pref", 'enforced',
            "--apic-no-nat-cidrs", '10.10.10.0/24',
            "--apic-multi-ext-nets",
        ]
        verifylist = [
            ('name', self._network.name),
            ('external', True),
            ('apic_nested_domain_name', "dntest1"),
            ('apic_nested_domain_type', "dntype1"),
            ('apic_distinguished_names', [{'ExternalNetwork': 'test1'}]),
            ('apic_nat_type', "edge"),
            ('apic_external_cidrs', '20.20.20.0/8'),
            ('apic_svi_enable', True),
            ('apic_bgp_enable', True),
            ('apic_bgp_asn', '1'),
            ('apic_bgp_type', "bgptest1"),
            ('apic_nested_domain_infra_vlan', '1'),
            ('apic_nested_domain_allowed_vlans', '2'),
            ('apic_nested_domain_service_vlan', '3'),
            ('apic_nested_domain_node_network_vlan', '4'),
            ('apic_extra_provided_contracts', 'pcontest1'),
            ('apic_extra_consumed_contracts', 'contest1'),
            ('apic_policy_enforcement_pref', 'enforced'),
            ('apic_no_nat_cidrs', '10.10.10.0/24'),
            ('apic_multi_ext_nets', True)
        ]
        create_ext = network_ext.CreateNetworkExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_network.assert_called_once_with(**{
            'admin_state_up': True,
            'name': self._network.name,
            'router:external': True,
            'apic:nested_domain_name': 'dntest1',
            'apic:distinguished_names': {"ExternalNetwork": "test1"},
            'apic:external_cidrs': ['20.20.20.0/8'],
            'apic:nat_type': 'edge',
            'apic:nested_domain_name': 'dntest1',
            'apic:nested_domain_type': 'dntype1',
            'apic:svi': True,
            'apic:bgp_enable': True,
            'apic:bgp_asn': '1',
            'apic:bgp_type': 'bgptest1',
            'apic:extra_consumed_contracts': ['contest1'],
            'apic:extra_provided_contracts': ['pcontest1'],
            'apic:nested_domain_allowed_vlans': [2],
            'apic:nested_domain_infra_vlan': '1',
            'apic:nested_domain_node_network_vlan': '4',
            'apic:nested_domain_service_vlan': '3',
            'apic:policy_enforcement_pref': 'enforced',
            'apic:no_nat_cidrs': ['10.10.10.0/24'],
            'apic:multi_ext_nets': True,
        })

    def test_create_empty_contracts(self):
        arglist = [
            self._network.name,
            "--apic-extra-provided-contracts", '',
            "--apic-extra-consumed-contracts", '',
        ]
        verifylist = [
            ('name', self._network.name),
            ('apic_extra_provided_contracts', ''),
            ('apic_extra_consumed_contracts', ''),
        ]
        create_ext = network_ext.CreateNetworkExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_network.assert_called_once_with(**{
            'admin_state_up': True,
            'name': self._network.name,
            'apic:extra_consumed_contracts': [],
            'apic:extra_provided_contracts': [],
        })

    def test_create_no_nat_option(self):
        arglist = [
            self._network.name,
            "--external",
            "--apic-distinguished-names", 'ExternalNetwork=test1',
            "--apic-nat-type", "",
            "--apic-external-cidrs", '20.20.20.0/8',
            "--apic-no-nat-cidrs", '10.10.10.0/24',
        ]
        verifylist = [
            ('name', self._network.name),
            ('external', True),
            ('apic_distinguished_names', [{'ExternalNetwork': 'test1'}]),
            ('apic_nat_type', ""),
            ('apic_external_cidrs', '20.20.20.0/8'),
            ('apic_no_nat_cidrs', '10.10.10.0/24'),
        ]
        create_ext = network_ext.CreateNetworkExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_network.assert_called_once_with(**{
            'admin_state_up': True,
            'name': self._network.name,
            'router:external': True,
            'apic:distinguished_names': {"ExternalNetwork": "test1"},
            'apic:external_cidrs': ['20.20.20.0/8'],
            'apic:nat_type': '',
            'apic:no_nat_cidrs': ['10.10.10.0/24'],
        })


# Tests for network set with APIC extensions
#
class TestNetworkSet(test_network.TestNetwork, test_cli20.CLITestV20Base):

    _network = test_network.TestSetNetwork._network

    def setUp(self):
        super(TestNetworkSet, self).setUp()
        self.network.update_network = mock.Mock(return_value=None)
        self.network.find_network = mock.Mock(return_value=self._network)
        self.cmd = network.SetNetwork(self.app, self.namespace)

    def test_set_no_options(self):
        arglist = [
            self._network.name,
        ]
        verifylist = [
            ('network', self._network.name),
            ('apic_nested_domain_name', None),
            ('apic_nested_domain_type', None),
            ('apic_external_cidrs', None),
            ('apic_bgp_enable', None),
            ('apic_bgp_asn', None),
            ('apic_bgp_type', None),
            ('apic_nested_domain_infra_vlan', None),
            ('apic_nested_domain_allowed_vlans', None),
            ('apic_nested_domain_service_vlan', None),
            ('apic_nested_domain_node_network_vlan', None),
            ('apic_extra_provided_contracts', None),
            ('apic_extra_consumed_contracts', None),
            ('apic_policy_enforcement_pref', None),
            ('apic_no_nat_cidrs', None),
        ]
        set_ext = network_ext.SetNetworkExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, set_ext)
        result = self.cmd.take_action(parsed_args)

        self.assertFalse(self.network.update_network.called)
        self.assertIsNone(result)

    def test_set_all_valid_options(self):
        arglist = [
            self._network.name,
            "--external",
            "--apic-nested-domain-name", "dntest11",
            "--apic-nested-domain-type", "dntype11",
            "--apic-external-cidrs", '30.30.30.0/8',
            "--apic-bgp-disable",
            "--apic-bgp-asn", '2',
            "--apic-bgp-type", "bgptest11",
            "--apic-nested-domain-infra-vlan", '2',
            "--apic-nested-domain-allowed-vlans", '2,3',
            "--apic-nested-domain-service-vlan", '4',
            "--apic-nested-domain-node-network-vlan", '5',
            "--apic-extra-provided-contracts", 'pcontest1,pcontest11',
            "--apic-extra-consumed-contracts", 'contest1,contest11',
            "--apic-policy-enforcement-pref", 'enforced',
            "--apic-no-nat-cidrs", '10.10.10.0/24',
        ]
        verifylist = [
            ('network', self._network.name),
            ('external', True),
            ('apic_nested_domain_name', "dntest11"),
            ('apic_nested_domain_type', "dntype11"),
            ('apic_external_cidrs', '30.30.30.0/8'),
            ('apic_bgp_disable', True),
            ('apic_bgp_asn', '2'),
            ('apic_bgp_type', "bgptest11"),
            ('apic_nested_domain_infra_vlan', '2'),
            ('apic_nested_domain_allowed_vlans', '2,3'),
            ('apic_nested_domain_service_vlan', '4'),
            ('apic_nested_domain_node_network_vlan', '5'),
            ('apic_extra_provided_contracts', 'pcontest1,pcontest11'),
            ('apic_extra_consumed_contracts', 'contest1,contest11'),
            ('apic_policy_enforcement_pref', 'enforced'),
            ('apic_no_nat_cidrs', '10.10.10.0/24'),
        ]
        set_ext = network_ext.SetNetworkExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, set_ext)
        result = self.cmd.take_action(parsed_args)

        attrs = {
            'router:external': True,
            'apic:nested_domain_name': 'dntest11',
            'apic:external_cidrs': ['30.30.30.0/8'],
            'apic:nested_domain_name': 'dntest11',
            'apic:nested_domain_type': 'dntype11',
            'apic:bgp_enable': False,
            'apic:bgp_asn': '2',
            'apic:bgp_type': 'bgptest11',
            'apic:extra_consumed_contracts': ['contest1', 'contest11'],
            'apic:extra_provided_contracts': ['pcontest1', 'pcontest11'],
            'apic:nested_domain_allowed_vlans': [2, 3],
            'apic:nested_domain_infra_vlan': '2',
            'apic:nested_domain_node_network_vlan': '5',
            'apic:nested_domain_service_vlan': '4',
            'apic:policy_enforcement_pref': 'enforced',
            'apic:no_nat_cidrs': ['10.10.10.0/24'],
        }

        self.network.update_network.assert_called_once_with(
            self._network, **attrs)
        self.assertIsNone(result)

    def test_set_apic_no_external_cidrs(self):
        arglist = [
            self._network.name,
            "--external",
            "--apic-no-external-cidrs",
            "--no-apic-no-nat-cidrs",
        ]
        verifylist = [
            ('network', self._network.name),
            ('external', True),
            ('apic_nested_domain_name', None),
            ('apic_nested_domain_type', None),
            ('apic_external_cidrs', None),
            ('apic_no_external_cidrs', True),
            ('apic_bgp_enable', None),
            ('apic_bgp_asn', None),
            ('apic_bgp_type', None),
            ('apic_nested_domain_infra_vlan', None),
            ('apic_nested_domain_allowed_vlans', None),
            ('apic_nested_domain_service_vlan', None),
            ('apic_nested_domain_node_network_vlan', None),
            ('apic_extra_provided_contracts', None),
            ('apic_extra_consumed_contracts', None),
            ('apic_policy_enforcement_pref', None),
            ('no_apic_no_nat_cidrs', True),
        ]
        set_ext = network_ext.SetNetworkExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, set_ext)
        result = self.cmd.take_action(parsed_args)

        attrs = {
            'router:external': True,
            'apic:external_cidrs': [],
            'apic:no_nat_cidrs': [],
        }

        self.network.update_network.assert_called_once_with(
            self._network, **attrs)
        self.assertIsNone(result)
