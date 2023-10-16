from mock import patch

from ..sc_test_case import SCTestCase
from ...services.contract_contract_process import ContractContractProcess


class TestContractProcess(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.env = {}

    @patch('odoo.addons.somconnexio.services.contract_contract_process.MobileContractProcess')  # noqa
    def test_create_mobile_contract(self, MobileContractProcessMock):
        expected_contract = object
        MobileContractProcessMock.return_value.create.return_value = expected_contract
        data = {
            "service_technology": 'Mobile',
        }
        contract = ContractContractProcess(self.env).create(**data)

        self.assertEquals(
            contract,
            expected_contract
        )
        MobileContractProcessMock.assert_called_once_with(self.env)
        MobileContractProcessMock.return_value.create.assert_called_once_with(**data)

    @patch('odoo.addons.somconnexio.services.contract_contract_process.ADSLContractProcess')  # noqa
    def test_create_adsl_contract(self, ADSLContractProcessMock):
        expected_contract = object
        ADSLContractProcessMock.return_value.create.return_value = expected_contract
        data = {
            "service_technology": 'ADSL',
        }
        contract = ContractContractProcess(self.env).create(**data)

        self.assertEquals(
            contract,
            expected_contract
        )
        ADSLContractProcessMock.assert_called_once_with(self.env)
        ADSLContractProcessMock.return_value.create.assert_called_once_with(**data)

    @patch('odoo.addons.somconnexio.services.contract_contract_process.FiberContractProcess')  # noqa
    def test_create_fiber_contract(self, FiberContractProcessMock):
        expected_contract = object
        FiberContractProcessMock.return_value.create.return_value = expected_contract
        data = {
            "service_technology": 'Fiber',
        }
        contract = ContractContractProcess(self.env).create(**data)

        self.assertEquals(
            contract,
            expected_contract
        )
        FiberContractProcessMock.assert_called_once_with(self.env)
        FiberContractProcessMock.return_value.create.assert_called_once_with(**data)

    @patch('odoo.addons.somconnexio.services.contract_contract_process.Router4GContractProcess')  # noqa
    def test_create_router4g_contract(self, Router4GContractProcessMock):
        expected_contract = object
        Router4GContractProcessMock.return_value.create.return_value = expected_contract
        data = {
            "service_technology": '4G',
        }
        contract = ContractContractProcess(self.env).create(**data)

        self.assertEquals(
            contract,
            expected_contract
        )
        Router4GContractProcessMock.assert_called_once_with(self.env)
        Router4GContractProcessMock.return_value.create.assert_called_once_with(**data)
