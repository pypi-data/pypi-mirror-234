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
Port extension implementations
"""

from cliff import hooks
from osc_lib.cli import parseractions

from openstack.network.v2 import port as port_sdk
from openstack import resource

from openstackclient.i18n import _
from openstackclient.network.v2 import port


_get_attrs_port_new = port._get_attrs


def _convert_erspan_config(parsed_args):
    ops = []
    for opt in parsed_args.apic_erspan_config:
        addr = {}
        addr['dest_ip'] = opt['dest-ip']
        addr['flow_id'] = opt['flow-id']
        if 'direction' in opt:
            addr['direction'] = opt['direction']
        ops.append(addr)
    return ops


def _get_attrs_port_extension(client_manager, parsed_args):
    attrs = _get_attrs_port_new(client_manager, parsed_args)
    if parsed_args.apic_erspan_config:
        attrs['apic:erspan_config'
              ] = _convert_erspan_config(parsed_args)
    if parsed_args.no_apic_erspan_config:
        attrs['apic:erspan_config'] = []
    return attrs


port._get_attrs = _get_attrs_port_extension

port_sdk.Port.apic_synchronization_state = resource.Body(
    'apic:synchronization_state')
port_sdk.Port.apic_erspan_config = resource.Body('apic:erspan_config')


class CreateAndSetPortExtension(hooks.CommandHook):

    def get_parser(self, parser):
        parser.add_argument(
            '--apic-erspan-config',
            metavar="<apic_erspan_config>",
            dest='apic_erspan_config',
            action=parseractions.MultiKeyValueAction,
            required_keys=['flow-id', 'dest-ip'],
            optional_keys=['direction'],
            help=_("APIC ERSPAN configuration\n"
                   "Custom data to be passed as apic:erspan_config\n"
                   "Data is passed as <key>=<value>, where "
                   "valid keys are 'flow-id', 'dest-ip', and 'direction'\n"
                   "Required keys: flow-id, dest-ip\n"
                   "Optional keys: direction\n"
                   "Syntax Example: dest-ip=10.0.0.0,flow-id=1 "
                   "or dest-ip=10.0.0.0,flow-id=1,direction=in ")
        )
        parser.add_argument(
            '--no-apic-erspan-config',
            dest='no_apic_erspan_config',
            action='store_true',
            help=_("No APIC ERSPAN configuration\n"
                   "Clear the apic:erspan_config configuration ")
        )
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code


class ShowPortExtension(hooks.CommandHook):

    def get_parser(self, parser):
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code
