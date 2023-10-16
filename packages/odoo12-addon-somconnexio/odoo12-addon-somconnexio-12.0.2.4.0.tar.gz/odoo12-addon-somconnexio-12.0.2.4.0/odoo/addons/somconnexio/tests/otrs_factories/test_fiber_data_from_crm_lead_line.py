from mock import patch
from otrs_somconnexio.otrs_models.coverage.adsl import ADSLCoverage
from otrs_somconnexio.otrs_models.coverage.mm_fibre import MMFibreCoverage
from otrs_somconnexio.otrs_models.coverage.orange_fibre import OrangeFibreCoverage
from otrs_somconnexio.otrs_models.coverage.vdf_fibre import VdfFibreCoverage

from ...otrs_factories.fiber_data_from_crm_lead_line import FiberDataFromCRMLeadLine
from ..helpers import crm_lead_create
from ..sc_test_case import SCTestCase


class FiberDataFromCRMLeadLineTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner_id = self.browse_ref("somconnexio.res_partner_2_demo")

    def test_build(self):
        ba_crm_lead = crm_lead_create(self.env, self.partner_id, "fiber")
        crm_lead_line = ba_crm_lead.lead_line_ids[0]
        broadband_isp_info = crm_lead_line.broadband_isp_info

        fiber_data = FiberDataFromCRMLeadLine(crm_lead_line).build()

        self.assertEqual(fiber_data.order_id, crm_lead_line.id)
        self.assertEqual(fiber_data.technology, "Fibra")
        self.assertEqual(fiber_data.phone_number, broadband_isp_info.phone_number)
        self.assertEqual(
            fiber_data.service_address, broadband_isp_info.service_full_street
        )
        self.assertEqual(fiber_data.service_city, broadband_isp_info.service_city)
        self.assertEqual(fiber_data.service_zip, broadband_isp_info.service_zip_code)
        self.assertEqual(
            fiber_data.service_subdivision, broadband_isp_info.service_state_id.name
        )
        self.assertEqual(fiber_data.service_subdivision_code, "B")
        self.assertEqual(
            fiber_data.shipment_address, broadband_isp_info.delivery_full_street
        )
        self.assertEqual(fiber_data.shipment_city, broadband_isp_info.delivery_city)
        self.assertEqual(fiber_data.shipment_zip, broadband_isp_info.delivery_zip_code)
        self.assertEqual(
            fiber_data.shipment_subdivision, broadband_isp_info.delivery_state_id.name
        )
        self.assertEqual(fiber_data.notes, crm_lead_line.lead_id.description)
        self.assertEqual(fiber_data.iban, crm_lead_line.lead_id.iban)
        self.assertEqual(fiber_data.email, crm_lead_line.lead_id.email_from)
        self.assertEqual(fiber_data.product, crm_lead_line.product_id.default_code)
        self.assertFalse(fiber_data.all_grouped_SIMS_recieved)
        self.assertFalse(fiber_data.has_grouped_mobile_with_previous_owner)
        self.assertEqual(fiber_data.product_ba_mm, "fibra_100")

    def test_portability_build(self):
        ba_crm_lead = crm_lead_create(
            self.env, self.partner_id, "fiber", portability=True
        )
        crm_lead_line = ba_crm_lead.lead_line_ids[0]
        broadband_isp_info = crm_lead_line.broadband_isp_info
        broadband_isp_info.write({"previous_service": "fiber"})

        fiber_data = FiberDataFromCRMLeadLine(crm_lead_line).build()

        self.assertEqual(fiber_data.phone_number, broadband_isp_info.phone_number)
        self.assertEqual(
            fiber_data.previous_owner_vat, broadband_isp_info.previous_owner_vat_number
        )
        self.assertEqual(
            fiber_data.previous_owner_name, broadband_isp_info.previous_owner_first_name
        )
        self.assertEqual(
            fiber_data.previous_owner_surname, broadband_isp_info.previous_owner_name
        )
        self.assertEqual(
            fiber_data.previous_provider, broadband_isp_info.previous_provider.code
        )
        self.assertEqual(fiber_data.previous_service, "Fibra")

    def test_check_phone_number_build(self):
        ba_crm_lead = crm_lead_create(
            self.env, self.partner_id, "fiber", portability=True
        )
        crm_lead_line = ba_crm_lead.lead_line_ids[0]
        crm_lead_line.check_phone_number = True

        fiber_data = FiberDataFromCRMLeadLine(crm_lead_line).build()

        self.assertEqual(fiber_data.phone_number, "REVISAR FIX")

    def test_change_address_build(self):
        service_supplier = self.browse_ref("somconnexio.service_supplier_vodafone")
        ba_crm_lead = crm_lead_create(
            self.env, self.partner_id, "fiber", portability=True
        )
        crm_lead_line = ba_crm_lead.lead_line_ids[0]
        broadband_isp_info = crm_lead_line.broadband_isp_info
        broadband_isp_info.write(
            {
                "type": "location_change",
                "service_supplier_id": service_supplier.id,
                "mm_fiber_coverage": MMFibreCoverage.VALUES[2][0],
                "vdf_fiber_coverage": VdfFibreCoverage.VALUES[3][0],
                "orange_fiber_coverage": OrangeFibreCoverage.VALUES[1][0],
                "adsl_coverage": ADSLCoverage.VALUES[6][0],
                "previous_contract_phone": "666666666",
                "previous_contract_address": "Calle Teper",
                "previous_contract_pon": "VDF0001",
                "previous_contract_fiber_speed": self.browse_ref(
                    "somconnexio.100Mb"
                ).name,
            }
        )

        fiber_data = FiberDataFromCRMLeadLine(crm_lead_line).build()

        self.assertEqual(fiber_data.previous_internal_provider, service_supplier.ref)
        self.assertEqual(fiber_data.mm_fiber_coverage, MMFibreCoverage.VALUES[2][0])
        self.assertEqual(fiber_data.vdf_fiber_coverage, VdfFibreCoverage.VALUES[3][0])
        self.assertEqual(
            fiber_data.orange_fiber_coverage, OrangeFibreCoverage.VALUES[1][0]
        )
        self.assertEqual(fiber_data.adsl_coverage, ADSLCoverage.VALUES[6][0])
        self.assertEqual(fiber_data.previous_contract_phone, "666666666")
        self.assertEqual(fiber_data.previous_contract_address, "Calle Teper")
        self.assertEqual(fiber_data.previous_contract_pon, "VDF0001")
        self.assertEqual(fiber_data.previous_contract_fiber_speed, "100Mb")
        self.assertEqual(fiber_data.type, "location_change")

    @patch("odoo.addons.somconnexio.models.contract.OpenCellConfiguration")
    @patch("odoo.addons.somconnexio.models.contract.SubscriptionService")
    @patch(
        "odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractCreateService"  # noqa
    )
    @patch(
        "odoo.addons.somconnexio.models.contract.CRMAccountHierarchyFromContractUpdateService"  # noqa
    )
    def test_change_address_pack_build(self, *args):
        partner = self.browse_ref("somconnexio.res_partner_1_demo")
        mobile_contract_service_info = self.env["mobile.service.contract.info"].create(
            {"phone_number": "654987654", "icc": "123"}
        )
        mobile_contract = self.env["contract.contract"].create(
            {
                "name": "Test Contract Mobile",
                "partner_id": partner.id,
                "invoice_partner_id": partner.id,
                "service_technology_id": self.ref(
                    "somconnexio.service_technology_mobile"
                ),
                "service_supplier_id": self.ref(
                    "somconnexio.service_supplier_masmovil"
                ),
                "mobile_contract_service_info_id": mobile_contract_service_info.id,
                "bank_id": partner.bank_ids.id,
            }
        )
        ba_crm_lead = crm_lead_create(
            self.env, self.partner_id, "fiber", portability=True
        )
        crm_lead_line = ba_crm_lead.lead_line_ids[0]
        broadband_isp_info = crm_lead_line.broadband_isp_info
        broadband_isp_info.write(
            {
                "type": "location_change",
                "service_supplier_id": self.browse_ref(
                    "somconnexio.service_supplier_vodafone"
                ).id,
                "mobile_pack_contracts": [(6, 0, [mobile_contract.id])],
            }
        )

        fiber_data = FiberDataFromCRMLeadLine(crm_lead_line).build()

        self.assertEqual(fiber_data.mobile_pack_contracts, mobile_contract.code)
        self.assertEqual(fiber_data.type, "location_change")

    def test_grouped_mobile_params_true(self):
        pack_crm_lead = crm_lead_create(
            self.env, self.partner_id, "pack", portability=True
        )
        mbl_lead_line = pack_crm_lead.lead_line_ids.filtered(
            lambda line: line.is_mobile
        )
        mbl_lead_line.mobile_isp_info_has_sim = True
        mbl_lead_line.mobile_isp_info.update(
            {
                "previous_owner_vat_number": "1234G",
                "previous_owner_name": "Owner",
                "previous_owner_first_name": "Previous",
            }
        )
        fiber_lead_line = pack_crm_lead.lead_line_ids.filtered(
            lambda line: not line.is_mobile
        )

        fiber_data = FiberDataFromCRMLeadLine(fiber_lead_line).build()

        self.assertTrue(mbl_lead_line.mobile_isp_info.has_sim)
        self.assertTrue(fiber_data.all_grouped_SIMS_recieved)
        self.assertTrue(fiber_data.has_grouped_mobile_with_previous_owner)

    def test_grouped_mobile_params_false(self):
        pack_crm_lead = crm_lead_create(
            self.env, self.partner_id, "pack", portability=True
        )
        mbl_lead_line = pack_crm_lead.lead_line_ids.filtered(
            lambda line: line.is_mobile
        )
        mbl_lead_line.mobile_isp_info.update(
            {
                "previous_owner_vat_number": False,
                "previous_owner_name": False,
                "previous_owner_first_name": False,
            }
        )

        fiber_lead_line = pack_crm_lead.lead_line_ids.filtered(
            lambda line: not line.is_mobile
        )

        fiber_data = FiberDataFromCRMLeadLine(fiber_lead_line).build()

        self.assertFalse(fiber_data.all_grouped_SIMS_recieved)
        self.assertFalse(fiber_data.has_grouped_mobile_with_previous_owner)

    def test_fiber_product_ba_mm_with_mobile_pack(self):
        pack_crm_lead = crm_lead_create(
            self.env, self.partner_id, "pack", portability=True
        )
        fiber_lead_line = pack_crm_lead.lead_line_ids.filtered(
            lambda line: not line.is_mobile
        )

        fiber_data = FiberDataFromCRMLeadLine(fiber_lead_line).build()

        self.assertEqual(fiber_data.product_ba_mm, "fibra_100_pack")

    def test_fiber_product_ba_mm_with_shared_data_mobile(self):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "shared_data", portability=True
        )
        fiber_lead_line = crm_lead.lead_line_ids.filtered(
            lambda line: not line.is_mobile
        )

        fiber_data = FiberDataFromCRMLeadLine(fiber_lead_line).build()

        self.assertEqual(fiber_data.product_ba_mm, "fibra_100_shared")
