import json
from ...common_service import BaseEMCRestCaseAdmin
from datetime import date, timedelta, datetime


class TestContractCountController(BaseEMCRestCaseAdmin):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Contract = self.env['contract.contract']
        self.Partner = self.env['res.partner']
        vodafone_fiber_contract_service_info = self.env[
            "vodafone.fiber.service.contract.info"
        ].create(
            {
                "phone_number": "654321123",
                "vodafone_id": "123",
                "vodafone_offer_code": "456",
            }
        )
        partner = self.browse_ref("somconnexio.res_partner_1_demo")
        partner_id = partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner service OK',
            'type': 'service'
        })
        product_ref = self.browse_ref('somconnexio.Fibra100Mb')
        product = self.env["product.product"].search(
            [('default_code', '=', product_ref.default_code)]
        )
        self.contract_line = {
            "name": product.name,
            "product_id": product.id,
            "date_start": "2020-01-01 00:00:00",
            "recurring_next_date": date.today() + timedelta(days=30),
        }
        self.vals_contract = {
            'name': 'Test Contract Broadband',
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
                vodafone_fiber_contract_service_info.id
            ),
            'bank_id': partner.bank_ids.id,
            'contract_line_ids': [
                (0, False, self.contract_line)
            ]

        }
        self.vals_subscription = {
            'already_cooperator': False,
            'is_company': False,
            'firstname': 'Manuel',
            'lastname': 'Dublues Test',
            'email': 'manuel@demo-test.net',
            'ordered_parts': 1,
            'address': 'schaerbeekstraat',
            'city': 'Brussels',
            'zip_code': '1111',
            'country_id': self.ref('base.es'),
            'date': datetime.now() - timedelta(days=12),
            'company_id': 1,
            'source': 'manual',
            'share_product_id': False,
            'lang': 'en_US',
            'sponsor_id': False,
            'vat': "53020066Y",
            'iban': 'ES6020808687312159493841',
            'state': 'done'
        }

    def test_route_count_one_contract_active(self, *args):
        url = "/public-api/contract-count"
        count_contract = self.env['contract.contract'].search_count([])
        self.Contract.unlink()
        self.Contract.create(self.vals_contract)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn('contracts', decoded_response)
        self.assertEquals(decoded_response["contracts"], count_contract+1)

    def test_route_doesnt_count_one_contract_terminated(self, *args):
        url = "/public-api/contract-count"
        count_contract = self.env['contract.contract'].search_count([])
        self.Contract.unlink()
        self.vals_contract['is_terminated'] = True
        self.Contract.create(self.vals_contract)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn('contracts', decoded_response)
        self.assertEquals(decoded_response["contracts"], count_contract)

    def test_route_count_one_member(self, *args):
        url = "/public-api/contract-count"
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn('members', decoded_response)
        count_members = decoded_response['members']
        self.Partner.create({
            'name': 'test member', 'member': True, 'coop_candidate': False,
            'customer': True
        })
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn('members', decoded_response)
        self.assertEquals(decoded_response["members"]-count_members, 1)

    def test_route_count_one_coop_candidate(self, *args):
        url = "/public-api/contract-count"
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn('members', decoded_response)
        count_members = decoded_response['members']
        partner = self.Partner.create({
            'name': 'test member', 'coop_candidate': True, 'customer': True
        })
        self.vals_subscription['partner_id'] = partner.id
        self.env['subscription.request'].create(self.vals_subscription)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn('members', decoded_response)
        self.assertEquals(decoded_response["members"]-count_members, 1)

    def test_route_doesnt_count_one_partner_not_member(self, *args):
        url = "/public-api/contract-count"
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn('members', decoded_response)
        count_members = decoded_response['members']
        self.Partner.create({
            'name': 'test member', 'member': False, 'coop_candidate': False,
            'customer': True
        })
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        decoded_response = json.loads(response.content.decode("utf-8"))
        self.assertIn('members', decoded_response)
        self.assertEquals(decoded_response["members"]-count_members, 0)
