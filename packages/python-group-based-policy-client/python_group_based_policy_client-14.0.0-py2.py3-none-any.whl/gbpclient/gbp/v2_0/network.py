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

"""
Network extension implementations
"""

from cliff import hooks
from openstack.network.v2 import network as network_sdk
from openstack import resource
from openstackclient.network.v2 import network
from osc_lib.cli import parseractions

from openstackclient.i18n import _


_get_attrs_network_new = network._get_attrs_network


def _get_attrs_network_extension(client_manager, parsed_args):
    attrs = _get_attrs_network_new(client_manager, parsed_args)
    if ('apic_svi_enable' in parsed_args and
        parsed_args.apic_svi_enable):
        attrs['apic:svi'] = True
    if ('apic_svi_disable' in parsed_args and
        parsed_args.apic_svi_disable):
        attrs['apic:svi'] = False
    if parsed_args.apic_bgp_enable:
        attrs['apic:bgp_enable'] = True
    if parsed_args.apic_bgp_disable:
        attrs['apic:bgp_enable'] = False
    if parsed_args.apic_bgp_type:
        attrs['apic:bgp_type'] = parsed_args.apic_bgp_type
    if parsed_args.apic_bgp_asn:
        attrs['apic:bgp_asn'] = parsed_args.apic_bgp_asn
    if parsed_args.apic_nested_domain_name:
        attrs['apic:nested_domain_name'
              ] = parsed_args.apic_nested_domain_name
    if parsed_args.apic_nested_domain_type:
        attrs['apic:nested_domain_type'
              ] = parsed_args.apic_nested_domain_type
    if parsed_args.apic_nested_domain_infra_vlan:
        attrs['apic:nested_domain_infra_vlan'
              ] = parsed_args.apic_nested_domain_infra_vlan
    if parsed_args.apic_nested_domain_service_vlan:
        attrs['apic:nested_domain_service_vlan'
              ] = parsed_args.apic_nested_domain_service_vlan
    if parsed_args.apic_nested_domain_node_network_vlan:
        attrs['apic:nested_domain_node_network_vlan'
              ] = parsed_args.apic_nested_domain_node_network_vlan
    if parsed_args.apic_nested_domain_allowed_vlans:
        attrs['apic:nested_domain_allowed_vlans'
              ] = list(map(int,
                           parsed_args.apic_nested_domain_allowed_vlans.split(
                               ",")))
    if parsed_args.apic_extra_provided_contracts is not None:
        if parsed_args.apic_extra_provided_contracts:
            attrs['apic:extra_provided_contracts'
                  ] = parsed_args.apic_extra_provided_contracts.split(",")
        else:
            attrs['apic:extra_provided_contracts'] = []

    if parsed_args.apic_extra_consumed_contracts is not None:
        if parsed_args.apic_extra_consumed_contracts:
            attrs['apic:extra_consumed_contracts'
                  ] = parsed_args.apic_extra_consumed_contracts.split(",")
        else:
            attrs['apic:extra_consumed_contracts'] = []
    if parsed_args.apic_epg_contract_masters:
        attrs['apic:epg_contract_masters'
              ] = parsed_args.apic_epg_contract_masters.split(",")
    if ('apic_distinguished_names' in parsed_args and
        parsed_args.apic_distinguished_names):
        result = {}
        for element in parsed_args.apic_distinguished_names:
            result.update(element)
        attrs['apic:distinguished_names'] = result
    if parsed_args.apic_policy_enforcement_pref:
        attrs['apic:policy_enforcement_pref'
              ] = parsed_args.apic_policy_enforcement_pref
    if parsed_args.apic_no_nat_cidrs:
        attrs['apic:no_nat_cidrs'] = parsed_args.apic_no_nat_cidrs.split(",")
    if ('no_apic_no_nat_cidrs' in parsed_args and
        parsed_args.no_apic_no_nat_cidrs):
        attrs['apic:no_nat_cidrs'] = []
    if parsed_args.external:
        if ('apic_nat_type' in parsed_args and
            parsed_args.apic_nat_type is not None):
            attrs['apic:nat_type'] = parsed_args.apic_nat_type
        if parsed_args.apic_external_cidrs:
            attrs['apic:external_cidrs'
                  ] = parsed_args.apic_external_cidrs.split(",")
        if ('apic_no_external_cidrs' in parsed_args and
            parsed_args.apic_no_external_cidrs):
            attrs['apic:external_cidrs'] = []
    return attrs


network._get_attrs_network = _get_attrs_network_extension

network_sdk.Network.apic_synchronization_state = resource.Body(
    'apic:synchronization_state')
