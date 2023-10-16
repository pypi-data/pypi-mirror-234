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
Router extension implementations
"""

from cliff import hooks
from openstack.network.v2 import router as router_sdk
from openstack import resource
from openstackclient.network.v2 import router

from openstackclient.i18n import _


_get_attrs_router_new = router._get_attrs


def _get_attrs_router_extension(client_manager, parsed_args):
    attrs = _get_attrs_router_new(client_manager, parsed_args)
    if parsed_args.apic_external_provided_contracts:
        attrs['apic:external_provided_contracts'
              ] = parsed_args.apic_external_provided_contracts.split(",")
    if parsed_args.apic_external_consumed_contracts:
        attrs['apic:external_consumed_contracts'
              ] = parsed_args.apic_external_consumed_contracts.split(",")
    return attrs


router._get_attrs = _get_attrs_router_extension

router_sdk.Router.apic_distinguished_names = resource.Body(
    'apic:distinguished_names')
router_sdk.Router.apic_synchronization_state = resource.Body(
    'apic:synchronization_state')
router_sdk.Router.apic_external_provided_contracts = resource.Body(
    'apic:external_provided_contracts')
router_sdk.Router.apic_external_consumed_contracts = resource.Body(
    'apic:external_consumed_contracts')


class CreateAndSetRouterExtension(hooks.CommandHook):

    def get_parser(self, parser):
        parser.add_argument(
            '--apic-external-provided-contracts',
            metavar="<aaa,bbb>",
            dest='apic_external_provided_contracts',
            help=_("APIC external provided contracts\n"
                   "Data is passed as comma separated strings\n"
                   "Default value is []\n"
                   "Valid values: list of unique strings\n"
                   "Syntax Example: foo or foo,bar ")
        )
        parser.add_argument(
            '--apic-external-consumed-contracts',
            metavar="<aaa,bbb>",
            dest='apic_external_consumed_contracts',
            help=_("APIC external consumed contracts\n"
                   "Data is passed as comma separated strings\n"
                   "Default value is []\n"
                   "Valid values: list of unique strings\n"
                   "Syntax Example: foo or foo,bar ")
        )
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code


class ShowRouterExtension(hooks.CommandHook):

    def get_parser(self, parser):
        return parser

    def get_epilog(self):
        return ''

    def before(self, parsed_args):
        return parsed_args

    def after(self, parsed_args, return_code):
        return return_code
