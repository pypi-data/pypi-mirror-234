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
Address Scope extension implementations
"""

from cliff import hooks
from openstack.network.v2 import address_scope as address_scope_sdk
from openstack import resource
from openstackclient.network.v2 import address_scope
from osc_lib.cli import parseractions

from openstackclient.i18n import _


_get_attrs_address_scope_new = address_scope._get_attrs


def _get_attrs_address_scope_extension(client_manager, parsed_args):
    attrs = _get_attrs_address_scope_new(client_manager, parsed_args)
    if ('apic_distinguished_names' in parsed_args and
        parsed_args.apic_distinguished_names):
        result = {}
        for element in parsed_args.apic_distinguished_names:
            result.update(element)
        attrs['apic:distinguished_names'] = result
    return attrs


address_scope._get_attrs = _get_attrs_address_scope_extension

address_scope_sdk.AddressScope.apic_distinguished_names = resource.Body(
    'apic:distinguished_names')
address_scope_sdk.AddressScope.apic_synchronization_state = resource.Body(
    'apic:synchronization_state')


class CreateAddressScopeExtension(hooks.CommandHook):

    def get_parser(self, parser):
        parser.add_argument(
            '--apic-distinguished-names',
            metavar="<VRF=aaa>",
            dest='apic_distinguished_names',
            action=parseractions.MultiKeyValueAction,
            optional_keys=['VRF'],
            help=_("APIC distinguished names\n"
                   "Custom data to be passed as apic:distinguished_names\n"
                   "Data is passed as <key>=<value>, where "
                   "valid key is 'VRF'\n"
                   "Syntax Example: VRF=aaa ")
        )
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code


class ShowAddressScopeExtension(hooks.CommandHook):

    def get_parser(self, parser):
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code
