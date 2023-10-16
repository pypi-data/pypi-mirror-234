from datetime import date
from mock import patch
from ..sc_test_case import SCTestCase
from odoo.exceptions import ValidationError


class TestContractTariffChangeWizard(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.masmovil_mobile_contract_service_info = self.env[
            'mobile.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'icc': '123',
        })
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        self.partner = self.browse_ref('base.partner_demo')
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner service OK',
            'type': 'service'
        })
        product_ref = self.browse_ref('somconnexio.150Min2GB')
        product_ref_ba = self.browse_ref('somconnexio.Fibra100Mb')
        product = self.env["product.product"].search(
            [('default_code', '=', product_ref.default_code)]
        )
        self.product_ba = self.env["product.product"].search(
            [('default_code', '=', product_ref_ba.default_code)]
        )
        contract_line = {
            "name": product.name,
            "product_id": product.id,
            "date_start": "2020-01-01 00:00:00"
        }
        contract_line_ba = {
            "name": self.product_ba.name,
            "product_id": self.product_ba.id,
            "date_start": "2020-01-01 00:00:00"
        }
        vals_contract = {
            'name': 'Test Contract One Shot Request',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_mobile"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_masmovil"
            ),
            'mobile_contract_service_info_id': (
                self.masmovil_mobile_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id,
            'contract_line_ids': [
                (0, False, contract_line)
            ]
        }
        vals_contract_ba = {
            'name': 'Test Contract BA',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
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
            'bank_id': self.partner.bank_ids.id,
            'contract_line_ids': [
                (0, False, contract_line_ba)
            ]
        }
        self.contract = self.env['contract.contract'].create(vals_contract)
        self.contract_ba = self.env['contract.contract'].create(vals_contract_ba)
        self.user_admin = self.browse_ref('base.user_admin')
        self.new_tariff_product_id = self.browse_ref("somconnexio.150Min2GB")
        self.new_tariff_ba_same_tech_product_id = self.browse_ref(
            'somconnexio.Fibra600Mb'
        )
        self.new_tariff_ba_different_tech_product_id = self.browse_ref(
            'somconnexio.ADSL20MBSenseFix'
        )
        self.new_tariff_ba_wo_fix_product_id = self.browse_ref(
            'somconnexio.SenseFixFibra100Mb'
        )

    def test_wizard_tariff_change_ok(self):
        self.assertEqual(self.contract.current_tariff_contract_line.product_id.id,
                         self.ref('somconnexio.150Min2GB'))
        start_date = date.today()

        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=self.contract.id
        ).sudo(
            self.user_admin
        ).create({
            'start_date': start_date,
            'summary': 'Tariff change 150 min 2 GB',
        })
        wizard.new_tariff_product_id = self.new_tariff_product_id

        partner_activities_before = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)]
        )
        wizard.button_change()
        partner_activities_after = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)],
        )
        self.assertEquals(len(partner_activities_after) -
                          len(partner_activities_before), 1)
        created_activity = partner_activities_after[-1]
        self.assertEquals(created_activity.user_id, self.user_admin)
        self.assertEquals(
            created_activity.activity_type_id,
            self.browse_ref('somconnexio.mail_activity_type_tariff_change')
        )
        self.assertEquals(created_activity.done, True)
        self.assertEquals(created_activity.summary, 'Tariff change {}'.format(
            self.new_tariff_product_id.showed_name))
        self.assertTrue(self.contract.contract_line_ids[0].date_end)
        self.assertFalse(self.contract.contract_line_ids[1].date_end)
        self.assertEqual(self.contract.contract_line_ids[1].date_start,
                         start_date)
        self.assertEqual(self.contract.contract_line_ids[1].product_id.id,
                         self.new_tariff_product_id.id)

    def test_ba_tariff_change(self):
        self.assertEqual(self.contract_ba.current_tariff_contract_line.product_id.id,
                         self.ref('somconnexio.Fibra100Mb'))
        start_date = date.today()
        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=self.contract_ba.id,
        ).create({
            'start_date': start_date,
            'summary': 'Tariff change Fibra 600Mb',
        })
        wizard.new_tariff_product_id = self.new_tariff_ba_same_tech_product_id
        partner_activities_before = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)]
        )
        wizard.button_change()
        partner_activities_after = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)],
        )
        self.assertEquals(len(partner_activities_after) -
                          len(partner_activities_before), 1)
        created_activity = partner_activities_after[-1]
        self.assertEquals(
            created_activity.activity_type_id,
            self.browse_ref('somconnexio.mail_activity_type_tariff_change')
        )
        self.assertEquals(created_activity.done, True)
        self.assertEquals(created_activity.summary, 'Tariff change {}'.format(
            self.new_tariff_ba_same_tech_product_id.showed_name))
        self.assertTrue(self.contract_ba.contract_line_ids[0].date_end)
        self.assertFalse(self.contract_ba.contract_line_ids[1].date_end)
        self.assertEqual(self.contract_ba.contract_line_ids[1].date_start,
                         start_date)
        self.assertEqual(self.contract_ba.contract_line_ids[1].product_id.id,
                         self.new_tariff_ba_same_tech_product_id.id)

    def test_ba_tariff_diff_tech_change(self):
        self.assertEqual(self.contract_ba.current_tariff_contract_line.product_id.id,
                         self.ref('somconnexio.Fibra100Mb'))
        start_date = date.today()
        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=self.contract_ba.id,
            default_type='ba'
        ).create({
            'start_date': start_date,
            'summary': 'Tariff change ADSL Sense Fix',
        })
        wizard.new_tariff_product_id = self.new_tariff_ba_different_tech_product_id
        self.assertRaises(ValidationError, wizard.button_change)
        self.assertEqual(
            self.contract_ba.contract_line_ids.product_id, self.product_ba
        )

    def test_ba_tariff_wo_fix_change(self):
        self.assertEqual(self.contract_ba.current_tariff_contract_line.product_id.id,
                         self.ref('somconnexio.Fibra100Mb'))
        start_date = date.today()
        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=self.contract_ba.id,
            default_type='ba'
        ).create({
            'start_date': start_date,
            'summary': 'Tariff change Fibra 100Mb Sense Fix',
        })
        wizard.new_tariff_product_id = self.new_tariff_ba_wo_fix_product_id
        partner_activities_before = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)]
        )
        phone_number = self.contract_ba.phone_number
        wizard.button_change()
        partner_activities_after = self.env['mail.activity'].search(
            [('partner_id', '=', self.partner.id)],
        )
        self.assertEquals(len(partner_activities_after) -
                          len(partner_activities_before), 1)
        created_activity = partner_activities_after[-1]
        self.assertEquals(
            created_activity.activity_type_id,
            self.browse_ref('somconnexio.mail_activity_type_tariff_change')
        )
        self.assertEquals(created_activity.done, True)
        self.assertEquals(created_activity.summary, 'Tariff change {}'.format(
            self.new_tariff_ba_wo_fix_product_id.showed_name))
        self.assertTrue(self.contract_ba.contract_line_ids[0].date_end)
        self.assertFalse(self.contract_ba.contract_line_ids[1].date_end)
        self.assertEqual(self.contract_ba.contract_line_ids[1].date_start,
                         start_date)
        self.assertEqual(self.contract_ba.contract_line_ids[1].product_id.id,
                         self.new_tariff_ba_wo_fix_product_id.id)
        self.assertEqual(self.contract_ba.phone_number, phone_number)

    def test_wizard_tariff_change_KO_wo_start_date(self):

        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=self.contract.id
        ).sudo(self.user_admin).create({'summary': 'Tariff change 150 min 2 GB', })

        self.assertRaises(ValidationError, wizard.button_change)

    @patch('odoo.addons.mail.models.mail_thread.MailThread.message_post')
    def test_wizard_tariff_change_break_contract(self, mock_message_post):

        # Pack mobile and ba contracts
        self.contract.write(
            {
                "parent_pack_contract_id": self.contract_ba.id,
            }
        )
        self.contract.contract_line_ids[0].product_id = self.ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        )
        self.contract_ba.write(
            {"children_pack_contract_ids": [(4, self.contract.id, 0)]}
        )

        self.assertTrue(self.contract.is_pack)
        self.assertTrue(self.contract_ba.is_pack)

        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=self.contract.id
        ).sudo(
            self.user_admin
        ).create({
            'start_date': date.today(),
            'summary': 'Tariff change 150 min 2 GB',
        })
        wizard.new_tariff_product_id = self.new_tariff_product_id

        wizard.button_change()

        self.assertFalse(self.contract.is_pack)
        self.assertFalse(self.contract_ba.is_pack)

        message = "Pack broken because of mobile tariff change. Old linked fiber contract ref: '{}'"  # noqa
        mock_message_post.assert_called_with(
            body=message.format(self.contract_ba.code))

    @patch(
        "odoo.addons.somconnexio.models.contract.Contract.quit_sharing_bond_and_update_sharing_mobiles_tariffs",  # noqa
    )
    @patch('odoo.addons.mail.models.mail_thread.MailThread.message_post')
    def test_wizard_tariff_change_quit_sharing(
            self, mock_message_post, mock_quit_sharing_bond):

        contract = self.browse_ref('somconnexio.contract_mobile_il_50_shared_1_of_2')
        sharing_contract = self.browse_ref(
            'somconnexio.contract_mobile_il_50_shared_1_of_2'
        )
        self.assertTrue(contract.is_pack)
        original_shared_bond_id = contract.shared_bond_id
        self.assertTrue(original_shared_bond_id)
        self.assertEquals(
            sharing_contract.shared_bond_id, original_shared_bond_id
        )

        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=contract.id
        ).sudo(
            self.user_admin
        ).create({
            'start_date': date.today(),
            'summary': 'Tariff change 150 min 2 GB',
        })
        wizard.new_tariff_product_id = self.ref(
            'somconnexio.TrucadesIllimitades20GBPack')
        wizard.button_change()

        message = "Stopped sharing data because of mobile tariff change. Old shared bond id: '{}'"  # noqa

        mock_message_post.assert_called_with(
            body=message.format(original_shared_bond_id)
        )
        # Sharing contract contract
        mock_quit_sharing_bond.assert_called_once_with()

    @patch('odoo.addons.mail.models.mail_thread.MailThread.message_post')
    def test_wizard_tariff_BA_change_do_not_break_contract(self, mock_message_post):

        # Pack mobile and ba contracts
        self.contract.write(
            {
                "parent_pack_contract_id": self.contract_ba.id,
            }
        )
        self.contract.contract_line_ids[0].product_id = self.ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        )
        self.contract_ba.write(
            {"children_pack_contract_ids": [(4, self.contract.id, 0)]}
        )

        self.assertTrue(self.contract.is_pack)
        self.assertTrue(self.contract_ba.is_pack)

        wizard = self.env['contract.tariff.change.wizard'].with_context(
            active_id=self.contract_ba.id
        ).sudo(
            self.user_admin
        ).create({
            'start_date': date.today(),
            'summary': 'Tariff change Fiber without fix',
        })
        wizard.new_tariff_product_id = self.browse_ref('somconnexio.SenseFixFibra100Mb')

        wizard.button_change()

        self.assertTrue(self.contract.is_pack)
        self.assertTrue(self.contract_ba.is_pack)
