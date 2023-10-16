from datetime import datetime, timedelta, date

from mock import Mock, patch
from odoo.exceptions import ValidationError

from ..sc_test_case import SCComponentTestCase
from ...helpers.date import date_to_str


@patch("odoo.addons.somconnexio.models.res_partner.SomOfficeUser")
@patch("odoo.addons.somconnexio.models.contract.OpenCellConfiguration")
@patch("odoo.addons.somconnexio.models.contract.SubscriptionService")
@patch("odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractCreateService")  # noqa
@patch("odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractUpdateService")  # noqa
class TestContract(SCComponentTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Contract = self.env['contract.contract']
        self.product_1 = self.env.ref('product.product_product_1')
        self.router_product = self.env['product.product'].search(
            [
                ("default_code", "=", "NCDS224WTV"),
            ]
        )
        self.router_lot = self.env['stock.production.lot'].create({
            'product_id': self.router_product.id,
            'name': '123',
            'router_mac_address': '12:BB:CC:DD:EE:90'
        })
        self.mobile_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654987654',
            'icc': '123'
        })
        self.adsl_contract_service_info = self.env[
            'adsl.service.contract.info'
        ].create({
            'phone_number': '654987654',
            'administrative_number': '123',
            'router_product_id': self.router_product.id,
            'router_lot_id': self.router_lot.id,
            'ppp_user': 'ringo',
            'ppp_password': 'rango',
            'endpoint_user': 'user',
            'endpoint_password': 'password'
        })
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        self.partner = self.browse_ref('somconnexio.res_partner_2_demo')
        self.service_partner = self.env['res.partner'].create({
            'parent_id': self.partner.id,
            'name': 'Service partner',
            'type': 'service'
        })

    def test_service_contact_wrong_type(self, *args):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner not service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            ),
            "service_supplier_id": self.ref(
                "somconnexio.service_supplier_jazztel"
            ),
            'adsl_service_contract_info_id': (
                self.adsl_contract_service_info.id
            ),
        }
        self.assertRaises(
            ValidationError,
            self.Contract.create,
            (vals_contract,)
        )

    def test_service_contact_right_type(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        self.assertTrue(self.Contract.create(vals_contract))

    def test_contact_without_code(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        contract_code = self.browse_ref(
            'somconnexio.sequence_contract'
        ).number_next_actual
        contract = self.Contract.create(vals_contract)
        self.assertEquals(contract.code, str(contract_code))

    def test_contact_with_empty_code_manual_UI_creation(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': False,
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        contract_code = self.browse_ref(
            'somconnexio.sequence_contract'
        ).number_next_actual
        contract = self.Contract.create(vals_contract)
        self.assertEquals(contract.code, str(contract_code))

    def test_contact_with_code(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': 1234,
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        contract = self.Contract.create(vals_contract)
        self.assertEquals(contract.code, '1234')

    def test_service_contact_wrong_parent(self, *args):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': self.ref('somconnexio.res_partner_1_demo'),
            'name': 'Partner wrong parent',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            ),
            'adsl_service_contract_info_id': (
                self.adsl_contract_service_info.id
            ),
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_jazztel'
            ),
        }
        self.assertRaises(
            ValidationError,
            self.Contract.create,
            (vals_contract,)
        )

    def test_service_contact_wrong_parent_not_broadband(self, *args):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': self.ref('somconnexio.res_partner_1_demo'),
            'name': 'Partner wrong parent',
            'type': 'service'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
        }
        self.assertTrue(self.Contract.create(vals_contract))

    def test_service_contact_wrong_type_not_broadband(self, *args):
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner not service'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
        }
        self.assertTrue(self.Contract.create(vals_contract))

    def test_email_not_partner_not_child_wrong_type(self, *args):
        partner_id = self.partner.id
        wrong_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'email_ids': [(6, 0, [wrong_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.Contract.create,
            (vals_contract,)
        )

    def test_email_not_partner_not_child_right_type(self, *args):
        partner_id = self.partner.id
        wrong_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com',
            'type': 'contract-email',
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'email_ids': [(6, 0, [wrong_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.Contract.create,
            (vals_contract,)
        )

    def test_email_same_partner_not_contract_email_type(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'email_ids': [(6, 0, [partner_id])]
        }
        self.assertTrue(self.Contract.create(vals_contract))

    def test_email_child_partner_wrong_type(self, *args):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Bad email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'delivery'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        self.assertRaises(
            ValidationError,
            self.Contract.create,
            (vals_contract,)
        )

    def test_email_child_partner_right_type(self, *args):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Right email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'contract-email'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        self.assertTrue(self.Contract.create(vals_contract))

    def test_contact_create_call_opencell_integration(
            self,
            _,
            CRMAccountHierarchyFromContractCreateServiceMock,
            __,
            OpenCellConfigurationMock,
            ___):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        CRMAccountHierarchyFromContractCreateServiceMock.return_value = Mock(spec=["run"])  # noqa
        OpenCellConfigurationMock.return_value = object

        contract = self.Contract.create(vals_contract)

        CRMAccountHierarchyFromContractCreateServiceMock.assert_called_once_with(
            contract,
            OpenCellConfigurationMock.return_value
        )
        CRMAccountHierarchyFromContractCreateServiceMock.return_value.run.assert_called_once_with(  # noqa
            force=False)

    def test_sequence_in_creation(self, *args):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Right email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'contract-email'
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        contract_code = self.browse_ref(
            'somconnexio.sequence_contract'
        ).number_next_actual
        contract = self.Contract.create(vals_contract)
        self.assertEquals(contract.code, str(contract_code))

    def test_code_in_creation(self, *args):
        partner_id = self.partner.id
        child_email = self.env['res.partner'].create({
            'name': 'Right email',
            'email': 'hello@example.com',
            'parent_id': partner_id,
            'type': 'contract-email'
        })
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            'email_ids': [(6, 0, [child_email.id])]
        }
        contract = self.Contract.create(vals_contract)
        self.assertEquals(contract.code, '1234')

    def test_set_previous_id_vodafone(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Vodafone Fiber',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_fiber"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_vodafone"),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        contract = self.Contract.create(vals_contract)
        contract.previous_id = 'vf123'
        self.assertEquals(
            self.vodafone_fiber_contract_service_info.previous_id,
            'vf123'
        )

    def test_set_vodafone_id_in_submodel(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Vodafone Fiber',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_fiber"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_vodafone"),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        contract = self.Contract.create(vals_contract)
        self.vodafone_fiber_contract_service_info.vodafone_id = 'vf123'
        self.assertEquals(
            contract.vodafone_id,
            'vf123'
        )

    def test_set_vodafone_offer_code_in_submodel(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Vodafone Fiber',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_fiber"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_vodafone"),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        contract = self.Contract.create(vals_contract)
        self.vodafone_fiber_contract_service_info.vodafone_offer_code = 'vf123'
        self.assertEquals(
            contract.vodafone_offer_code,
            'vf123'
        )

    def test_set_previous_id_and_name_and_icc_router_4G(self, *args):
        partner_id = self.partner.id
        router_4g_service_contract_info = self.env[
            'router.4g.service.contract.info'
        ].create({
            'vodafone_id': 'VD123',
            'vodafone_offer_code': '456',
            'icc': '2222'
        })
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Vodafone Fiber',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_4G"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_vodafone"),
            'router_4G_service_contract_info_id': (
                router_4g_service_contract_info.id
            ),
        }
        contract = self.Contract.create(vals_contract)

        self.assertFalse(contract.previous_id)
        self.assertEquals(contract.icc, '2222')
        contract.previous_id = 'vf123'
        contract.icc = '333'
        self.assertEquals(
            router_4g_service_contract_info.previous_id,
            'vf123'
        )
        self.assertEquals(
            router_4g_service_contract_info.icc,
            '333'
        )
        self.assertEquals(contract.name, '-')

    def test_set_previous_id_masmovil(self, *args):
        partner_id = self.partner.id
        masmovil_fiber_contract_service_info = self.env[
            'mm.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'mm_id': '123',
        })
        vals_contract = {
            'code': '1234',
            'name': 'Test Contract Mas Movil Fiber',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'service_technology_id': self.ref("somconnexio.service_technology_fiber"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mm_fiber_service_contract_info_id': (
                masmovil_fiber_contract_service_info.id
            ),
        }
        contract = self.Contract.create(vals_contract)
        contract.previous_id = 'mm123'
        self.assertEquals(masmovil_fiber_contract_service_info.previous_id, 'mm123')

    def test_set_previous_id_adsl(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_adsl"
            ),
            'adsl_service_contract_info_id': (
                self.adsl_contract_service_info.id
            ),
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_jazztel'
            ),
        }
        contract = self.Contract.create(vals_contract)
        contract.previous_id = 'adsl123'
        self.assertEquals(self.adsl_contract_service_info.previous_id, 'adsl123')

    def test_set_previous_id_xoln(self, *args):
        partner_id = self.partner.id
        xoln_fiber_service_contract_info = self.env[
            'xoln.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'external_id': '123',
            'project': 'laBorda',
            'id_order': '456',
            'router_product_id': self.router_product.id,
            'router_lot_id': self.router_lot.id,
        })
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'xoln_fiber_service_contract_info_id': (
                xoln_fiber_service_contract_info.id
            ),
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_xoln'
            ),
        }
        contract = self.Contract.create(vals_contract)
        contract.previous_id = 'xoln123'
        self.assertEquals(xoln_fiber_service_contract_info.previous_id, 'xoln123')

    def test_set_icc_mobile(self, *args):
        partner_id = self.partner.id
        mobile_service_contract_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'icc': '123',
        })
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_mobile"
            ),
            'mobile_contract_service_info_id': (
                mobile_service_contract_info.id
            ),
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_masmovil'
            )
        }
        contract = self.Contract.create(vals_contract)
        self.assertEquals(contract.icc, '123')
        contract.icc = '333'
        self.assertEquals(mobile_service_contract_info.icc, '333')

    def adsl_contract_service_info_wo_phone_number(self, *args):
        adsl_contract_service_info = self.env[
            'adsl.service.contract.info'
        ].create({
            'administrative_number': '123',
            'router_product_id': self.router_product.id,
            'router_lot_id': self.router_lot.id,
            'ppp_user': 'ringo',
            'ppp_password': 'rango',
            'endpoint_user': 'user',
            'endpoint_password': 'password'
        })
        self.assertEqual(adsl_contract_service_info.phone_number, '-')

    def test_children_pack_contract_ids(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        parent_contract = self.Contract.create(vals_contract)
        vals_contract['parent_pack_contract_id'] = parent_contract.id
        contract = self.Contract.create(vals_contract)
        self.assertEquals(contract.parent_pack_contract_id, parent_contract)
        self.assertEquals(parent_contract.children_pack_contract_ids, contract)
        self.assertEquals(parent_contract.number_contracts_in_pack, 2)
        self.assertTrue(contract.is_pack)
        self.assertTrue(parent_contract.is_pack)

    def test_sharing_bond_contract_ids(self, *args):
        partner_id = self.partner.id
        shared_bond_id = 'ABCDEFGHI'

        ba_vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        fiber_contract = self.Contract.create(ba_vals_contract)

        msci = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'shared_bond_id': shared_bond_id,
            'icc': '28282'
        })
        mbl_vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_mobile"
            ),
            'mobile_contract_service_info_id': msci.id,
            'service_supplier_id': self.ref(
                'somconnexio.service_supplier_masmovil'
            ),
            'parent_pack_contract_id': fiber_contract.id
        }

        # Create mobile contract
        mbl_1_contract = self.Contract.create(mbl_vals_contract)

        self.assertEquals(fiber_contract.children_pack_contract_ids, mbl_1_contract)
        self.assertEquals(fiber_contract.number_contracts_in_pack, 2)

        # Create second mobile contract sharing data with the first one
        mbl_vals_contract['mobile_contract_service_info_id'] = msci.copy().id
        mbl_2_contract = self.Contract.create(mbl_vals_contract)

        self.assertTrue(mbl_2_contract.sharing_bond_contract_ids)
        self.assertEquals(
            set(mbl_2_contract.sharing_bond_contract_ids.ids),
            set([mbl_1_contract.id, mbl_2_contract.id])
        )
        self.assertEquals(
            set(fiber_contract.children_pack_contract_ids.ids),
            set([mbl_1_contract.id, mbl_2_contract.id])
        )
        self.assertEquals(fiber_contract.number_contracts_in_pack, 3)

        # Create third mobile contract sharing data with the other two
        mbl_vals_contract['mobile_contract_service_info_id'] = msci.copy().id
        mbl_3_contract = self.Contract.create(mbl_vals_contract)

        self.assertTrue(mbl_3_contract.sharing_bond_contract_ids)
        self.assertEquals(len(mbl_3_contract.sharing_bond_contract_ids), 3)
        self.assertEquals(
            set(mbl_3_contract.sharing_bond_contract_ids.ids),
            set([mbl_1_contract.id, mbl_2_contract.id, mbl_3_contract.id])
        )
        self.assertEquals(
            set(fiber_contract.children_pack_contract_ids.ids),
            set([mbl_1_contract.id, mbl_2_contract.id, mbl_3_contract.id])
        )
        self.assertEquals(fiber_contract.number_contracts_in_pack, 4)

    def test_not_pack_contract_id(self, *args):
        partner_id = self.partner.id
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
        }
        contract = self.Contract.create(vals_contract)
        self.assertFalse(contract.parent_pack_contract_id)
        self.assertEquals(contract.number_contracts_in_pack, 0)
        self.assertFalse(contract.is_pack)

    @patch(
        "odoo.addons.somconnexio.wizards.contract_mobile_tariff_change.contract_mobile_tariff_change.ContractMobileTariffChangeWizard.create",  # noqa
        return_value=Mock(spec=['button_change'])
    )
    def test_break_contracts_in_pack(self, mock_change_tariff_create, *args):
        partner_id = self.partner.id
        parent_contract_product = self.env.ref("somconnexio.Fibra100Mb")
        parent_contract_line = {
            "name": parent_contract_product.name,
            "product_id": parent_contract_product.id,
            "date_start": datetime.now() - timedelta(days=12),
        }
        parent_vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': self.service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            "contract_line_ids": [(0, 0, parent_contract_line)],
        }
        parent_contract = self.env["contract.contract"].create(parent_vals_contract)
        contract_product = self.env.ref("somconnexio.TrucadesIllimitades20GBPack")
        contract_line = {
            "name": contract_product.name,
            "product_id": contract_product.id,
            "date_start": datetime.now() - timedelta(days=12),
        }
        vals_contract = {
            'name': 'Test Contract Mobile',
            'partner_id': partner_id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref("somconnexio.service_technology_mobile"),
            'service_supplier_id': self.ref("somconnexio.service_supplier_masmovil"),
            'mobile_contract_service_info_id': self.mobile_contract_service_info.id,
            "contract_line_ids": [(0, 0, contract_line)],
            "email_ids": [(6, 0, [self.partner.id])],
        }
        contract = self.env["contract.contract"].create(vals_contract)
        contract.parent_pack_contract_id = parent_contract.id

        self.assertTrue(parent_contract.is_pack)
        self.assertTrue(contract.is_pack)

        parent_contract.terminate_date = date.today() - timedelta(days=2)
        parent_contract.break_packs()

        self.assertFalse(parent_contract.is_pack)
        self.assertFalse(contract.is_pack)

        mock_change_tariff_create.assert_called_once_with(
            {
                "new_tariff_product_id": self.env.ref(
                    "somconnexio.TrucadesIllimitades5GB"
                ).id,
                "exceptional_change": True,
                "otrs_checked": True,
                "send_notification": False,
                "fiber_contract_to_link": False,
                "start_date": parent_contract.terminate_date,
            }
        )
        mock_change_tariff_create.return_value.button_change.assert_called_once_with()

    @patch("odoo.addons.somconnexio.wizards.contract_mobile_tariff_change.contract_mobile_tariff_change.ChangeTariffExceptionalTicket")  # noqa
    def test_break_contract_sharing_data_from_2_to_1(
            self, MockChangeTariffTicket, *args):

        contract = self.browse_ref('somconnexio.contract_mobile_il_50_shared_1_of_2')
        sharing_contract = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_2_of_2'
        )

        self.assertTrue(contract.is_pack)
        self.assertTrue(contract.shared_bond_id)

        contract.terminate_date = date.today() - timedelta(days=2)
        contract.break_packs()

        self.assertFalse(contract.is_pack)
        self.assertFalse(contract.shared_bond_id)

        pack_mobile_product = self.browse_ref("somconnexio.TrucadesIllimitades20GBPack")

        # Sharing contract automatic change
        MockChangeTariffTicket.assert_called_once_with(
            sharing_contract.partner_id.vat,
            sharing_contract.partner_id.ref,
            {
                "phone_number": sharing_contract.phone_number,
                "new_product_code": pack_mobile_product.default_code,
                "current_product_code": (
                    sharing_contract.current_tariff_product.default_code
                ),
                "effective_date": date_to_str(contract.terminate_date),
                "subscription_email": sharing_contract.email_ids[0].email,
                "language": sharing_contract.partner_id.lang,
                "fiber_linked": sharing_contract.parent_pack_contract_id.code,
                "send_notification": False,
            }
        )
        MockChangeTariffTicket.return_value.create.assert_called_once()

    def test_break_contract_sharing_data_from_3_to_2(
            self, mock_change_tariff_create, *args):
        contract = self.browse_ref('somconnexio.contract_mobile_il_50_shared_1_of_3')
        sharing_contract_1 = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_2_of_3'
        )
        sharing_contract_2 = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_3_of_3'
        )

        self.assertTrue(contract.is_pack and contract.shared_bond_id)
        self.assertIn(contract, sharing_contract_1.sharing_bond_contract_ids)
        self.assertEqual(len(sharing_contract_1.sharing_bond_contract_ids), 3)
        self.assertEqual(
            sharing_contract_1.current_tariff_product,
            self.browse_ref('somconnexio.50GBCompartides3mobils')
        )
        self.assertEqual(
            sharing_contract_1.sharing_bond_contract_ids,
            sharing_contract_2.sharing_bond_contract_ids
        )
        self.assertEqual(
            sharing_contract_1.current_tariff_product,
            sharing_contract_2.current_tariff_product,
        )

        contract.terminate_date = date.today() - timedelta(days=2)
        contract.break_packs()

        self.assertFalse(contract.is_pack and contract.shared_bond_id)
        self.assertNotIn(contract, sharing_contract_1.sharing_bond_contract_ids)
        self.assertEqual(len(sharing_contract_1.sharing_bond_contract_ids), 2)
        self.assertEqual(
            sharing_contract_1.current_tariff_product,
            self.browse_ref('somconnexio.50GBCompartides2mobils')
        )
        self.assertEqual(
            sharing_contract_1.current_tariff_start_date,
            contract.terminate_date
        )
        self.assertEqual(
            sharing_contract_1.sharing_bond_contract_ids,
            sharing_contract_2.sharing_bond_contract_ids
        )
        self.assertEqual(
            sharing_contract_1.current_tariff_product,
            sharing_contract_2.current_tariff_product,
        )

    def test_display_name_broadband_contracts(self, *args):
        contract = self.browse_ref("somconnexio.contract_fibra_600")

        expected_name = "{} - {}, {}, {}, {}".format(
            contract.name,
            contract.service_partner_id.full_street,
            contract.service_partner_id.city,
            contract.service_partner_id.zip,
            contract.service_partner_id.state_id.name,
        )
        self.assertEqual(contract.display_name, expected_name)
