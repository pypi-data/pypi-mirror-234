from datetime import date

from mock import patch
from odoo.addons.component.tests.common import ComponentMixin
from odoo.tests.common import SavepointCase


class TestContractListener(SavepointCase, ComponentMixin):
    @classmethod
    def setUpClass(cls):
        super(TestContractListener, cls).setUpClass()
        cls.setUpComponent()

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        SavepointCase.setUp(self)
        ComponentMixin.setUp(self)

        self.mobile_contract_service_info = self.env[
            "mobile.service.contract.info"
        ].create({"phone_number": "654321123", "icc": "123"})

        self.partner = self.browse_ref("base.partner_demo")
        self.service_partner = self.env["res.partner"].create(
            {
                "parent_id": self.partner.id,
                "name": "Partner service OK",
                "type": "service",
            }
        )
        self.contract_data = {
            "name": "Test Contract Mobile",
            "partner_id": self.partner.id,
            "service_partner_id": self.service_partner.id,
            "invoice_partner_id": self.partner.id,
            "service_technology_id": self.ref("somconnexio.service_technology_mobile"),
            "service_supplier_id": self.ref("somconnexio.service_supplier_masmovil"),
            "mobile_contract_service_info_id": (self.mobile_contract_service_info.id),
            "bank_id": self.partner.bank_ids.id,
        }
        group_can_terminate_contract = self.env.ref("contract.can_terminate_contract")
        group_can_terminate_contract.users |= self.env.user

    def _create_ba_contract(self):
        vodafone_fiber_contract_service_info = self.env[
            "vodafone.fiber.service.contract.info"
        ].create(
            {
                "phone_number": "999990999",
                "vodafone_id": "123",
                "vodafone_offer_code": "456",
            }
        )
        self.ba_contract = self.env["contract.contract"].create(
            {
                "name": "Test Contract Broadband",
                "partner_id": self.partner.id,
                "service_partner_id": self.service_partner.id,
                "invoice_partner_id": self.partner.id,
                "service_technology_id": self.ref(
                    "somconnexio.service_technology_fiber"
                ),
                "service_supplier_id": self.ref(
                    "somconnexio.service_supplier_vodafone"
                ),
                "vodafone_fiber_service_contract_info_id": (
                    vodafone_fiber_contract_service_info.id
                ),
                "bank_id": self.partner.bank_ids.id,
            }
        )

    def test_create(self):
        contract = self.env["contract.contract"].create(self.contract_data)

        jobs_domain = [
            ("method_name", "=", "create_subscription"),
            ("model_name", "=", "contract.contract"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))
        self.assertEquals(queued_jobs.args, [contract.id])

    def test_terminate(self):
        contract = self.env["contract.contract"].create(self.contract_data)
        contract.date_end = date.today()

        contract.terminate_contract(
            self.browse_ref("somconnexio.reason_other"),
            "Comment",
            date.today(),
            self.browse_ref("somconnexio.user_reason_other"),
        )

        jobs_domain = [
            ("method_name", "=", "terminate_subscription"),
            ("model_name", "=", "contract.contract"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))
        self.assertEquals(queued_jobs.args, [contract.id])

    @patch("odoo.addons.somconnexio.models.contract.ChangeTariffTicket")
    def test_terminate_pack(self, _):
        self._create_ba_contract()
        contract = self.env["contract.contract"].create(self.contract_data)
        contract.parent_pack_contract_id = self.ba_contract.id
        self.ba_contract.date_end = date.today()

        self.ba_contract.terminate_contract(
            self.browse_ref("somconnexio.reason_other"),
            "Comment",
            date.today(),
            self.browse_ref("somconnexio.user_reason_other"),
        )

        jobs_domain = [
            ("method_name", "=", "terminate_subscription"),
            ("model_name", "=", "contract.contract"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))
        self.assertEquals(queued_jobs.args, [self.ba_contract.id])
        # Call to breack_pack
        self.assertFalse(contract.is_pack)
        self.assertFalse(contract.parent_pack_contract_id)

    def test_terminate_pack_address_change(self):
        self._create_ba_contract()
        contract = self.env["contract.contract"].create(self.contract_data)
        contract.parent_pack_contract_id = self.ba_contract.id
        self.ba_contract.date_end = date.today()

        self.ba_contract.terminate_contract(
            self.browse_ref("somconnexio.reason_location_change_from_SC_to_SC"),
            "Location change",
            date.today(),
            self.browse_ref("somconnexio.user_reason_other"),
        )

        jobs_domain = [
            ("method_name", "=", "terminate_subscription"),
            ("model_name", "=", "contract.contract"),
        ]
        queued_jobs = self.env["queue.job"].search(jobs_domain)

        self.assertEquals(1, len(queued_jobs))
        self.assertEquals(queued_jobs.args, [self.ba_contract.id])
        # Not call to breack_pack
        self.assertTrue(contract.is_pack)
        self.assertEqual(contract.parent_pack_contract_id, self.ba_contract)
