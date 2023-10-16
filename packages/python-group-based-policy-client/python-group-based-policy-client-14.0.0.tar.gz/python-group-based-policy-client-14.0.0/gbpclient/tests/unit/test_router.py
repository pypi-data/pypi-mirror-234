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

from gbpclient.gbp.v2_0 import router as router_ext
from gbpclient.tests.unit import test_cli20
from openstackclient.network.v2 import router
from openstackclient.tests.unit.network.v2 import test_router


# Tests for router create for APIC extensions
#
class TestRouterCreate(test_router.TestRouter, test_cli20.CLITestV20Base):

    def setUp(self):
        super(TestRouterCreate, self).setUp()
        self.new_router = test_router.TestCreateRouter.new_router
        self.network.create_router = mock.Mock(return_value=self.new_router)
        self.cmd = router.CreateRouter(self.app, self.namespace)

    def test_create_default_options(self):
        arglist = [
            self.new_router.name,
        ]
        verifylist = [
            ('name', self.new_router.name),
            ('apic_external_provided_contracts', None),
            ('apic_external_consumed_contracts', None),
        ]
        create_ext = router_ext.CreateAndSetRouterExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_router.assert_called_once_with(**{
            'admin_state_up': True,
            'name': self.new_router.name,
        })

    def test_create_all_options(self):
        arglist = [
            self.new_router.name,
            "--apic-external-provided-contracts", 'ptest1',
            "--apic-external-consumed-contracts", 'ctest1',
        ]
        verifylist = [
            ('name', self.new_router.name),
            ('apic_external_provided_contracts', 'ptest1'),
            ('apic_external_consumed_contracts', 'ctest1'),
        ]
        create_ext = router_ext.CreateAndSetRouterExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, create_ext)
        columns, data = self.cmd.take_action(parsed_args)

        self.network.create_router.assert_called_once_with(**{
            'admin_state_up': True,
            'name': self.new_router.name,
            'apic:external_provided_contracts': ['ptest1'],
            'apic:external_consumed_contracts': ['ctest1'],
        })


# Tests for router set for APIC extensions
#
class TestRouterSet(test_router.TestRouter, test_cli20.CLITestV20Base):

    _network = test_router.TestSetRouter._network
    _subnet = test_router.TestSetRouter._subnet
    _router = test_router.TestSetRouter._router

    def setUp(self):
        super(TestRouterSet, self).setUp()
        self.network.router_add_gateway = mock.Mock()
        self.network.update_router = mock.Mock(return_value=None)
        self.network.set_tags = mock.Mock(return_value=None)
        self.network.find_router = mock.Mock(return_value=self._router)
        self.network.find_network = mock.Mock(return_value=self._network)
        self.network.find_subnet = mock.Mock(return_value=self._subnet)
        self.cmd = router.SetRouter(self.app, self.namespace)

    def test_set_no_options(self):
        arglist = [
            self._router.name,
        ]
        verifylist = [
            ('router', self._router.name),
        ]
        set_ext = router_ext.CreateAndSetRouterExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, set_ext)
        result = self.cmd.take_action(parsed_args)

        self.assertFalse(self.network.update_router.called)
        self.assertFalse(self.network.set_tags.called)
        self.assertIsNone(result)

    def test_set_all_valid_options(self):
        arglist = [
            self._router.name,
            "--apic-external-provided-contracts", 'ptest1,ptest11',
            "--apic-external-consumed-contracts", 'ctest1,ctest11',
        ]
        verifylist = [
            ('router', self._router.name),
            ('apic_external_provided_contracts', 'ptest1,ptest11'),
            ('apic_external_consumed_contracts', 'ctest1,ctest11'),
        ]
        set_ext = router_ext.CreateAndSetRouterExtension(self.app)
        parsed_args = self.check_parser_ext(
            self.cmd, arglist, verifylist, set_ext)
        result = self.cmd.take_action(parsed_args)

        attrs = {
            'apic:external_provided_contracts': ['ptest1', 'ptest11'],
            'apic:external_consumed_contracts': ['ctest1', 'ctest11'],
        }
        self.network.update_router.assert_called_once_with(
            self._router, **attrs)
        self.assertIsNone(result)