network_sdk.Network.apic_svi = resource.Body('apic:svi')
network_sdk.Network.apic_bgp = resource.Body('apic:bgp_enable')
network_sdk.Network.apic_bgp_type = resource.Body('apic:bgp_type')
network_sdk.Network.apic_bgp_asn = resource.Body('apic:bgp_asn')
network_sdk.Network.apic_nested_domain_name = resource.Body(
    'apic:nested_domain_name')
network_sdk.Network.apic_nested_domain_type = resource.Body(
    'apic:nested_domain_type')
network_sdk.Network.apic_nested_domain_infra_vlan = resource.Body(
    'apic:nested_domain_infra_vlan')
network_sdk.Network.apic_nested_domain_service_vlan = resource.Body(
    'apic:nested_domain_service_vlan')
network_sdk.Network.apic_nested_domain_node_network_vlan = resource.Body(
    'apic:nested_domain_node_network_vlan')
network_sdk.Network.apic_nested_domain_allowed_vlans = resource.Body(
    'apic:nested_domain_allowed_vlans')
network_sdk.Network.apic_extra_provided_contracts = resource.Body(
    'apic:extra_provided_contracts')
network_sdk.Network.apic_extra_consumed_contracts = resource.Body(
    'apic:extra_consumed_contracts')
network_sdk.Network.apic_epg_contract_masters = resource.Body(
    'apic:epg_contract_masters')
network_sdk.Network.apic_distinguished_names = resource.Body(
    'apic:distinguished_names')
network_sdk.Network.apic_policy_enforcement_pref = resource.Body(
    'apic:policy_enforcement_pref')
network_sdk.Network.apic_nat_type = resource.Body('apic:nat_type')
network_sdk.Network.apic_external_cidrs = resource.Body('apic:external_cidrs')
network_sdk.Network.apic_no_nat_cidrs = resource.Body('apic:no_nat_cidrs')


