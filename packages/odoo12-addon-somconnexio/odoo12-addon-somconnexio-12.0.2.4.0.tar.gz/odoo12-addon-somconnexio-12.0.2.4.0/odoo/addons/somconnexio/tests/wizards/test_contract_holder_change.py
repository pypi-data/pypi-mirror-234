from datetime import date, timedelta

from mock import patch
from odoo.exceptions import MissingError

from ..sc_test_case import SCTestCase


class TestContractHolderChangeWizard(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.vodafone_fiber_contract_service_info = self.env[
            "vodafone.fiber.service.contract.info"
        ].create(
            {
                "phone_number": "654321123",
                "vodafone_id": "123",
                "vodafone_offer_code": "456",
            }
        )
        self.partner = self.browse_ref("base.partner_demo")
        self.partner.write({"ref": "987654321"})
        partner_id = self.partner.id
        self.service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner service OK',
            'type': 'service',
            'street': 'New test street'
        })
        contract_line = {
            "name": "Hola",
            "product_id": self.browse_ref('somconnexio.Fibra600Mb').id,
            "date_start": '2020-01-01'
        }
        vals_contract = {
            "name": "Test Contract Broadband",
            "partner_id": partner_id,
            "service_partner_id": self.service_partner.id,
            "invoice_partner_id": partner_id,
            "service_technology_id": self.ref("somconnexio.service_technology_fiber"),
            "service_supplier_id": self.ref("somconnexio.service_supplier_vodafone"),
            "vodafone_fiber_service_contract_info_id": (
                self.vodafone_fiber_contract_service_info.id
            ),
            "bank_id": self.partner.bank_ids.id,
            "contract_line_ids": [(0, 0, contract_line)],
            "code": "10001",
        }
        self.ba_contract = self.env["contract.contract"].create(vals_contract)
        contract_line = {
            "name": "Hola",
            "product_id": self.browse_ref("somconnexio.200Min2GB").id,
            "date_start": "2020-01-01",
        }
        mobile_contract_service_info = self.env["mobile.service.contract.info"].create(
            {"phone_number": "654987654", "icc": "123"}
        )
        vals_contract = {
            "name": "Test Contract Mobile",
            "partner_id": self.partner.id,
            "service_partner_id": self.service_partner.id,
            "invoice_partner_id": self.partner.id,
            "service_technology_id": self.ref("somconnexio.service_technology_mobile"),
            "service_supplier_id": self.ref("somconnexio.service_supplier_masmovil"),
            "mobile_contract_service_info_id": mobile_contract_service_info.id,
            "bank_id": self.partner.bank_ids.id,
            "contract_line_ids": [(0, 0, contract_line)],
            "code": "10002",
        }

        self.mobile_contract = self.env["contract.contract"].create(vals_contract)

        self.partner_b = self.browse_ref("somconnexio.res_partner_2_demo")
        self.partner_b_bank = self.browse_ref("somconnexio.demo_bank_id")
        self.banking_mandate = self.browse_ref(
            "somconnexio.demo_mandate_partner_2_demo"
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
    )
    def test_wizard_holder_change_ok(self, mock_get_fiber_contracts_to_pack):
        # No bonified mobile product available
        mock_get_fiber_contracts_to_pack.side_effect = MissingError("")

        group_can_terminate_contract = self.env.ref("contract.can_terminate_contract")
        group_can_terminate_contract.users |= self.env.user

        wizard = (
            self.env["contract.holder.change.wizard"]
            .with_context(active_id=self.ba_contract.id)
            .create(
                {
                    "change_date": date.today(),
                    "partner_id": self.partner_b.id,
                    "banking_mandate_id": self.banking_mandate.id,
                }
            )
        )
        product_templates = self.env["product.template"].search(
            [
                ("categ_id", "=", self.browse_ref("somconnexio.broadband_fiber_service").id),  # noqa
            ]
        )
        available_fiber_products = self.env['product.product'].search(
            [
                ("product_tmpl_id", "in", product_templates.ids),
                ("public", "=", "True"),
            ]
        )
        self.assertEqual(
            wizard.available_products,
            available_fiber_products,
        )
        self.assertEqual(
            wizard.payment_mode,
            self.browse_ref("somconnexio.payment_mode_inbound_sepa"),
        )
        self.assertEqual(
            wizard.available_banking_mandates,
            self.env["account.banking.mandate"].browse(self.banking_mandate.id),
        )
        new_service_partner_b = self.env["res.partner"].search(
            [
                ("parent_id", "=", self.partner_b.id),
                ("type", "=", "service"),
                ("street", "=", self.service_partner.street),
            ]
        )
        self.assertFalse(new_service_partner_b)

        wizard.button_change()

        self.assertEqual(
            self.ba_contract.terminate_reason_id,
            self.browse_ref("somconnexio.reason_holder_change"),
        )
        self.assertEqual(
            self.ba_contract.terminate_user_reason_id,
            self.browse_ref("somconnexio.user_reason_other"),
        )
        self.assertTrue(self.ba_contract.is_terminated)

        new_contract = self.env["contract.contract"].search(
            [("partner_id", "=", self.partner_b.id)]
        )

        self.assertEqual(
            self.ba_contract.service_supplier_id, new_contract.service_supplier_id
        )
        self.assertEqual(
            self.ba_contract.service_technology_id, new_contract.service_technology_id
        )
        self.assertNotEqual(
            self.ba_contract.vodafone_fiber_service_contract_info_id,
            new_contract.vodafone_fiber_service_contract_info_id,
        )
        self.assertEqual(self.ba_contract.contract_line_ids[0].date_end, date.today())
        self.assertEqual(
            new_contract.contract_line_ids[0].date_start,
            date.today() + timedelta(days=1)
        )
        self.assertEqual(new_contract.mandate_id, self.banking_mandate)

        new_service_partner_b = self.env["res.partner"].search(
            [
                ("parent_id", "=", self.partner_b.id),
                ("type", "=", "service"),
                ("street", "=", self.service_partner.street),
            ]
        )
        self.assertTrue(new_service_partner_b)
        self.assertEqual(new_contract.service_partner_id.id, new_service_partner_b.id)
        self.assertEquals(
            new_contract.crm_lead_line_id.lead_id.name, "Change Holder process"
        )
        self.assertEquals(
            new_contract.crm_lead_line_id.lead_id.partner_id, self.partner_b
        )
        self.assertEquals(
            new_contract.crm_lead_line_id.lead_id.stage_id,
            self.env.ref("crm.stage_lead4"),
        )
        self.assertEqual(new_contract.create_reason, "holder_change")

    @patch(
        "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
    )
    def test_wizard_holder_change_ok_mobile(self, mock_get_fiber_contracts_to_pack):
        # No bonified mobile product available
        mock_get_fiber_contracts_to_pack.side_effect = MissingError("")

        group_can_terminate_contract = self.env.ref("contract.can_terminate_contract")
        group_can_terminate_contract.users |= self.env.user

        other_service_partner_b = self.env["res.partner"].create(
            {
                "parent_id": self.partner_b.id,
                "name": "Partner B service OK",
                "type": "service",
                "street": "Partner b diferent street",
            }
        )
        same_street_service_partner = self.env["res.partner"].create(
            {
                "parent_id": self.partner_b.id,
                "name": "Partner B service OK",
                "type": "service",
                "street": self.service_partner.street,
            }
        )

        wizard = (
            self.env["contract.holder.change.wizard"]
            .with_context(active_id=self.mobile_contract.id)
            .create(
                {
                    "change_date": date.today(),
                    "partner_id": self.partner_b.id,
                    "banking_mandate_id": self.banking_mandate.id,
                }
            )
        )

        wizard.button_change()

        new_contract = self.env["contract.contract"].search(
            [("partner_id", "=", self.partner_b.id)]
        )

        self.assertNotEqual(
            new_contract.service_partner_id.id, other_service_partner_b.id
        )
        self.assertEqual(
            new_contract.service_partner_id.id, same_street_service_partner.id
        )
        self.assertEquals(
            new_contract.crm_lead_line_id.lead_id.name, "Change Holder process"
        )
        self.assertEquals(
            new_contract.crm_lead_line_id.lead_id.partner_id, self.partner_b
        )
        self.assertEquals(
            new_contract.crm_lead_line_id.lead_id.stage_id,
            self.env.ref("crm.stage_lead4"),
        )
        self.assertEqual(new_contract.create_reason, "holder_change")

    @patch(
        "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
    )
    def test_wizard_holder_change_service_address_already_existed(
        self, mock_get_fiber_contracts_to_pack
    ):
        # No bonified mobile product available
        mock_get_fiber_contracts_to_pack.side_effect = MissingError("")

        group_can_terminate_contract = self.env.ref("contract.can_terminate_contract")
        group_can_terminate_contract.users |= self.env.user

        wizard = (
            self.env["contract.holder.change.wizard"]
            .with_context(active_id=self.ba_contract.id)
            .create(
                {
                    "change_date": date.today(),
                    "partner_id": self.partner_b.id,
                    "banking_mandate_id": self.banking_mandate.id,
                }
            )
        )

        new_service_partner_b = self.env["res.partner"].create(
            {
                "parent_id": self.partner_b.id,
                "type": "service",
                "street": self.service_partner.street,
            }
        )

        wizard.button_change()

        new_contract = self.env["contract.contract"].search(
            [("partner_id", "=", self.partner_b.id)]
        )

        self.assertEqual(new_contract.service_partner_id.id, new_service_partner_b.id)

    @patch(
        "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
    )
    def test_wizard_holder_skip_oneshot(self, mock_get_fiber_contracts_to_pack):
        # No bonified mobile product available
        mock_get_fiber_contracts_to_pack.side_effect = MissingError("")

        group_can_terminate_contract = self.env.ref("contract.can_terminate_contract")
        group_can_terminate_contract.users |= self.env.user

        contract_line = {
            "name": "Hola",
            "product_id": self.browse_ref("somconnexio.RecollidaRouter").id,
            "date_start": "2020-01-01",
        }
        self.ba_contract.write({"contract_line_ids": [(0, 0, contract_line)]})
        wizard = (
            self.env["contract.holder.change.wizard"]
            .with_context(active_id=self.ba_contract.id)
            .create(
                {
                    "change_date": date.today(),
                    "partner_id": self.partner_b.id,
                    "banking_mandate_id": self.banking_mandate.id,
                }
            )
        )

        wizard.button_change()
        new_contract = self.env["contract.contract"].search(
            [("partner_id", "=", self.partner_b.id)]
        )
        self.assertTrue(
            self.ba_contract.contract_line_ids.filtered(
                lambda l: l.product_id == self.browse_ref("somconnexio.RecollidaRouter")
            )
        )
        self.assertTrue(new_contract.contract_line_ids)
        self.assertFalse(
            new_contract.contract_line_ids.filtered(
                lambda l: l.product_id == self.browse_ref("somconnexio.RecollidaRouter")
            )
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
    )
    def test_wizard_holder_skip_terminated_line(self, mock_get_fiber_contracts_to_pack):
        # No bonified mobile product available
        mock_get_fiber_contracts_to_pack.side_effect = MissingError("")

        group_can_terminate_contract = self.env.ref("contract.can_terminate_contract")
        group_can_terminate_contract.users |= self.env.user

        contract_line = {
            "name": "Hola",
            "product_id": self.browse_ref("somconnexio.Fibra600Mb").id,
            "date_start": "2020-01-01",
            "date_end": "2020-01-15",
        }
        self.ba_contract.write({"contract_line_ids": [(0, 0, contract_line)]})
        wizard = (
            self.env["contract.holder.change.wizard"]
            .with_context(active_id=self.ba_contract.id)
            .create(
                {
                    "change_date": date.today(),
                    "partner_id": self.partner_b.id,
                    "banking_mandate_id": self.banking_mandate.id,
                }
            )
        )

        wizard.button_change()
        new_contract = self.env["contract.contract"].search(
            [("partner_id", "=", self.partner_b.id)]
        )
        self.assertTrue(
            self.ba_contract.contract_line_ids.filtered(lambda l: l.date_end)
        )
        self.assertTrue(new_contract.contract_line_ids)
        self.assertFalse(new_contract.contract_line_ids.filtered(lambda l: l.date_end))

    @patch(
        "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
    )
    def test_wizard_holder_pack_offer_no_defaults(
        self, mock_get_fiber_contracts_to_pack
    ):
        # No bonified mobile product available
        mock_get_fiber_contracts_to_pack.side_effect = MissingError("")

        wizard = (
            self.env["contract.holder.change.wizard"]
            .with_context(active_id=self.mobile_contract.id)
            .create(
                {
                    "change_date": date.today(),
                    "partner_id": self.partner_b.id,
                    "banking_mandate_id": self.banking_mandate.id,
                }
            )
        )

        product_templates = self.env["product.template"].search(
            [
                ("categ_id", "=", self.browse_ref("somconnexio.mobile_service").id),
            ]
        )
        available_mobile_products = self.env['product.product'].search(
            [
                ("product_tmpl_id", "in", product_templates.ids),
                ("public", "=", "True"),
            ]
        )
        self.assertEqual(
            wizard.available_products,
            available_mobile_products,
        )
        self.assertFalse(
            wizard.fiber_contract_to_link,
        )
        self.assertEqual(
            wizard.has_mobile_pack_offer_text,
            "no",
        )
        # Check bonified product not available
        self.assertNotIn(
            self.browse_ref("somconnexio.TrucadesIllimitades20GBPack"),
            wizard.available_products,
        )
        self.assertEqual(
            wizard.product_id.id,
            self.mobile_contract.current_tariff_product.id,
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
    )
    def test_wizard_holder_pack_offer_yes(
        self, mock_get_fiber_contracts_to_pack
    ):
        mock_get_fiber_contracts_to_pack.return_value = [
            {
                "id": self.ba_contract.id,
                "code": self.ba_contract.code,
            }
        ]

        wizard = (
            self.env["contract.holder.change.wizard"]
            .with_context(active_id=self.mobile_contract.id)
            .create(
                {
                    "change_date": date.today(),
                    "partner_id": self.partner_b.id,
                    "banking_mandate_id": self.banking_mandate.id,
                }
            )
        )
        self.assertEqual(
            wizard.fiber_contract_to_link.code,
            self.ba_contract.code,
        )
        self.assertEqual(
            wizard.has_mobile_pack_offer_text,
            "yes",
        )
        # Check bonified product available
        self.assertIn(
            self.browse_ref("somconnexio.TrucadesIllimitades20GBPack"),
            wizard.available_products,
        )
        self.assertEqual(
            wizard.product_id.id,
            self.mobile_contract.current_tariff_product.id,
        )
        mock_get_fiber_contracts_to_pack.assert_called_once_with(
            partner_ref=self.partner_b.ref
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
    )
    def test_wizard_holder_change_ok_mobile_pack_offer_selected(
        self, mock_get_fiber_contracts_to_pack
    ):
        mock_get_fiber_contracts_to_pack.return_value = [
            {
                "id": self.ba_contract.id,
                "code": self.ba_contract.code,
            }
        ]
        offer_product = self.browse_ref("somconnexio.TrucadesIllimitades20GBPack")

        group_can_terminate_contract = self.env.ref("contract.can_terminate_contract")
        group_can_terminate_contract.users |= self.env.user

        wizard = (
            self.env["contract.holder.change.wizard"]
            .with_context(active_id=self.mobile_contract.id)
            .create(
                {
                    "change_date": date.today(),
                    "partner_id": self.partner_b.id,
                    "banking_mandate_id": self.banking_mandate.id,
                    "product_id": offer_product.id,
                }
            )
        )

        wizard.button_change()

        new_contract = self.env["contract.contract"].search(
            [("partner_id", "=", self.partner_b.id)]
        )
        new_crm_lead = new_contract.crm_lead_line_id.lead_id

        self.assertEqual(
            new_contract.parent_pack_contract_id.id,
            self.ba_contract.id,
        )
        self.assertEqual(
            new_contract.contract_line_ids[0].product_id,
            offer_product,
        )
        self.assertEqual(
            new_crm_lead.lead_line_ids[0].mobile_isp_info.linked_fiber_contract_id.id,
            self.ba_contract.id,
        )
        self.assertEqual(
            new_crm_lead.lead_line_ids[0].product_id,
            offer_product,
        )
        mock_get_fiber_contracts_to_pack.assert_called_once_with(
            partner_ref=self.partner_b.ref
        )

    @patch(
        "odoo.addons.somconnexio.services.contract_contract_service.ContractService.get_fiber_contracts_to_pack"  # noqa
    )
    def test_wizard_holder_change_ok_mobile_pack_wo_offer_selected(
        self, mock_get_fiber_contracts_to_pack
    ):
        mock_get_fiber_contracts_to_pack.return_value = [
            {
                "id": self.ba_contract.id,
                "code": self.ba_contract.code,
            }
        ]
        product = self.browse_ref("somconnexio.TrucadesIllimitades20GB")

        group_can_terminate_contract = self.env.ref("contract.can_terminate_contract")
        group_can_terminate_contract.users |= self.env.user

        wizard = (
            self.env["contract.holder.change.wizard"]
            .with_context(active_id=self.mobile_contract.id)
            .create(
                {
                    "change_date": date.today(),
                    "partner_id": self.partner_b.id,
                    "banking_mandate_id": self.banking_mandate.id,
                    "product_id": product.id,
                }
            )
        )

        wizard.button_change()

        new_contract = self.env["contract.contract"].search(
            [("partner_id", "=", self.partner_b.id)]
        )
        new_crm_lead = new_contract.crm_lead_line_id.lead_id

        self.assertFalse(
            new_contract.parent_pack_contract_id
        )
        self.assertEqual(
            new_contract.contract_line_ids[0].product_id,
            product,
        )
        self.assertFalse(
            new_crm_lead.lead_line_ids[0].mobile_isp_info.linked_fiber_contract_id
        )
        self.assertEqual(
            new_crm_lead.lead_line_ids[0].product_id,
            product,
        )
        mock_get_fiber_contracts_to_pack.assert_called_once_with(
            partner_ref=self.partner_b.ref
        )
