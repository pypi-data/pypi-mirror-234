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
Subnet extension implementations
"""

from cliff import hooks
from openstack.network.v2 import subnet as subnet_sdk
from openstack import resource
from openstackclient.network.v2 import subnet

from openstackclient.i18n import _


_get_attrs_subnet_new = subnet._get_attrs


def _get_attrs_subnet_extension(client_manager, parsed_args, is_create=True):
    attrs = _get_attrs_subnet_new(client_manager, parsed_args, is_create)
    if parsed_args.apic_snat_host_pool_enable:
        attrs['apic:snat_host_pool'] = True
    if parsed_args.apic_snat_host_pool_disable:
        attrs['apic:snat_host_pool'] = False
    if ('apic_active_active_aap_enable' in parsed_args and
        parsed_args.apic_active_active_aap_enable):
        attrs['apic:active_active_aap'] = True
    if ('apic_active_active_aap_disable' in parsed_args and
        parsed_args.apic_active_active_aap_disable):
        attrs['apic:active_active_aap'] = False
    if parsed_args.apic_snat_subnet_only_enable:
        attrs['apic:snat_subnet_only'] = True
    if parsed_args.apic_snat_subnet_only_disable:
        attrs['apic:snat_subnet_only'] = False
    if ('apic_epg_subnet' in parsed_args and
        parsed_args.apic_epg_subnet):
        attrs['apic:epg_subnet'] = True

    return attrs


subnet._get_attrs = _get_attrs_subnet_extension

subnet_sdk.Subnet.apic_distinguished_names = resource.Body(
    'apic:distinguished_names')
subnet_sdk.Subnet.apic_synchronization_state = resource.Body(
    'apic:synchronization_state')
subnet_sdk.Subnet.apic_snat_host_pool = resource.Body(
    'apic:snat_host_pool')
subnet_sdk.Subnet.apic_active_active_aap = resource.Body(
    'apic:active_active_aap')
subnet_sdk.Subnet.apic_snat_subnet_only = resource.Body(
    'apic:snat_subnet_only')
subnet_sdk.Subnet.apic_epg_subnet = resource.Body(
    'apic:epg_subnet')


class CreateSubnetExtension(hooks.CommandHook):

    def get_parser(self, parser):
        parser.add_argument(
            '--apic-snat-host-pool-enable',
            action='store_true',
            default=None,
            dest='apic_snat_host_pool_enable',
            help=_("Set APIC snat host pool to true\n"
                   "Default value for apic_snat_host_pool is False ")
        )
        parser.add_argument(
            '--apic-snat-host-pool-disable',
            action='store_true',
            dest='apic_snat_host_pool_disable',
            help=_("Set APIC snat host pool to false\n"
                   "Default value for apic_snat_host_pool is False ")
        )
        parser.add_argument(
            '--apic-active-active-aap-enable',
            action='store_true',
            default=None,
            dest='apic_active_active_aap_enable',
            help=_("Set APIC active active aap to true\n"
                   "Default value for apic_active_active_aap is False ")
        )
        parser.add_argument(
            '--apic-active-active-aap-disable',
            action='store_true',
            dest='apic_active_active_aap_disable',
            help=_("Set APIC active active aap to false\n"
                   "Default value for apic_active_active_aap is False ")
        )
        parser.add_argument(
            '--apic-snat-subnet-only-enable',
            action='store_true',
            default=None,
            dest='apic_snat_subnet_only_enable',
            help=_("Set APIC snat subnet only to true\n"
                   "Default value for apic_snat_subnet_only is False ")
        )
        parser.add_argument(
            '--apic-snat-subnet-only-disable',
            action='store_true',
            dest='apic_snat_subnet_only_disable',
            help=_("Set APIC snat subnet only to false\n"
                   "Default value for apic_snat_subnet_only is False ")
        )
        parser.add_argument(
            '--apic-epg-subnet',
            action='store_true',
            default=False,
            dest='apic_epg_subnet',
            help=_("Set APIC epg subnet to true\n"
                   "Default value for apic_epg_subnet is False ")
        )
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code


class SetSubnetExtension(hooks.CommandHook):

    def get_parser(self, parser):
        parser.add_argument(
            '--apic-snat-host-pool-enable',
            action='store_true',
            default=None,
            dest='apic_snat_host_pool_enable',
            help=_("Set APIC snat host pool to true\n"
                   "Default value for apic_snat_host_pool is False ")
        )
        parser.add_argument(
            '--apic-snat-host-pool-disable',
            action='store_true',
            dest='apic_snat_host_pool_disable',
            help=_("Set APIC snat host pool to false\n"
                   "Default value for apic_snat_host_pool is False ")
        )
        parser.add_argument(
            '--apic-snat-subnet-only-enable',
            action='store_true',
            default=None,
            dest='apic_snat_subnet_only_enable',
            help=_("Set APIC snat subnet only to true\n"
                   "Default value for apic_snat_subnet_only is False ")
        )
        parser.add_argument(
            '--apic-snat-subnet-only-disable',
            action='store_true',
            dest='apic_snat_subnet_only_disable',
            help=_("Set APIC snat subnet only to false\n"
                   "Default value for apic_snat_subnet_only is False ")
        )
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code


class ShowSubnetExtension(hooks.CommandHook):

    def get_parser(self, parser):
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code