class CreateNetworkExtension(hooks.CommandHook):

    def get_parser(self, parser):
        parser.add_argument(
            '--apic-svi-enable',
            action='store_true',
            default=None,
            dest='apic_svi_enable',
            help=_("Set APIC SVI to true\n"
                   "Default value for apic_svi is False ")
        )
        parser.add_argument(
            '--apic-svi-disable',
            action='store_true',
            dest='apic_svi_disable',
            help=_("Set APIC SVI to false\n"
                   "Default value for apic_svi is False ")
        )
        parser.add_argument(
            '--apic-bgp-enable',
            action='store_true',
            default=None,
            dest='apic_bgp_enable',
            help=_("Set APIC BGP to true\n"
                   "Default value for apic_bgp is False ")
        )
        parser.add_argument(
            '--apic-bgp-disable',
            action='store_true',
            dest='apic_bgp_disable',
            help=_("Set APIC BGP to false\n"
                   "Default value for apic_bgp is False ")
        )
        parser.add_argument(
            '--apic-bgp-type',
            metavar="<string>",
            dest='apic_bgp_type',
            help=_("APIC BGP Type\n"
                   "Default value is 'default_export'\n"
                   "Valid values: default_export, '' ")
        )
        parser.add_argument(
            '--apic-bgp-asn',
            metavar="<integer>",
            dest='apic_bgp_asn',
            help=_("APIC BGP ASN\n"
                   "Default value is 0\n"
                   "Valid values: non negative integer ")
        )
        parser.add_argument(
            '--apic-nested-domain-name',
            metavar="<string>",
            dest='apic_nested_domain_name',
            help=_("APIC nested domain name\n"
                   "Default value is '' ")
        )
        parser.add_argument(
            '--apic-nested-domain-type',
            metavar="<string>",
            dest='apic_nested_domain_type',
            help=_("APIC nested domain type\n"
                   "Default value is '' ")
        )
        parser.add_argument(
            '--apic-nested-domain-infra-vlan',
            metavar="<integer>",
            dest='apic_nested_domain_infra_vlan',
            help=_("APIC nested domain infra vlan\n"
                   "Valid values: integer between 1 and 4093 ")
        )
        parser.add_argument(
            '--apic-nested-domain-service-vlan',
            metavar="<integer>",
            dest='apic_nested_domain_service_vlan',
            help=_("APIC nested domain service vlan\n"
                   "Valid values: integer between 1 and 4093 ")
        )
        parser.add_argument(
            '--apic-nested-domain-node-network-vlan',
            metavar="<integer>",
            dest='apic_nested_domain_node_network_vlan',
            help=_("APIC nested domain node network vlan\n"
                   "Valid values: integer between 1 and 4093 ")
        )
        parser.add_argument(
            '--apic-nested-domain-allowed-vlans',
            metavar="<int,int>",
            dest='apic_nested_domain_allowed_vlans',
            help=_("APIC nested domain allowed vlans\n"
                   "Data is passed as comma separated integers\n"
                   "Valid values: integers between 1 and 4093\n"
                   "Syntax Example: 1 or 1,2 ")
        )
        parser.add_argument(
            '--apic-extra-provided-contracts',
            metavar="<aaa,bbb>",
            dest='apic_extra_provided_contracts',
            help=_("APIC extra provided contracts\n"
                   "Data is passed as comma separated strings\n"
                   "Default value is []\n"
                   "Valid values: list of unique strings\n"
                   "Syntax Example: foo or foo,bar ")
        )
        parser.add_argument(
            '--apic-extra-consumed-contracts',
            metavar="<aaa,bbb>",
            dest='apic_extra_consumed_contracts',
            help=_("APIC extra consumed contracts\n"
                   "Data is passed as comma separated strings\n"
                   "Default value is []\n"
                   "Valid values: list of unique strings\n"
                   "Syntax Example: foo or foo,bar ")
        )
        parser.add_argument(
            '--apic-epg-contract-masters',
            metavar="<aaa,bbb>",
            dest='apic_epg_contract_masters',
            help=_("APIC epg contract masters\n"
                   "Data is passed as comma separated strings\n"
                   "Default value is []\n"
                   "Syntax Example: foo or foo,bar ")
        )
        parser.add_argument(
            '--apic-distinguished-names',
            metavar="<ExternalNetwork=aaa,BridgeDomain=bbb>",
            dest='apic_distinguished_names',
            action=parseractions.MultiKeyValueAction,
            optional_keys=['ExternalNetwork', 'BridgeDomain'],
            help=_("APIC distinguished names\n"
                   "Custom data to be passed as apic:distinguished_names\n"
                   "Data is passed as <key>=<value>, where "
                   "valid keys are 'ExternalNetwork' and 'BridgeDomain'\n"
                   "Both the keys are optional\n"
                   "Syntax Example: BridgeDomain=aaa or ExternalNetwork=bbb "
                   "or ExternalNetwork=aaa,BridgeDomain=bbb ")
        )
        parser.add_argument(
            '--apic-policy-enforcement-pref',
            metavar="<string>",
            dest='apic_policy_enforcement_pref',
            help=_("APIC Policy Enforcement Pref\n"
                   "Default value is 'unenforced'\n"
                   "Valid values: unenforced, enforced, '' ")
        )
        parser.add_argument(
            '--apic-nat-type',
            metavar="<string>",
            dest='apic_nat_type',
            help=_("APIC nat type for external network\n"
                   "For external type networks only\n"
                   "Default value is 'distributed'\n"
                   "Valid values: distributed, edge, '' ")
        )
        parser.add_argument(
            '--apic-external-cidrs',
            metavar="<subnet1,subnet2>",
            dest='apic_external_cidrs',
            help=_("APIC external CIDRS for external network\n"
                   "For external type networks only\n"
                   "Data is passed as comma separated valid ip subnets\n"
                   "Default value is ['0.0.0.0/0']\n"
                   "Syntax Example: 10.10.10.0/24 "
                   "or 10.10.10.0/24,20.20.20.0/24 ")
        )
        parser.add_argument(
            '--apic-no-nat-cidrs',
            metavar="<subnet1,subnet2>",
            dest='apic_no_nat_cidrs',
            help=_("APIC CIDRS for a network to config no NAT routing\n"
                   "Data is passed as comma separated valid ip subnets\n"
                   "Default value is []\n"
                   "Syntax Example: 10.10.10.0/24 "
                   "or 10.10.10.0/24,20.20.20.0/24 ")
        )
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code


