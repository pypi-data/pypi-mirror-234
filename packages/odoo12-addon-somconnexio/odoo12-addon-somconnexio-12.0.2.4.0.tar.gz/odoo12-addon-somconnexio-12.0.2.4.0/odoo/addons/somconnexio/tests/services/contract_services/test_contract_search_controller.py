import json
import odoo
from faker import Faker
from ...common_service import BaseEMCRestCaseAdmin
from ....services.contract_contract_service import ContractService
from ...helpers import crm_lead_create


class TestContractSearchController(BaseEMCRestCaseAdmin):

    def setUp(self):
        super().setUp()
        self.url = "/api/contract"
        self.partner = self.browse_ref('somconnexio.res_partner_2_demo')
        self.phone_number = "654321123"
        mbl_contract_service_info = self.env["mobile.service.contract.info"].create(
            {
                "phone_number": self.phone_number,
                "icc": "123",
            }
        )
        fake = Faker("es-ES")
        crm_lead = crm_lead_create(self.env, self.partner, "fiber", portability=True)
        self.mandate = self.env["account.banking.mandate"].create(
            {
                "partner_bank_id": self.partner.bank_ids[0].id,
                "state": "valid",
                "partner_id": self.partner.id,
                "signature_date": fake.date_time_this_month(),
            }
        )
        self.contract = self.env["contract.contract"].create(
            {
                "name": "Test Contract Mobile",
                "partner_id": self.partner.id,
                "service_partner_id": self.partner.id,
                "invoice_partner_id": self.partner.id,
                "service_technology_id": self.ref(
                    "somconnexio.service_technology_mobile"
                ),
                "service_supplier_id": self.ref(
                    "somconnexio.service_supplier_masmovil"
                ),
                "mobile_contract_service_info_id": mbl_contract_service_info.id,
                "contract_line_ids": [
                    (
                        0,
                        False,
                        {
                            "name": "Mobile",
                            "product_id": self.ref("somconnexio.150Min1GB"),
                        },
                    )
                ],
                "mandate_id": self.mandate.id,
                "crm_lead_line_id": crm_lead.lead_line_ids[0].id,
                "fiber_signal_type_id": self.ref("somconnexio.FTTH_fiber_signal"),
            }
        )
        router_product = self.env["product.product"].search(
            [
                ("default_code", "=", "HG8245Q2"),
            ]
        )
        router_lot = self.env["stock.production.lot"].create(
            {
                "product_id": router_product.id,
                "name": "123",
                "router_mac_address": "12:BB:CC:DD:EE:90",
            }
        )
        broadband_contract_service_info = self.env["adsl.service.contract.info"].create(
            {
                "phone_number": "654123456",
                "administrative_number": "123",
                "router_product_id": router_product.id,
                "router_lot_id": router_lot.id,
                "ppp_user": "ringo",
                "ppp_password": "rango",
                "endpoint_user": "connection",
                "endpoint_password": "password",
            }
        )

        self.broadband_contract = self.env["contract.contract"].create(
            {
                "name": "Test Contract Broadband",
                "partner_id": self.partner.id,
                "service_partner_id": self.partner.id,
                "invoice_partner_id": self.partner.id,
                "service_technology_id": self.ref(
                    "somconnexio.service_technology_adsl"
                ),
                "service_supplier_id": self.ref("somconnexio.service_supplier_jazztel"),
                "adsl_service_contract_info_id": (broadband_contract_service_info.id),
                "bank_id": self.partner.bank_ids.id,
                "contract_line_ids": [
                    (
                        0,
                        False,
                        {
                            "name": "ADSL",
                            "product_id": self.ref("somconnexio.ADSL20MB1000MinFix"),
                        },
                    )
                ],
            }
        )
        fiber_contract_service_info = self.env["mm.fiber.service.contract.info"].create(
            {
                "phone_number": "934567521",
                "mm_id": "934567521",
            }
        )

        self.fiber_contract = self.env["contract.contract"].create(
            {
                "name": "Test Contract Fiber",
                "partner_id": self.partner.id,
                "service_partner_id": self.partner.id,
                "invoice_partner_id": self.partner.id,
                "service_technology_id": self.ref(
                    "somconnexio.service_technology_fiber"
                ),
                "service_supplier_id": self.ref(
                    "somconnexio.service_supplier_masmovil"
                ),
                "mm_fiber_service_contract_info_id": fiber_contract_service_info.id,
                "bank_id": self.partner.bank_ids.id,
                "contract_line_ids": [
                    (
                        0,
                        False,
                        {
                            "name": "Fiber",
                            "product_id": self.ref("somconnexio.Fibra100Mb"),
                        },
                    )
                ],
            }
        )

    @odoo.tools.mute_logger("odoo.addons.auth_api_key.models.ir_http")
    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_without_auth(self):
        response = self.http_get_without_auth()

        self.assertEquals(response.status_code, 403)
        self.assertEquals(response.reason, "FORBIDDEN")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_unknown_parameter(self):
        url = "{}?{}={}".format(self.url, "unknown_parameter", "2828")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_multiple_parameters(self):
        url = "{}?{}={}&{}={}".format(self.url, "code", "111111",
                                      "partner_vat", "ES1828028")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_code_not_found(self):
        url = "{}?{}={}".format(self.url, "code", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_vat_not_found(self):
        url = "{}?{}={}".format(self.url, "partner_vat", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_phone_number_not_found(self):
        url = "{}?{}={}".format(self.url, "phone_number", "111111")
        response = self.http_get(url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.reason, "NOT FOUND")

    def test_route_contract_search_code_ok(self):
        url = "{}?{}={}".format(self.url, "code", self.contract.code)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.contract.id)

    def test_route_contract_search_phone_number_ok(self, *args):
        url = "{}?{}={}".format(self.url, "phone_number", self.contract.phone_number)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(len(result["contracts"]), 1)
        self.assertEquals(result["contracts"][0]["id"], self.contract.id)

    def test_route_contract_search_partner_code_ok(self):
        url = "{}?{}={}".format(self.url, "customer_ref", self.contract.partner_id.ref)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn(self.contract.id, [c["id"] for c in result["contracts"]])

    def test_route_contract_search_partner_vat_multiple_ok(self, *args):
        url = "{}?{}={}".format(self.url, "partner_vat", self.partner.vat)
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", result)
        self.assertEquals(len(result["contracts"]), 3)
        self.assertEquals(result["contracts"][0]["id"], self.contract.id)
        self.assertEquals(result["contracts"][1]["id"], self.broadband_contract.id)
        self.assertEquals(result["contracts"][2]["id"], self.fiber_contract.id)

    def test_route_contract_search_partner_pagination_first_page(self, *args):
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "limit", 1
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", result)
        self.assertEquals(len(result['contracts']), 1)
        self.assertEquals(result['contracts'][0]["id"], self.contract.id)
        self.assertIn("paging", result)
        self.assertIn("limit", result["paging"])
        self.assertEquals(result["paging"]["limit"], 1)
        self.assertIn("offset", result["paging"])
        self.assertEquals(result["paging"]["offset"], 0)
        self.assertIn("totalNumberOfRecords", result["paging"])
        self.assertEquals(result["paging"]["totalNumberOfRecords"], 3)

    def test_route_contract_search_partner_pagination_second_page(self, *args):
        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "limit", 1, "offset", 1
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", result)
        self.assertEquals(len(result["contracts"]), 1)
        self.assertEquals(result["contracts"][0]["id"], self.broadband_contract.id)
        self.assertIn("paging", result)
        self.assertIn("offset", result["paging"])
        self.assertEquals(result["paging"]["offset"], 1)
        self.assertIn("limit", result["paging"])
        self.assertEquals(result["paging"]["limit"], 1)
        self.assertIn("totalNumberOfRecords", result["paging"])
        self.assertEquals(result["paging"]["totalNumberOfRecords"], 3)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_pagination_bad_limit(self, *args):
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "limit", 'XXX'
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Limit must be numeric")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_pagination_bad_offset(self, *args):
        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "limit", '1', "offset", 'XXX'
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Offset must be numeric")

    def test_route_contract_search_partner_sort_by(self, *args):
        self.contract.phone_number = "ZZZ"
        self.contract.code = "ZZZ"
        self.broadband_contract.phone_number = "YYY"
        self.broadband_contract.code = "YYY"
        self.fiber_contract.phone_number = "XXX"
        self.fiber_contract.code = "XXX"

        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortBy", "name"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        codes = [c["code"] for c in result["contracts"]]
        self.assertEquals(codes, ["XXX", "YYY", "ZZZ"])
        self.assertIn("paging", result)
        self.assertIn("sortBy", result['paging'])
        self.assertEquals(result['paging']['sortBy'], 'name')

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_bad_sort_by(self, *args):
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortBy", "XXX"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "Invalid field to sortBy")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_sort_order(self, *args):
        self.contract.phone_number = "ZZZ"
        self.contract.code = "ZZZ"
        self.broadband_contract.phone_number = "YYY"
        self.broadband_contract.code = "YYY"
        self.fiber_contract.phone_number = "XXX"
        self.fiber_contract.code = "XXX"

        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortBy", "name", "sortOrder", "DESCENDENT"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        codes = [c["code"] for c in result["contracts"]]
        self.assertEquals(codes, ["ZZZ", "YYY", "XXX"])
        self.assertIn("paging", result)
        self.assertIn("sortBy", result['paging'])
        self.assertEquals(result['paging']['sortBy'], 'name')
        self.assertIn("sortOrder", result['paging'])
        self.assertEquals(result['paging']['sortOrder'], 'DESCENDENT')

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_bad_sort_order(self, *args):
        url = "{}?{}={}&{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortBy", "name",
            "sortOrder", "XXX"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        error_msg = response.json().get("description")
        self.assertRegex(error_msg, "sortOrder must be ASCENDING or DESCENDING")

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_pagination_offset_without_limit(self, *args):
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "offset", '1'
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        self.assertIn("contracts", result)
        self.assertEquals(len(result["contracts"]), 2)
        self.assertEquals(result["contracts"][0]["id"], self.broadband_contract.id)
        self.assertIn("paging", result)
        self.assertIn("offset", result["paging"])
        self.assertEquals(result["paging"]["offset"], 1)
        self.assertIn("totalNumberOfRecords", result["paging"])
        self.assertEquals(result["paging"]["totalNumberOfRecords"], 3)

    @odoo.tools.mute_logger("odoo.addons.base_rest.http")
    def test_route_contract_search_partner_pagination_sort_order_without_by(self, *args):  # noqa
        url = "{}?{}={}&{}={}".format(
            self.url,
            "partner_vat", self.partner.vat,
            "sortOrder", "DESCENDENT"
        )
        response = self.http_get(url)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.reason, "BAD REQUEST")

    def test_route_contract_search_to_dict(self):
        result = ContractService(self.env)._to_dict(self.contract)

        self.assertEquals(result["id"], self.contract.id)
        self.assertEquals(result["code"], self.contract.code)
        self.assertEquals(result["customer_firstname"],
                          self.contract.partner_id.firstname)
        self.assertEquals(result["customer_lastname"],
                          self.contract.partner_id.lastname)
        self.assertEquals(result["customer_ref"], self.contract.partner_id.ref)
        self.assertEquals(result["customer_vat"], self.contract.partner_id.vat)
        self.assertEquals(result["phone_number"], self.contract.phone_number)
        self.assertEquals(
            result["current_tariff_product"],
            "SE_SC_REC_MOBILE_T_150_1024")
        self.assertEquals(result["ticket_number"], self.contract.ticket_number)
        self.assertEquals(result["technology"],
                          self.contract.service_technology_id.name)
        self.assertEquals(result["supplier"], self.contract.service_supplier_id.name)
        self.assertEquals(result["lang"], self.contract.lang)
        self.assertEquals(
            result["iban"],
            self.contract.mandate_id.partner_bank_id.sanitized_acc_number
        )
        self.assertEquals(result["is_terminated"], self.contract.is_terminated)
        self.assertEquals(result["date_start"], self.contract.date_start)
        self.assertEquals(result["date_end"], self.contract.date_end)
        self.assertEquals(result["fiber_signal"], "fibraFTTH")

    def test_route_contract_search_to_dict_subscription_type_mobile(self):
        self.url = "{}?{}={}".format(self.url, "code", self.contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.contract.id)
        self.assertEquals(result["contracts"][0]["subscription_type"], "mobile")

    def test_route_contract_search_to_dict_subscription_type_broadband(self):
        self.url = "{}?{}={}".format(self.url, "code", self.broadband_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.broadband_contract.id)
        self.assertEquals(result["contracts"][0]["subscription_type"], "broadband")

    def test_route_contract_search_to_dict_address(self):
        self.url = "{}?{}={}".format(self.url, "code", self.contract.code)
        response = self.http_get(self.url)
        result = json.loads(response.content.decode("utf-8"))
        self.assertEquals(
            result["contracts"][0]["address"]["street"], self.partner.street
        )
        self.assertEquals(result["contracts"][0]["address"]["city"], self.partner.city)
        self.assertEquals(
            result["contracts"][0]["address"]["zip_code"], self.partner.zip
        )

    def test_route_contract_search_to_dict_subscription_technology_mobile(self):
        self.url = "{}?{}={}".format(self.url, "code", self.contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.contract.id)
        self.assertEquals(result["contracts"][0]["subscription_technology"], "mobile")

    def test_route_contract_search_to_dict_subscription_technology_adsl(self):
        self.url = "{}?{}={}".format(self.url, "code", self.broadband_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.broadband_contract.id)
        self.assertEquals(result["contracts"][0]["subscription_technology"], "adsl")

    def test_route_contract_search_to_dict_subscription_technology_fiber(self):
        self.url = "{}?{}={}".format(self.url, "code", self.fiber_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.fiber_contract.id)
        self.assertEquals(result["contracts"][0]["subscription_technology"], "fiber")

    def test_route_contract_search_to_dict_available_operations_change_tariff_fiber_out_landline(  # noqa
        self,
    ):
        fiber_wo_fix = self.browse_ref("somconnexio.SenseFixFibra100Mb")
        fiber_wo_fix.without_fix = True
        self.fiber_contract.contract_line_ids.update({
            "product_id": fiber_wo_fix.id
        })
        self.url = "{}?{}={}".format(self.url, "code", self.fiber_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.fiber_contract.id)
        self.assertEquals(
            result["contracts"][0]["available_operations"],
            ["ChangeTariffFiberOutLandline"],
        )

    def test_route_contract_search_to_dict_available_operations_change_tariff_fiber_landline(  # noqa
        self,
    ):
        self.url = "{}?{}={}".format(self.url, "code", self.broadband_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.broadband_contract.id)
        self.assertEquals(
            result["contracts"][0]["available_operations"],
            ["ChangeTariffFiberLandline"],
        )

    def test_route_contract_search_to_dict_available_operations_change_tariff_mobile(  # noqa
        self,
    ):
        self.url = "{}?{}={}".format(self.url, "code", self.contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        self.assertEquals(result["contracts"][0]["id"], self.contract.id)
        self.assertEquals(
            result["contracts"][0]["available_operations"],
            ["ChangeTariffMobile", "AddOneShotMobile"],
        )

    def test_route_contract_search_to_dict_mobile_shared_bond(  # noqa
        self,
    ):
        shared_bond_id = "ABC123XYZ"
        shared_bond_contract = self.env["contract.contract"].create(
            {
                "name": "Test Contract Mobile",
                "partner_id": self.partner.id,
                "service_partner_id": self.partner.id,
                "invoice_partner_id": self.partner.id,
                "service_technology_id": self.ref(
                    "somconnexio.service_technology_mobile"
                ),
                "service_supplier_id": self.ref(
                    "somconnexio.service_supplier_masmovil"
                ),
                "mobile_contract_service_info_id": self.env[
                    "mobile.service.contract.info"
                ]
                .create(
                    {
                        "phone_number": self.phone_number,
                        "icc": "123",
                        "shared_bond_id": shared_bond_id,
                    }
                )
                .id,
                "contract_line_ids": [
                    (
                        0,
                        False,
                        {
                            "name": "Mobile",
                            "product_id": self.ref(
                                "somconnexio.50GBCompartides3mobils"
                            ),
                        },
                    )
                ],
                "mandate_id": self.mandate.id,
            }
        )
        shared_bond_contract.parent_pack_contract_id = self.fiber_contract.id

        self.url = "{}?{}={}".format(self.url, "code", shared_bond_contract.code)
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))

        contract = result["contracts"][0]
        self.assertEquals(contract["id"], shared_bond_contract.id)
        self.assertEquals(
            contract["available_operations"],
            ["AddOneShotMobile"],
        )
        self.assertEquals(
            contract["parent_contract"],
            self.fiber_contract.code,
        )
        self.assertEquals(
            contract["shared_bond_id"],
            shared_bond_id,
        )
        self.assertEquals(
            contract["price"],
            shared_bond_contract.current_tariff_product.with_context(
                pricelist=self.ref("somconnexio.pricelist_21_IVA")
            ).price,
        )
        self.assertFalse(contract["has_landline_phone"])

    def test_route_contract_search_to_dict_broadband_with_landline(  # noqa
        self,
    ):
        response = self.http_get(
            "{}?code={}".format(self.url, self.fiber_contract.code)
        )
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        contract = result["contracts"][0]

        self.assertTrue(contract["has_landline_phone"])
        self.assertEquals(contract["bandwidth"], 100)

    def test_route_contract_search_to_dict_description_translation(  # noqa
        self,
    ):
        response = self.http_get(
            "{}?code={}".format(self.url, self.broadband_contract.code)
        )
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        ca_contract = result["contracts"][0]

        self.broadband_contract.partner_id.lang = "es_ES"

        response = self.http_get(
            "{}?code={}".format(self.url, self.broadband_contract.code)
        )
        self.assertEquals(response.status_code, 200)
        result = json.loads(response.content.decode("utf-8"))
        es_contract = result["contracts"][0]

        self.assertEqual(ca_contract["description"], "ADSL 1000 min a fix")
        self.assertEqual(es_contract["description"], "ADSL 1000 min a fijo")
