from correos_preregistro.errors import (
    InvalidApiResponse,
    MissingData,
    UnknownApiResponse,
)
from correos_seguimiento.services.shipment import (
    InvalidApiResponse as InvalidApiResponseSeguimiento,
)
from correos_seguimiento.services.shipment import (
    InvalidCredentials,
    InvalidEndpoint,
    UndefinedCredentials,
)
from correos_seguimiento.errors import (
    UnknownApiResponse as UnknownApiResponseSeguimiento,
)
from mock import Mock, call, patch
from odoo.exceptions import MissingError, ValidationError
from otrs_somconnexio.exceptions import TicketNotReadyToBeUpdatedWithSIMReceivedData
from requests.exceptions import ConnectionError
from socket import error as SocketError

from ...services.mobile_activation_date_service import MobileActivationDateService
from ..helpers import crm_lead_create, random_icc
from ..sc_test_case import SCTestCase


class TicketMock:
    def __init__(self, tid):
        self.tid = tid


class CRMLeadTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.partner_id = self.browse_ref('somconnexio.res_partner_2_demo')
        self.crm_lead_iban = 'ES6000491500051234567891'
        self.crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
            }]
        )
        self.product_pack_mobile = self.env.ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        )
        self.product_mobile = self.env.ref(
            "somconnexio.TrucadesIllimitades20GB"
        )
        self.product_pack_fiber = self.env.ref(
            "somconnexio.Fibra100Mb"
        )
        self.mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'new',
        })
        self.CRMLeadLine = self.env['crm.lead.line']

    def test_crm_lead_action_set_won(self):
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }]
        )
        crm_lead.action_set_won()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead4'))

    def test_crm_lead_action_set_won_raise_error_if_not_in_remesa_stage(self):
        self.assertNotEqual(self.crm_lead.stage_id, self.browse_ref('crm.stage_lead3'))
        self.assertRaisesRegex(
            ValidationError,
            "The crm lead must be in remesa or delivery generated stage.",
            self.crm_lead.action_set_won
        )

    def test_crm_lead_action_set_remesa_raise_error_if_not_in_new_stage(self):
        self.crm_lead.write(
            {
                'iban': 'ES91 2100 0418 4502 0005 1332',
                'stage_id': self.browse_ref('crm.stage_lead4').id,
            })
        self.assertNotEqual(self.crm_lead.stage_id, self.browse_ref('crm.stage_lead1'))
        self.assertRaisesRegex(
            ValidationError,
            "The crm lead must be in new stage.",
            self.crm_lead.action_set_remesa
        )

    def test_crm_lead_action_set_cancelled(self):
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('somconnexio.stage_lead5').id,
            }]
        )
        crm_lead.action_set_cancelled()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('somconnexio.stage_lead5'))

    def test_crm_lead_action_set_delivery_generated(self):
        crm_lead = crm_lead_create(self.env, self.partner_id, "mobile",
                                   portability=True)
        crm_lead.action_set_remesa()

        self.assertFalse(crm_lead.sim_delivery_in_course)

        crm_lead.action_set_delivery_generated()

        self.assertTrue(crm_lead.sim_delivery_in_course)
        self.assertEquals(crm_lead.stage_id, self.browse_ref("somconnexio.stage_lead8"))

    @patch('odoo.addons.mail.models.mail_template.MailTemplate.send_mail')
    def test_crm_lead_action_send_email(self, mock_send_mail):
        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        self.assertFalse(crm_lead.email_sent)

        crm_lead.action_send_email()

        mock_send_mail.assert_called_with(
            crm_lead.id,
            email_values=None, force_send=False,
            notif_layout=False, raise_exception=False
        )

        self.assertTrue(crm_lead.email_sent)

    def test_ensure_crm_lead_iban_in_partner(self):
        self.crm_lead.write(
            {
                'iban': self.crm_lead_iban,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            })

        self.assertEquals(len(self.partner_id.bank_ids), 1)
        self.assertNotEqual(self.crm_lead_iban,
                            self.partner_id.bank_ids[0].sanitized_acc_number)

        self.crm_lead.action_set_won()

        self.assertEquals(len(self.partner_id.bank_ids), 2)
        self.assertEquals(self.crm_lead_iban,
                          self.partner_id.bank_ids[1].sanitized_acc_number)

    def test_crm_lead_partner_email(self):
        self.assertEquals(self.crm_lead.email_from, self.partner_id.email)

    def test_crm_lead_subscription_request_email(self):
        subscription_request_id = self.browse_ref(
            'somconnexio.sc_subscription_request_2_demo')

        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'New Test Lead',
                'subscription_request_id': subscription_request_id.id,
            }]
        )
        self.assertEquals(crm_lead.email_from, subscription_request_id.email)

    def test_crm_lead_new_email(self):
        new_email = "new.email@demo.net"
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'New Test Lead',
                'partner_id': self.partner_id.id,
                'email_from': new_email,
            }]
        )
        self.assertEquals(crm_lead.email_from, new_email)

    def test_crm_lead_action_set_remesa(self):
        product_mobile = self.env.ref(
            "somconnexio.100MinSenseDades_product_template"
        ).product_variant_id
        lead_line_vals = {
            'name': '666666666',
            'product_id': product_mobile.id,
            'mobile_isp_info': self.mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )
        crm_lead.action_set_remesa()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead3'))

    def test_crm_lead_action_set_remesa_raise_error_without_partner(self):
        product_mobile = self.env.ref(
            "somconnexio.100MinSenseDades_product_template"
        ).product_variant_id
        lead_line_vals = {
            'name': '666666666',
            'product_id': product_mobile.id,
            'mobile_isp_info': self.mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': None,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )
        self.assertRaisesRegex(
            ValidationError,
            "Error in {}: The subscription request related must be validated.".format(crm_lead.id),  # noqa
            crm_lead.action_set_remesa
        )

    def test_crm_lead_action_set_remesa_raise_error_with_invalid_bank(self):
        product_mobile = self.env.ref(
            "somconnexio.100MinSenseDades_product_template"
        ).product_variant_id
        lead_line_vals = {
            'name': '666666666',
            'product_id': product_mobile.id,
            'mobile_isp_info': self.mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': 'ES6099991500051234567891',
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )
        self.assertRaisesRegex(
            ValidationError,
            "Error in {}: Invalid bank.".format(crm_lead.id),
            crm_lead.action_set_remesa
        )

    def test_crm_lead_action_set_remesa_raise_error_with_existent_phone_number(self):
        product_mobile = self.env.ref(
            "somconnexio.100MinSenseDades_product_template"
        ).product_variant_id
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '663322234',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        lead_line_vals = {
            'name': '663322234',
            'product_id': product_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
                'stage_id': self.env.ref("crm.stage_lead4").id,
            }]
        )
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )
        self.assertRaisesRegex(
            ValidationError,
            "Error in {}: Contract or validated CRMLead with the same phone already exists.".format(crm_lead.id),  # noqa
            crm_lead.action_set_remesa
        )

    def test_crm_lead_action_set_remesa_location_change_existent_phone_number(self):
        crm_lead = crm_lead_create(self.env, self.partner_id, "mobile")

        copied_mobile_isp_info = crm_lead.lead_line_ids.mobile_isp_info.copy()
        copied_mobile_isp_info.type = "location_change"

        lead_line_vals = {
            'name': 'copied crm lead line',
            'product_id': crm_lead.lead_line_ids.product_id.id,
            'mobile_isp_info': copied_mobile_isp_info.id
        }

        copied_crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )
        copied_crm_lead.action_set_remesa()

        self.assertTrue(copied_crm_lead.skip_duplicated_phone_validation)

    def test_crm_lead_action_set_remesa_raise_error_with_duplicate_phone_number_in_new_line(self):  # noqa
        product_mobile = self.env.ref(
            "somconnexio.100MinSenseDades_product_template"
        ).product_variant_id
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '663322234',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        lead_line_vals = {
            'name': '663322234',
            'product_id': product_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        crm_leads = self.env['crm.lead'].create(
            [
                {
                    'name': 'Test Lead',
                    'partner_id': self.partner_id.id,
                    'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                    'lead_line_ids': [(0, 0, lead_line_vals)],
                    'stage_id': self.env.ref("crm.stage_lead1").id,
                },
                {
                    'name': 'Test Lead',
                    'partner_id': self.partner_id.id,
                    'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                    'lead_line_ids': [(0, 0, lead_line_vals)],
                    'stage_id': self.env.ref("crm.stage_lead1").id,
                }
            ]
        )
        self.assertRaisesRegex(
            ValidationError,
            "Error in {}: Duplicated phone number in CRMLead petitions.".format(crm_leads[0].id),  # noqa
            crm_leads.action_set_remesa,
        )

    def test_crm_lead_action_set_remesa_dont_raise_error_with_existent_phone_number_if_skip_true(self):  # noqa
        product_mobile = self.env.ref(
            "somconnexio.100MinSenseDades_product_template"
        ).product_variant_id
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '663322234',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        lead_line_vals = {
            'name': '663322234',
            'product_id': product_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
                'stage_id': self.env.ref("crm.stage_lead4").id,
            }]
        )
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
                'skip_duplicated_phone_validation': True
            }]
        )

        self.assertNotEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead3'))
        crm_lead.action_set_remesa()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead3'))

    def test_crm_lead_action_set_remesa_dont_raise_error_with_existent_phone_number_if_dash(self):  # noqa
        product_broadband = self.env.ref(
            "somconnexio.ADSL20MB100MinFixMobile_product_template"
        ).product_variant_id
        previous_provider = self.ref("somconnexio.previousprovider3")
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'portability',
            'phone_number': '-',
            'previous_service': 'adsl',
            'previous_provider': previous_provider,
        })
        lead_line_vals = {
            'name': '-',
            'product_id': product_broadband.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
                'stage_id': self.env.ref("crm.stage_lead4").id,
            }]
        )
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )

        self.assertNotEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead3'))
        crm_lead.action_set_remesa()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead3'))

    def test_mobile_phone_number_portability_format_validation(self):
        product_mobile = self.env.ref(
            "somconnexio.100MinSenseDades_product_template"
        ).product_variant_id
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        lead_line_vals = {
            'name': '497453838',
            'product_id': product_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )

        self.assertRaisesRegex(
            ValidationError,
            'Mobile phone number has to be a 9 digit number starting with 6 or 7',
            crm_lead.action_set_remesa
        )

    def test_broadband_phone_number_portability_format_validation(self):
        product_broadband = self.env.ref(
            "somconnexio.ADSL20MB100MinFixMobile_product_template"
        ).product_variant_id
        previous_provider = self.ref("somconnexio.previousprovider3")
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_service': 'adsl',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        lead_line_vals = {
            'name': '497453838',
            'product_id': product_broadband.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )

        self.assertRaisesRegex(
            ValidationError,
            'Landline phone number has to be a dash "-" '
            'or a 9 digit number starting with 8 or 9',
            crm_lead.action_set_remesa
        )

    def test_broadband_phone_number_portability_skip_format_validation(self):
        product_broadband = self.env.ref(
            "somconnexio.ADSL20MB100MinFixMobile_product_template"
        ).product_variant_id
        previous_provider = self.ref("somconnexio.previousprovider3")
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_service': 'adsl',
            'previous_provider': previous_provider,
        })
        lead_line_vals = {
            'name': '497453838',
            'product_id': product_broadband.id,
            'broadband_isp_info': broadband_isp_info.id,
            'check_phone_number': True,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )
        crm_lead.action_set_remesa()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead3'))

    def test_broadband_phone_number_portability_format_validation_dash(self):
        product_broadband = self.env.ref(
            "somconnexio.ADSL20MBSenseFix"
        ).product_variant_id
        previous_provider = self.ref("somconnexio.previousprovider3")
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'portability',
            'phone_number': '-',
            'previous_service': 'adsl',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        lead_line_vals = {
            'name': '497453838',
            'product_id': product_broadband.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [(0, 0, lead_line_vals)],
            }]
        )

        crm_lead.action_set_remesa()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead3'))
        self.assertEquals(crm_lead.phones_from_lead, "[]")

    def test_crm_lead_right_pack(self):
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
            }]
        )
        self.assertTrue(crm)
        self.assertEqual(len(crm.mobile_lead_line_ids), 1)
        self.assertTrue(crm.has_broadband_lead_lines)
        self.assertEqual(len(crm.broadband_lead_line_ids), 1)
        self.assertTrue(crm.has_mobile_lead_lines)
        self.assertEqual(crm.sims_to_deliver, 'one')
        self.assertEqual(
            crm.phones_from_lead,
            str([mobile_isp_info.phone_number])
        )

    def test_crm_lead_right_no_pack(self):
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        self.assertTrue(self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, lead_line_vals),
                    (0, 0, lead_line_vals),
                ],
            }]
        ))

    def test_crm_lead_right_pack_different_number(self):
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        mobile_isp_info_2 = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '666777888',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            "phone_number": "896666666",
            "delivery_street": "Carrer Nogal",
            "delivery_street2": "55 Principal",
            "delivery_zip_code": "08008",
            "delivery_city": "Barcelona",
            "delivery_state_id": self.ref("base.state_es_b"),
            "delivery_country_id": self.ref("base.es"),
            "type": "portability",
            "service_street": "Calle Repet",
            "service_street2": "1 5º A",
            "service_zip_code": "01003",
            "service_city": "Madrid",
            "service_state_id": self.ref("base.state_es_m"),
            "service_country_id": self.ref("base.es"),
            "keep_phone_number": True,
            "previous_owner_name": "Mora",
            "previous_owner_first_name": "Josep",
            "previous_owner_vat_number": "ES61518707D",
            "previous_provider": self.ref("somconnexio.previousprovider3"),
            "previous_service": "fiber",
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        mobile_lead_line_2_vals = {
            'name': '666777888',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info_2.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, mobile_lead_line_2_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
            }]
        )
        self.assertTrue(crm)
        self.assertEqual(len(crm.broadband_lead_line_ids), 1)
        self.assertTrue(crm.has_broadband_lead_lines)
        self.assertEqual(len(crm.mobile_lead_line_ids), 2)
        self.assertTrue(crm.has_mobile_lead_lines)
        self.assertEqual(crm.sims_to_deliver, 'multiple')
        self.assertEqual(
            crm.phones_from_lead,
            str([
                mobile_isp_info.phone_number,
                mobile_isp_info_2.phone_number,
                broadband_isp_info.phone_number
            ])

        )

    def test_crm_lead_right_archive_crm_lead_line(self):
        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        mobile_crm_lead_line = crm_lead.lead_line_ids.filtered("is_mobile")

        self.assertTrue(mobile_crm_lead_line.active)
        self.assertEqual(crm_lead.sims_to_deliver, 'one')

        mobile_crm_lead_line.toggle_active()

        self.assertFalse(mobile_crm_lead_line.active)
        self.assertEqual(crm_lead.sims_to_deliver, 'none')

    def test_crm_lead_right_extra_product(self):
        product_mobile_extra = self.env.ref(
            "somconnexio.TrucadesIllimitades20GB"
        )
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        mobile_lead_line_extra_vals = {
            'name': '497453838',
            'product_id': product_mobile_extra.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        self.assertTrue(self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, mobile_lead_line_extra_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
            }]
        ))

    def test_crm_lead_right_single_pack_product(self):
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
            'icc': random_icc(self.env),
            'has_sim': True,
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        crm = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                ],
            }]
        )
        self.assertTrue(crm)
        self.assertFalse(crm.broadband_lead_line_ids)
        self.assertFalse(crm.has_broadband_lead_lines)
        self.assertEqual(len(crm.mobile_lead_line_ids), 1)
        self.assertTrue(crm.has_mobile_lead_lines)
        self.assertEqual(crm.sims_to_deliver, 'none')
        self.assertEqual(
            crm.phones_from_lead,
            str([mobile_isp_info.phone_number])
        )

    def test_crm_lead_action_set_won_right_pack(self):
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
            'icc': random_icc(self.env),
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        crm_lead.lead_line_ids = self.CRMLeadLine.create([
            mobile_lead_line_vals, broadband_lead_line_vals
        ])
        crm_lead.action_set_won()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead4'))

    def test_crm_lead_action_set_won_no_pack(self):
        product_mobile = self.env.ref(
            "somconnexio.TrucadesIllimitades20GB"
        )
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
            'icc': random_icc(self.env),
        })
        lead_line_vals = {
            'name': '497453838',
            'product_id': product_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        crm_lead.lead_line_ids = self.CRMLeadLine.create([
            lead_line_vals, lead_line_vals
        ])
        crm_lead.action_set_won()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead4'))

    def test_crm_lead_action_set_won_right_pack_different_number(self):
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
            'icc': random_icc(self.env),
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        crm_lead.lead_line_ids = self.CRMLeadLine.create([
            broadband_lead_line_vals, mobile_lead_line_vals, mobile_lead_line_vals
        ])
        crm_lead.action_set_won()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead4'))

    def test_crm_lead_action_set_won_right_pack_extra_product(self):
        product_mobile_extra = self.env.ref(
            "somconnexio.TrucadesIllimitades20GB"
        )
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
            'icc': random_icc(self.env),
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        mobile_lead_line_extra_vals = {
            'name': '497453838',
            'product_id': product_mobile_extra.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        crm_lead.lead_line_ids = self.CRMLeadLine.create([
            broadband_lead_line_vals, mobile_lead_line_vals, mobile_lead_line_extra_vals
        ])
        crm_lead.action_set_won()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead4'))

    def test_crm_lead_right_validation_single_pack_product(self):
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'icc': random_icc(self.env),
            'previous_provider': previous_provider,
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        crm_lead.lead_line_ids = self.CRMLeadLine.create([
            mobile_lead_line_vals
        ])
        crm_lead.action_set_won()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead4'))

    @patch('odoo.addons.somconnexio.models.crm_lead.OTRSClient')
    def test_link_pack_tickets_ok(self, MockOTRSClient):
        fiber_crm_lead = crm_lead_create(self.env, self.partner_id, "fiber",
                                         portability=True)
        fiber_crm_lead_line = fiber_crm_lead.lead_line_ids
        fiber_crm_lead_line.ticket_number = "23828"
        fiber_crm_lead_line.product_id = self.product_pack_fiber.id
        fiber_ticket = TicketMock(1234)
        mobile_crm_lead = crm_lead_create(self.env, self.partner_id, "mobile",
                                          portability=True)
        mobile_crm_lead_line = mobile_crm_lead.lead_line_ids
        mobile_crm_lead_line.ticket_number = "442352"
        mobile_crm_lead_line.product_id = self.product_pack_mobile.id
        mobile_ticket = TicketMock(2345)

        mobile_crm_lead_2 = crm_lead_create(self.env, self.partner_id, "mobile",
                                            portability=True)
        mobile_crm_lead_line_2 = mobile_crm_lead_2.lead_line_ids
        mobile_crm_lead_line_2.ticket_number = "253244"
        mobile_crm_lead_line_2.product_id = self.product_pack_mobile.id
        mobile_ticket_2 = TicketMock(6789)

        MockOTRSClient.return_value = Mock(spec=['get_ticket_by_number',
                                                 'link_tickets'])

        def side_effect_ticket_get(ticket_number):
            if ticket_number == fiber_crm_lead_line.ticket_number:
                return fiber_ticket
            elif ticket_number == mobile_crm_lead_line.ticket_number:
                return mobile_ticket
            elif ticket_number == mobile_crm_lead_line_2.ticket_number:
                return mobile_ticket_2

        MockOTRSClient.return_value.get_ticket_by_number.side_effect = \
            side_effect_ticket_get

        pack_crm_lead = self.env['crm.lead'].create({
            'name': 'Pack Test Lead',
            'partner_id': self.partner_id.id,
            'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
            'lead_line_ids': [(6, 0, [
                fiber_crm_lead_line.id, mobile_crm_lead_line.id,
                mobile_crm_lead_line_2.id
            ])],
            'stage_id': self.env.ref("crm.stage_lead1").id,
        })
        pack_crm_lead.link_pack_tickets()

        MockOTRSClient.return_value.link_tickets.assert_has_calls([
            call(fiber_ticket.tid, mobile_ticket.tid, link_type="ParentChild"),
            call(fiber_ticket.tid, mobile_ticket_2.tid, link_type="ParentChild")
        ], any_order=True)

    @patch(
        "odoo.addons.somconnexio.models.crm_lead.OTRSClient",
        return_value=Mock(spec=["get_ticket_by_number", "link_tickets"]),
    )
    def test_link_pack_tickets_without_ticket_number(self, MockOTRSClient):

        fiber_crm_lead = crm_lead_create(self.env, self.partner_id, "fiber",
                                         portability=True)
        fiber_crm_lead_line = fiber_crm_lead.lead_line_ids
        fiber_crm_lead_line.product_id = self.product_pack_fiber.id
        mobile_crm_lead = crm_lead_create(self.env, self.partner_id, "mobile",
                                          portability=True)
        mobile_crm_lead_line = mobile_crm_lead.lead_line_ids
        mobile_crm_lead_line.product_id = self.product_pack_mobile.id

        pack_crm_lead = self.env['crm.lead'].create({
            'name': 'Pack Test Lead',
            'partner_id': self.partner_id.id,
            'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
            'lead_line_ids': [(6, 0, [
                fiber_crm_lead_line.id, mobile_crm_lead_line.id
                ])],
            'stage_id': self.env.ref("crm.stage_lead1").id,
        })

        self.assertRaisesRegex(
            MissingError,
            "Either mobile or fiber ticket numbers where not found "
            "among the lines of this pack CRMLead",
            pack_crm_lead.link_pack_tickets
        )

    @patch(
        "odoo.addons.somconnexio.models.crm_lead.OTRSClient",
        return_value=Mock(spec=["get_ticket_by_number", "link_tickets"]),
    )
    def test_link_pack_tickets_one_ticket_without_ticket_number(self, MockOTRSClient):

        fiber_crm_lead = crm_lead_create(self.env, self.partner_id, "fiber",
                                         portability=True)
        fiber_crm_lead_line = fiber_crm_lead.lead_line_ids
        fiber_crm_lead_line.product_id = self.product_pack_fiber.id
        mobile_crm_lead = crm_lead_create(self.env, self.partner_id, "mobile",
                                          portability=True)
        mobile_crm_lead_line = mobile_crm_lead.lead_line_ids
        mobile_crm_lead_line.product_id = self.product_pack_mobile.id

        mobile_crm_lead_2 = crm_lead_create(self.env, self.partner_id, "mobile",
                                            portability=True)
        mobile_crm_lead_line_2 = mobile_crm_lead_2.lead_line_ids
        mobile_crm_lead_line_2.ticket_number = "442352"
        mobile_crm_lead_line_2.product_id = self.product_pack_mobile.id
        pack_crm_lead = self.env['crm.lead'].create({
            'name': 'Pack Test Lead',
            'partner_id': self.partner_id.id,
            'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
            'lead_line_ids': [(6, 0, [
                fiber_crm_lead_line.id, mobile_crm_lead_line.id,
                mobile_crm_lead_line_2.id
                ])],
            'stage_id': self.env.ref("crm.stage_lead1").id,
        })

        self.assertRaisesRegex(
            MissingError,
            "Either mobile or fiber ticket numbers where not found "
            "among the lines of this pack CRMLead",
            pack_crm_lead.link_pack_tickets
        )

    @patch('odoo.addons.somconnexio.models.crm_lead.OTRSClient')
    def test_link_pack_tickets_ticket_not_found(self, MockOTRSClient):
        fiber_crm_lead = crm_lead_create(self.env, self.partner_id, "fiber",
                                         portability=True)
        fiber_crm_lead_line = fiber_crm_lead.lead_line_ids
        fiber_crm_lead_line.ticket_number = "23828"
        fiber_crm_lead_line.product_id = self.product_pack_fiber.id
        fiber_ticket = TicketMock(1234)
        mobile_crm_lead = crm_lead_create(self.env, self.partner_id, "mobile",
                                          portability=True)
        mobile_crm_lead_line = mobile_crm_lead.lead_line_ids
        mobile_crm_lead_line.ticket_number = "442352"
        mobile_crm_lead_line.product_id = self.product_pack_mobile.id

        MockOTRSClient.return_value = Mock(
            spec=['get_ticket_by_number', 'link_tickets'])

        def side_effect_ticket_get(ticket_number):
            if ticket_number == fiber_crm_lead_line.ticket_number:
                return fiber_ticket
            elif ticket_number == mobile_crm_lead_line.ticket_number:
                return False

        MockOTRSClient.return_value.get_ticket_by_number.side_effect = \
            side_effect_ticket_get

        pack_crm_lead = self.env['crm.lead'].create({
            'name': 'Pack Test Lead',
            'partner_id': self.partner_id.id,
            'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
            'lead_line_ids': [(6, 0, [
                fiber_crm_lead_line.id, mobile_crm_lead_line.id
                ])],
            'stage_id': self.env.ref("crm.stage_lead1").id,
        })

        self.assertRaisesRegex(
            MissingError,
            "Mobile tickets not found in OTRS with ticket_numbers {}".format(
                mobile_crm_lead_line.ticket_number),
            pack_crm_lead.link_pack_tickets
        )

    @patch('odoo.addons.somconnexio.models.crm_lead.OTRSClient')
    def test_link_pack_tickets_many_tickets_not_found(self, MockOTRSClient):
        fiber_crm_lead = crm_lead_create(self.env, self.partner_id, "fiber",
                                         portability=True)
        fiber_crm_lead_line = fiber_crm_lead.lead_line_ids
        fiber_crm_lead_line.ticket_number = "23828"
        fiber_crm_lead_line.product_id = self.product_pack_fiber.id
        fiber_ticket = TicketMock(1234)
        mobile_crm_lead = crm_lead_create(self.env, self.partner_id, "mobile",
                                          portability=True)
        mobile_crm_lead_line = mobile_crm_lead.lead_line_ids
        mobile_crm_lead_line.ticket_number = "442352"
        mobile_crm_lead_line.product_id = self.product_pack_mobile.id

        mobile_crm_lead_2 = crm_lead_create(self.env, self.partner_id, "mobile",
                                            portability=True)
        mobile_crm_lead_line_2 = mobile_crm_lead_2.lead_line_ids
        mobile_crm_lead_line_2.ticket_number = "253244"
        mobile_crm_lead_line_2.product_id = self.product_pack_mobile.id

        MockOTRSClient.return_value = Mock(
            spec=['get_ticket_by_number', 'link_tickets'])

        def side_effect_ticket_get(ticket_number):
            if ticket_number == fiber_crm_lead_line.ticket_number:
                return fiber_ticket
            elif ticket_number == mobile_crm_lead_line.ticket_number:
                return False
            elif ticket_number == mobile_crm_lead_line_2.ticket_number:
                return False

        MockOTRSClient.return_value.get_ticket_by_number.side_effect = \
            side_effect_ticket_get

        pack_crm_lead = self.env['crm.lead'].create({
            'name': 'Pack Test Lead',
            'partner_id': self.partner_id.id,
            'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
            'lead_line_ids': [(6, 0, [
                fiber_crm_lead_line.id, mobile_crm_lead_line.id,
                mobile_crm_lead_line_2.id
                ])],
            'stage_id': self.env.ref("crm.stage_lead1").id,
        })

        self.assertRaisesRegex(
            MissingError,
            "Mobile tickets not found in OTRS with ticket_numbers {},{}".format(
                mobile_crm_lead_line.ticket_number, mobile_crm_lead_line_2.ticket_number
            ),
            pack_crm_lead.link_pack_tickets
        )

    @patch('odoo.addons.somconnexio.models.crm_lead.OTRSClient')
    def test_link_sharing_data_mobile_tickets_2(self, MockOTRSClient):
        product_shared_bond_2 = self.env.ref(
            "somconnexio.50GBCompartides2mobils"
        )
        mobile_lead_line_vals = {
            'name': 'TEST',
            'product_id': product_shared_bond_2.id,
            'mobile_isp_info': self.mobile_isp_info.id,
            'ticket_number': '23828'
        }
        mobile_lead_line_1 = self.CRMLeadLine.create(mobile_lead_line_vals)
        mobile_lead_line_vals.update({
            'ticket_number': '442352',
            'mobile_isp_info': self.mobile_isp_info.copy().id,
        })
        mobile_lead_line_2 = self.CRMLeadLine.create(mobile_lead_line_vals)

        mobile_ticket = TicketMock(1234)
        mobile_ticket_2 = TicketMock(5678)

        MockOTRSClient.return_value = Mock(
            spec=['get_ticket_by_number', 'link_tickets'])

        def side_effect_ticket_get(ticket_number):
            if ticket_number == mobile_lead_line_1.ticket_number:
                return mobile_ticket
            elif ticket_number == mobile_lead_line_2.ticket_number:
                return mobile_ticket_2

        MockOTRSClient.return_value.get_ticket_by_number.side_effect = \
            side_effect_ticket_get

        shared_data_crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Sharing Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (6, 0, [mobile_lead_line_1.id, mobile_lead_line_2.id])
                ]
            }]
        )

        shared_data_crm_lead.link_sharing_data_mobile_tickets()

        MockOTRSClient.return_value.link_tickets.assert_has_calls([
            call(mobile_ticket.tid, mobile_ticket_2.tid, link_type="Normal"),
        ], any_order=True)

    @patch('odoo.addons.somconnexio.models.crm_lead.OTRSClient')
    def test_link_sharing_data_mobile_tickets_3(self, MockOTRSClient):
        product_shared_bond_3 = self.env.ref(
            "somconnexio.50GBCompartides3mobils"
        )
        mobile_lead_line_vals = {
            'name': 'TEST',
            'product_id': product_shared_bond_3.id,
            'mobile_isp_info': self.mobile_isp_info.id,
            'ticket_number': '23828'
        }
        mobile_lead_line_1 = self.CRMLeadLine.create(mobile_lead_line_vals)
        mobile_lead_line_vals.update({
            'ticket_number': '442352',
            'mobile_isp_info': self.mobile_isp_info.copy().id,
        })
        mobile_lead_line_2 = self.CRMLeadLine.create(mobile_lead_line_vals)
        mobile_lead_line_vals.update({
            'ticket_number': '777223',
            'mobile_isp_info': self.mobile_isp_info.copy().id,
        })
        mobile_lead_line_3 = self.CRMLeadLine.create(mobile_lead_line_vals)

        mobile_ticket = TicketMock(1234)
        mobile_ticket_2 = TicketMock(5678)
        mobile_ticket_3 = TicketMock(8765)

        MockOTRSClient.return_value = Mock(
            spec=['get_ticket_by_number', 'link_tickets'])

        def side_effect_ticket_get(ticket_number):
            if ticket_number == mobile_lead_line_1.ticket_number:
                return mobile_ticket
            elif ticket_number == mobile_lead_line_2.ticket_number:
                return mobile_ticket_2
            elif ticket_number == mobile_lead_line_3.ticket_number:
                return mobile_ticket_3

        MockOTRSClient.return_value.get_ticket_by_number.side_effect = \
            side_effect_ticket_get

        shared_data_crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Sharing Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (6, 0, [mobile_lead_line_1.id, mobile_lead_line_2.id,
                            mobile_lead_line_3.id])
                ]
            }
        )

        shared_data_crm_lead.link_sharing_data_mobile_tickets()

        MockOTRSClient.return_value.link_tickets.assert_has_calls([
            call(mobile_ticket.tid, mobile_ticket_2.tid, link_type="Normal"),
            call(mobile_ticket.tid, mobile_ticket_3.tid, link_type="Normal"),
            call(mobile_ticket_2.tid, mobile_ticket_3.tid, link_type="Normal"),
        ], any_order=True)

    @patch('odoo.addons.somconnexio.models.crm_lead.OTRSClient')
    def test_link_sharing_data_mobile_tickets_single(self, MockOTRSClient):
        product_shared_bond_2 = self.env.ref(
            "somconnexio.50GBCompartides2mobils"
        )
        mobile_lead_line_vals = {
            'name': 'TEST',
            'product_id': product_shared_bond_2.id,
            'mobile_isp_info': self.mobile_isp_info.id,
            'ticket_number': '23828'
        }

        shared_crm_lead = self.env['crm.lead'].create({
            'name': 'Pack Test Lead',
            'partner_id': self.partner_id.id,
            'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
            'lead_line_ids': [
                (0, 0, mobile_lead_line_vals),
            ],
            'stage_id': self.env.ref("crm.stage_lead1").id,
        })

        self.assertRaisesRegex(
            ValidationError,
            "We cannot share bonds with <2 or >3 mobiles",
            shared_crm_lead.link_sharing_data_mobile_tickets
        )

    @patch('odoo.addons.somconnexio.models.crm_lead.OTRSClient')
    def test_link_sharing_data_mobile_tickets_4(
            self, MockOTRSClient):
        product_shared_bond_3 = self.env.ref(
            "somconnexio.50GBCompartides3mobils"
        )
        mobile_lead_line_vals = {
            'name': 'TEST',
            'product_id': product_shared_bond_3.id,
            'mobile_isp_info': self.mobile_isp_info.id,
            'ticket_number': '23828'
        }
        mobile_lead_line = self.CRMLeadLine.create(mobile_lead_line_vals)
        mobile_lead_line_2 = self.CRMLeadLine.create(mobile_lead_line_vals)
        mobile_lead_line_3 = self.CRMLeadLine.create(mobile_lead_line_vals)
        mobile_lead_line_4 = self.CRMLeadLine.create(mobile_lead_line_vals)

        shared_crm_lead = self.env['crm.lead'].create({
            'name': 'Pack Test Lead',
            'partner_id': self.partner_id.id,
            'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
            'lead_line_ids': [
                (6, 0, [mobile_lead_line.id, mobile_lead_line_2.id,
                        mobile_lead_line_3.id, mobile_lead_line_4.id])
            ],
            'stage_id': self.env.ref("crm.stage_lead1").id,
        })

        self.assertRaisesRegex(
            ValidationError,
            "We cannot share bonds with <2 or >3 mobiles",
            shared_crm_lead.link_sharing_data_mobile_tickets
        )

    @patch(
        "odoo.addons.somconnexio.models.crm_lead.CorreosShipment",
        return_value=Mock(spec=["create"]),
    )
    def test_create_shipment_ok(self, mock_correos_shipment):
        shipment_code = 'test_code'
        label_file = 'XXXXXXXX'

        mock_shipment = Mock(spec=['shipment_code',
                                   'label_file'])
        mock_shipment.shipment_code = shipment_code
        mock_shipment.label_file = label_file

        mock_correos_shipment.return_value.create.return_value = mock_shipment

        crm_lead = crm_lead_create(self.env, self.partner_id, "mobile",
                                   portability=True)
        crm_lead.action_set_remesa()

        crm_lead.create_shipment()

        self.assertEquals(crm_lead.stage_id, self.browse_ref("somconnexio.stage_lead6"))
        self.assertEquals(crm_lead.correos_tracking_code, "test_code")
        mock_correos_shipment.return_value.create.assert_called_once_with(
            crm_lead, None
        )
        attachment = self.env["ir.attachment"].search([
            ("res_id", "=", crm_lead.id),
            ("res_model", "=", "crm.lead"),
        ])
        self.assertTrue(attachment)

        self.assertEquals(
            attachment.name, "shipment_{}".format(shipment_code)
        )
        self.assertEquals(attachment.datas.decode(), label_file)

    @patch("odoo.addons.mail.models.mail_thread.MailThread.message_post")
    @patch(
        "odoo.addons.somconnexio.models.crm_lead.CorreosShipment",
        side_effect=MissingData("Nombre"),
    )
    def test_create_shipment_KO_MissingData(
        self,
        mock_correos_shipment,
        mock_message_post,
    ):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        crm_lead.create_shipment()

        self.assertEquals(crm_lead.stage_id, self.browse_ref("somconnexio.stage_lead7"))
        mock_message_post.assert_called_with(
            body="Error sending the delivery to Correos with the next field: Nombre"
        )

    @patch("odoo.addons.mail.models.mail_thread.MailThread.message_post")
    @patch(
        "odoo.addons.somconnexio.models.crm_lead.CorreosShipment",
        side_effect=UnknownApiResponse("Exception Message"),
    )
    def test_create_shipment_KO_UnknownApiResponse(
        self,
        mock_correos_shipment,
        mock_message_post,
    ):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        crm_lead.create_shipment()

        self.assertEquals(crm_lead.stage_id, self.browse_ref("somconnexio.stage_lead7"))
        mock_message_post.assert_called_with(
            body="Error sending the delivery to Correos. Contact with Sistemas team."
            " Error: Exception Message"
        )

    @patch("odoo.addons.mail.models.mail_thread.MailThread.message_post")
    @patch(
        "odoo.addons.somconnexio.models.crm_lead.CorreosShipment",
        side_effect=InvalidApiResponse("Exception Message"),
    )
    def test_create_shipment_KO_InvalidApiResponse(
        self,
        mock_correos_shipment,
        mock_message_post,
    ):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        crm_lead.create_shipment()

        self.assertEquals(crm_lead.stage_id, self.browse_ref("somconnexio.stage_lead7"))
        mock_message_post.assert_called_with(
            body="Error sending the delivery to Correos. Contact with Sistemas team."
            " Error: Exception Message"
        )

    @patch("odoo.addons.mail.models.mail_thread.MailThread.message_post")
    @patch(
        "odoo.addons.somconnexio.models.crm_lead.CorreosShipment",
        side_effect=Exception(),
    )
    def test_create_shipment_KO_Exception(
        self,
        mock_correos_shipment,
        mock_message_post,
    ):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        with self.assertRaises(Exception):
            crm_lead.create_shipment()

    def test_crm_lead_right_mobile_icc(self):
        self.env['ir.config_parameter'].set_param(
            'somconnexio.icc_start_sequence', "1234"
        )
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
            'icc': "1234567890123456789",
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        crm_lead.lead_line_ids = self.CRMLeadLine.create(mobile_lead_line_vals)
        crm_lead.action_set_won()
        self.assertEquals(crm_lead.stage_id, self.browse_ref('crm.stage_lead4'))

    def test_crm_lead_wrong_mobile_icc_bad_prefix(self):
        self.env['ir.config_parameter'].set_param(
            'somconnexio.icc_start_sequence', "1234"
        )
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
            'icc': "XXXX567890123456789",
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        crm_lead.lead_line_ids = self.CRMLeadLine.create(mobile_lead_line_vals)
        self.assertRaisesRegex(
            ValidationError,
            "The value of ICC is not right: it must contain "
            "19 digits and starts with 1234",
            crm_lead.action_set_won,
        )

    def test_crm_lead_wrong_mobile_icc_bad_length(self):
        self.env['ir.config_parameter'].set_param(
            'somconnexio.icc_start_sequence', "1234"
        )
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
            'icc': "1234567890",
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        crm_lead.lead_line_ids = self.CRMLeadLine.create(mobile_lead_line_vals)
        self.assertRaisesRegex(
            ValidationError,
            "The value of ICC is not right: it must contain "
            "19 digits and starts with 1234",
            crm_lead.action_set_won,
        )

    def test_crm_lead_wrong_mobile_icc_not_filled(self):
        self.env['ir.config_parameter'].set_param(
            'somconnexio.icc_start_sequence', "1234"
        )
        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        crm_lead.lead_line_ids = self.CRMLeadLine.create(mobile_lead_line_vals)
        self.assertRaisesRegex(
            ValidationError,
            "The ICC value of all mobile lines is not filled",
            crm_lead.action_set_won,
        )

    def test_crm_lead_broadband_w_fix_lead_line_ids(self):
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.ref('somconnexio.Fibra100Mb'),
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead.lead_line_ids = self.CRMLeadLine.create(broadband_lead_line_vals)
        self.assertEquals(
            crm_lead.broadband_w_fix_lead_line_ids, crm_lead.lead_line_ids
        )
        self.assertFalse(crm_lead.broadband_wo_fix_lead_line_ids)

    def test_crm_lead_broadband_wo_fix_lead_line_ids(self):
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'stage_id': self.browse_ref('crm.stage_lead3').id,
            }
        )
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.ref('somconnexio.SenseFixFibra100Mb'),
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead.lead_line_ids = self.CRMLeadLine.create(broadband_lead_line_vals)
        self.assertEquals(
            crm_lead.broadband_wo_fix_lead_line_ids, crm_lead.lead_line_ids
        )
        self.assertFalse(crm_lead.broadband_w_fix_lead_line_ids)

    @patch('odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket')
    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)  # noqa
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_not_delivered(self, mock_tracking_shipment, mock_set_received):  # noqa

        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = False

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': 'ZZZ',
            }]
        )
        self.assertEquals(crm_lead.sims_to_deliver, 'one')
        crm_lead.track_correos_delivery()
        mock_tracking_shipment.assert_called_with('XXX', 'YYY', 'ZZZ')
        mock_delivery.is_delivered.assert_called_once()
        mock_set_received.return_value.run.assert_not_called()
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_not_delivered_relabeled(self, mock_tracking_shipment):  # noqa
        correos_tracking_code = 'AAA'
        new_tracking_code = 'BBB'

        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = False
        mock_delivery.is_relabeled.return_value = True
        mock_delivery.get_relabeled_shipment_code.return_value = new_tracking_code

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': correos_tracking_code,
            }
        )

        crm_lead.track_correos_delivery()

        mock_tracking_shipment.assert_called_with('XXX', 'YYY', correos_tracking_code)
        mock_delivery.is_delivered.assert_called()
        mock_delivery.is_relabeled.assert_called()
        mock_delivery.get_relabeled_shipment_code.assert_called()
        self.assertEqual(crm_lead.correos_tracking_code, new_tracking_code)
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_not_delivered_relabeled_index_error(self, mock_tracking_shipment):  # noqa
        correos_tracking_code = 'AAA'

        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = False
        mock_delivery.is_relabeled.return_value = True
        mock_delivery.get_relabeled_shipment_code.side_effect = IndexError("IndexError while retrieving relabeled shipment code")  # noqa

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            {
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': correos_tracking_code,
            }
        )

        with self.assertRaises(IndexError):
            crm_lead.track_correos_delivery()

        mock_tracking_shipment.assert_called_with('XXX', 'YYY', correos_tracking_code)
        mock_delivery.is_delivered.assert_called()
        mock_delivery.is_relabeled.assert_called()
        mock_delivery.get_relabeled_shipment_code.assert_called()
        self.assertEqual(crm_lead.correos_tracking_code, correos_tracking_code)
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch('odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket')
    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_delivered(self, mock_tracking_shipment, mock_set_received):  # noqa

        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = True
        mock_delivery.is_relabeled.return_value = False

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
            'ticket_number': '1234',
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': 'ZZZ',
            }]
        )
        mobile_lead_line = crm_lead.lead_line_ids.filtered('is_mobile')
        self.assertEquals(crm_lead.sims_to_deliver, 'one')

        crm_lead.track_correos_delivery()

        mock_tracking_shipment.assert_called_with('XXX', 'YYY', 'ZZZ')
        is_portability = mobile_lead_line.is_portability()
        mock_delivery.is_delivered.assert_called()
        mock_set_received.assert_called_once_with(
            mobile_lead_line_vals["ticket_number"],
            MobileActivationDateService(self.env, is_portability).get_activation_date(),
            MobileActivationDateService(self.env, is_portability).get_introduced_date(),
        )
        mock_set_received.return_value.run.assert_called()
        self.assertFalse(crm_lead.sim_delivery_in_course)

    @patch('odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket')
    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_delivered_lead_line_has_sim(self, mock_tracking_shipment, mock_set_received):  # noqa

        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = True

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        mobile_isp_info_with_sim = mobile_isp_info.copy()
        mobile_isp_info_with_sim.update({
            'has_sim': True,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
            'ticket_number': '1234',
        }
        mobile_lead_line_with_sim_vals = {
            'name': '699123456',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info_with_sim.id,
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, mobile_lead_line_with_sim_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': 'ZZZ',
            }]
        )
        mobile_lead_line_with_sim = crm_lead.lead_line_ids.filtered(
            'mobile_isp_info_has_sim'
        )
        mobile_lead_line_without_sim = crm_lead.lead_line_ids.filtered(
            lambda line: not line.mobile_isp_info_has_sim and line.is_mobile
        )
        self.assertTrue(mobile_lead_line_with_sim.mobile_isp_info_has_sim)
        self.assertEquals(crm_lead.sims_to_deliver, 'one')

        crm_lead.track_correos_delivery()

        is_portability = mobile_lead_line_without_sim.is_portability()
        mock_set_received.assert_called_once_with(
            mobile_lead_line_vals["ticket_number"],
            MobileActivationDateService(self.env, is_portability).get_activation_date(),
            MobileActivationDateService(self.env, is_portability).get_introduced_date(),
        )
        mock_tracking_shipment.assert_called_with('XXX', 'YYY', 'ZZZ')
        mock_delivery.is_delivered.assert_called()
        mock_set_received.return_value.run.assert_called()
        self.assertFalse(crm_lead.sim_delivery_in_course)

    @patch('odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket')
    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_undefined_credentials(self, mock_tracking_shipment, mock_set_received):  # noqa

        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.side_effect = UndefinedCredentials()

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
            'ticket_number': '1234',
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': 'ZZZ',
            }]
        )
        self.assertEquals(crm_lead.sims_to_deliver, 'one')
        self.assertRaisesRegex(
            UndefinedCredentials,
            'Credentials for Correos API are not defined',
            crm_lead.track_correos_delivery
        )
        mock_set_received.return_value.run.assert_not_called()
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch('odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket')
    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_invalid_credentials(self, mock_tracking_shipment, mock_set_received):  # noqa

        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.side_effect = InvalidCredentials()

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
            'ticket_number': '1234',
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': 'ZZZ',
            }]
        )
        self.assertEquals(crm_lead.sims_to_deliver, 'one')
        self.assertRaisesRegex(
            InvalidCredentials,
            'Credentials for Correos API are not valid',
            crm_lead.track_correos_delivery
        )
        mock_set_received.return_value.run.assert_not_called()
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch('odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket')
    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch('time.sleep')
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_error_retry_3(self, delay, mock_tracking_shipment, mock_set_received):  # noqa

        mock_delivery = Mock(spec=["is_delivered"])
        mock_delivery.is_delivered.return_value = True

        def is_delivered_side_effect(*args, **kwargs):
            if mock_tracking_shipment.call_count == 1:
                raise SocketError()
            elif mock_tracking_shipment.call_count < 3:
                raise InvalidEndpoint()
            elif mock_tracking_shipment.call_count == 3:
                raise ConnectionError()
            return mock_delivery

        mock_tracking_shipment.return_value.build.side_effect = is_delivered_side_effect

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
            'ticket_number': '1234',
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': 'ZZZ',
            }]
        )

        self.assertEquals(crm_lead.sims_to_deliver, 'one')

        crm_lead.track_correos_delivery()

        self.assertEquals(mock_tracking_shipment.call_count, 4)
        mock_delivery.is_delivered.assert_called_once()
        self.assertTrue(mock_delivery.is_delivered())
        mock_set_received.return_value.run.assert_called_once_with()
        self.assertFalse(crm_lead.sim_delivery_in_course)

    @patch('odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket')
    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch('time.sleep')
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_error_retry_4(self, delay, mock_tracking_shipment, mock_set_received): # noqa

        mock_delivery = Mock(spec=["is_delivered"])
        mock_delivery.is_delivered.return_value = False

        def is_delivered_side_effect(*args, **kwargs):
            if mock_tracking_shipment.call_count < 21:
                raise InvalidEndpoint()
            elif mock_tracking_shipment.call_count == 21:
                raise ConnectionError()
            return mock_delivery

        mock_tracking_shipment.return_value.build.side_effect = is_delivered_side_effect

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
            'ticket_number': '1234',
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': 'ZZZ',
            }]
        )

        self.assertEquals(crm_lead.sims_to_deliver, 'one')
        self.assertRaisesRegex(
            ConnectionError,
            'Connection with Correos API failed',
            crm_lead.track_correos_delivery
        )

    @patch('odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket')
    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_unknown_api_response(self, mock_tracking_shipment, mock_set_received):  # noqa

        mock_tracking_shipment.return_value.build.side_effect = UnknownApiResponseSeguimiento()  # noqa

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
            'ticket_number': '1234',
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': 'ZZZ',
            }]
        )
        self.assertEquals(crm_lead.sims_to_deliver, 'one')
        self.assertRaisesRegex(
            UnknownApiResponseSeguimiento,
            "The JSON shows a data format that can't be parsed",
            crm_lead.track_correos_delivery
        )
        mock_set_received.return_value.run.assert_not_called()
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch('odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket')
    @patch('odoo.addons.somconnexio.models.crm_lead.TrackingShipment', autospec=True)
    @patch.dict('os.environ', {
        'CORREOS_USER': 'XXX',
        'CORREOS_PASSWORD': 'YYY'
    })
    def test_track_correos_delivery_invalid_api_response(self, mock_tracking_shipment, mock_set_received):  # noqa

        mock_tracking_shipment.return_value.build.side_effect = InvalidApiResponseSeguimiento()  # noqa

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env['mobile.isp.info'].create({
            'type': 'portability',
            'phone_number': '497453838',
            'previous_contract_type': 'contract',
            'previous_provider': previous_provider,
        })
        broadband_isp_info = self.env['broadband.isp.info'].create({
            'type': 'new',
        })
        mobile_lead_line_vals = {
            'name': '497453838',
            'product_id': self.product_pack_mobile.id,
            'mobile_isp_info': mobile_isp_info.id,
            'ticket_number': '1234',
        }
        broadband_lead_line_vals = {
            "name": '916079471',
            'product_id': self.product_pack_fiber.id,
            'broadband_isp_info': broadband_isp_info.id,
        }
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
                'iban': self.partner_id.bank_ids[0].sanitized_acc_number,
                'lead_line_ids': [
                    (0, 0, mobile_lead_line_vals),
                    (0, 0, broadband_lead_line_vals),
                ],
                'sim_delivery_in_course': True,
                'correos_tracking_code': 'ZZZ',
            }]
        )
        self.assertEquals(crm_lead.sims_to_deliver, 'one')
        self.assertRaisesRegex(
            InvalidApiResponseSeguimiento,
            'Returned data is not JSON valid',
            crm_lead.track_correos_delivery
        )
        mock_set_received.return_value.run.assert_not_called()
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch("odoo.addons.somconnexio.models.crm_lead.SetSIMRecievedMobileTicket")
    @patch("odoo.addons.somconnexio.models.crm_lead.TrackingShipment", autospec=True)
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_correos_delivery_ticket_not_ready_exception(
        self, mock_tracking_shipment, mock_set_received
    ):

        previous_provider = self.ref("somconnexio.previousprovider1")
        mobile_isp_info = self.env["mobile.isp.info"].create(
            {
                "type": "portability",
                "phone_number": "497453838",
                "previous_contract_type": "contract",
                "previous_provider": previous_provider,
            }
        )
        broadband_isp_info = self.env["broadband.isp.info"].create(
            {
                "type": "new",
            }
        )
        mobile_lead_line_vals = {
            "name": "497453838",
            "product_id": self.product_pack_mobile.id,
            "mobile_isp_info": mobile_isp_info.id,
            "ticket_number": "1234",
        }
        broadband_lead_line_vals = {
            "name": "916079471",
            "product_id": self.product_pack_fiber.id,
            "broadband_isp_info": broadband_isp_info.id,
        }
        crm_lead = self.env["crm.lead"].create(
            [
                {
                    "name": "Test Lead",
                    "partner_id": self.partner_id.id,
                    "iban": self.partner_id.bank_ids[0].sanitized_acc_number,
                    "lead_line_ids": [
                        (0, 0, mobile_lead_line_vals),
                        (0, 0, broadband_lead_line_vals),
                    ],
                    "sim_delivery_in_course": True,
                    "correos_tracking_code": "ZZZ",
                }
            ]
        )
        mock_tracking_shipment.return_value.build.side_effect = (
            TicketNotReadyToBeUpdatedWithSIMReceivedData(
                mobile_lead_line_vals["ticket_number"]
            )
        )

        self.assertEquals(crm_lead.sims_to_deliver, "one")
        self.assertTrue(crm_lead.sim_delivery_in_course)