class SetNetworkExtension(hooks.CommandHook):

    def get_parser(self, parser):
        parser.add_argument(
            '--apic-bgp-enable',
            action='store_true',
            default=None,
            dest='apic_bgp_enable',
            help=_("Set APIC BGP to true\n"
                   "Default value for apic_bgp is False ")
        )
        parser.add_argument(
            '--apic-bgp-disable',
            action='store_true',
            dest='apic_bgp_disable',
            help=_("Set APIC BGP to false\n"
                   "Default value for apic_bgp is False ")
        )
        parser.add_argument(
            '--apic-bgp-type',
            metavar="<string>",
            dest='apic_bgp_type',
            help=_("APIC BGP Type\n"
                   "Default value is 'default_export'\n"
                   "Valid values: default_export, '' ")
        )
        parser.add_argument(
            '--apic-bgp-asn',
            metavar="<integer>",
            dest='apic_bgp_asn',
            help=_("APIC BGP ASN\n"
                   "Default value is 0\n"
                   "Valid values: non negative integer ")
        )
        parser.add_argument(
            '--apic-nested-domain-name',
            metavar="<string>",
            dest='apic_nested_domain_name',
            help=_("APIC nested domain name\n"
                   "Default value is '' ")
        )
        parser.add_argument(
            '--apic-nested-domain-type',
            metavar="<string>",
            dest='apic_nested_domain_type',
            help=_("APIC nested domain type\n"
                   "Default value is '' ")
        )
        parser.add_argument(
            '--apic-nested-domain-infra-vlan',
            metavar="<integer>",
            dest='apic_nested_domain_infra_vlan',
            help=_("APIC nested domain infra vlan\n"
                   "Valid values: integer between 1 and 4093 ")
        )
        parser.add_argument(
            '--apic-nested-domain-service-vlan',
            metavar="<integer>",
            dest='apic_nested_domain_service_vlan',
            help=_("APIC nested domain service vlan\n"
                   "Valid values: integer between 1 and 4093 ")
        )
        parser.add_argument(
            '--apic-nested-domain-node-network-vlan',
            metavar="<integer>",
            dest='apic_nested_domain_node_network_vlan',
            help=_("APIC nested domain node network vlan\n"
                   "Valid values: integer between 1 and 4093 ")
        )
        parser.add_argument(
            '--apic-nested-domain-allowed-vlans',
            metavar="<int,int>",
            dest='apic_nested_domain_allowed_vlans',
            help=_("APIC nested domain allowed vlans. "
                   "Data is passed as comma separated integers\n"
                   "Valid values: integers between 1 and 4093\n"
                   "Syntax Example: 1 or 1,2 ")
        )
        parser.add_argument(
            '--apic-extra-provided-contracts',
            metavar="<aaa,bbb>",
            dest='apic_extra_provided_contracts',
            help=_("APIC extra provided contracts\n"
                   "Data is passed as comma separated of strings.\n"
                   "Default value is []\n"
                   "Valid values: list of unique strings\n"
                   "Syntax Example: foo or foo,bar ")
        )
        parser.add_argument(
            '--apic-extra-consumed-contracts',
            metavar="<aaa,bbb>",
            dest='apic_extra_consumed_contracts',
            help=_("APIC extra consumed contracts\n"
                   "Data is passed as comma separated strings\n"
                   "Default value is []\n"
                   "Valid values: list of unique strings\n"
                   "Syntax Example: foo or foo,bar ")
        )
        parser.add_argument(
            '--apic-epg-contract-masters',
            metavar="<aaa,bbb,ccc>",
            dest='apic_epg_contract_masters',
            help=_("APIC epg contract masters\n"
                   "Data is passed as comma separated strings\n"
                   "Default value is []\n"
                   "Syntax Example: foo or foo,bar ")
        )
        parser.add_argument(
            '--apic-policy-enforcement-pref',
            metavar="<string>",
            dest='apic_policy_enforcement_pref',
            help=_("APIC Policy Enforcement Pref\n"
                   "Default value is 'unenforced'\n"
                   "Valid values: unenforced, enforced, '' ")
        )
        parser.add_argument(
            '--apic-external-cidrs',
            metavar="<subnet1,subnet2>",
            dest='apic_external_cidrs',
            help=_("APIC external CIDRS for external network\n"
                   "For external type networks only\n"
                   "Data is passed as comma separated valid ip subnets\n"
                   "Need to pass the --external argument wth this field\n"
                   "Default value is ['0.0.0.0/0']\n"
                   "Syntax Example: 10.10.10.0/24 "
                   "or 10.10.10.0/24,20.20.20.0/24 ")
        )
        parser.add_argument(
            '--apic-no-external-cidrs',
            dest='apic_no_external_cidrs',
            action='store_true',
            help=_("Reset APIC external CIDRS for external network\n"
                   "For external type networks only\n"
                   "Need to pass the --external argument wth this field\n"
                   "Resets the apic:external_cidrs field to 0.0.0.0/0 ")
        )
        parser.add_argument(
            '--apic-no-nat-cidrs',
            metavar="<subnet1,subnet2>",
            dest='apic_no_nat_cidrs',
            help=_("APIC CIDRS for a network to config no NAT routing\n"
                   "Data is passed as comma separated valid ip subnets\n"
                   "Default value is []\n"
                   "Syntax Example: 10.10.10.0/24 "
                   "or 10.10.10.0/24,20.20.20.0/24 ")
        )
        parser.add_argument(
            '--no-apic-no-nat-cidrs',
            dest='no_apic_no_nat_cidrs',
            action='store_true',
            help=_("Reset APIC no NAT CIDRS for a network\n"
                   "Resets the apic:no_nat_cidrs field to []")
        )
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code


class ShowNetworkExtension(hooks.CommandHook):

    def get_parser(self, parser):
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code
