from faker import Faker
from datetime import datetime, timedelta
import random

faker = Faker("es_CA")


def random_icc(odoo_env):
    icc_prefix = odoo_env['ir.config_parameter'].get_param(
        'somconnexio.icc_start_sequence'
    )
    random_part = [
        str(random.randint(0, 9))
        for _ in range(19-len(icc_prefix))
    ]
    return icc_prefix + "".join(random_part)


def random_ref():
    return str(random.randint(0, 99999))


def random_mobile_phone():
    """
    Returns a random 9 digit number starting with either 6 or 7
    """
    return str(random.randint(6, 7)) + str(random.randint(10000000, 99999999))


def random_landline_number():
    """
    Returns a random 9 digit number starting with either 8 or 9
    """
    return str(random.randint(8, 9)) + str(random.randint(10000000, 99999999))


def subscription_request_create_data(odoo_env):
    return {
        "partner_id": 0,
        "already_cooperator": False,
        "is_company": False,
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "email": faker.email(),
        "ordered_parts": 1,
        "share_product_id": odoo_env.browse_ref(
            "easy_my_coop.product_template_share_type_2_demo"
        ).product_variant_id.id,
        "address": faker.street_address(),
        "city": faker.city(),
        "zip_code": faker.postcode(),
        "country_id": odoo_env.ref("base.es"),
        "date": datetime.now() - timedelta(days=12),
        "company_id": 1,
        "source": "manual",
        "lang": random.choice(["es_ES", "ca_ES"]),
        "sponsor_id": False,
        "vat": faker.vat_id(),
        "discovery_channel_id": odoo_env.browse_ref(
            "somconnexio.other_cooperatives"
        ).id,
        "iban": faker.iban(),
        "state": "draft",
    }


def partner_create_data(odoo_env):
    return {
        "parent_id": False,
        "name": faker.name(),
        "email": faker.email(),
        "street": faker.street_address(),
        "street2": faker.street_address(),
        "city": faker.city(),
        "zip_code": faker.postcode(),
        "country_id": odoo_env.ref("base.es"),
        "state_id": odoo_env.ref("base.state_es_b"),
        "customer": True,
        "ref": random_ref(),
        "lang": random.choice(["es_ES", "ca_ES"]),
    }


def crm_lead_line_create(
    odoo_env, service_category, portability, shared_bond_id="ABC1234"
):
    product_switcher = {
        "mobile": odoo_env.ref("somconnexio.TrucadesIllimitades20GB"),
        "pack": odoo_env.ref("somconnexio.TrucadesIllimitades20GBPack"),
        "shared_data": odoo_env.ref("somconnexio.50GBCompartides2mobils"),
        "fiber": odoo_env.ref("somconnexio.Fibra100Mb"),
        "adsl": odoo_env.ref("somconnexio.ADSL20MBSenseFix"),
        "4G": odoo_env.ref("somconnexio.Router4G"),
    }
    base_isp_info_args = (
        {
            "type": "portability",
            "previous_contract_type": "contract",
            "previous_provider": odoo_env.ref("somconnexio.previousprovider39").id,
            "previous_owner_vat_number": faker.vat_id(),
            "previous_owner_name": faker.first_name(),
            "previous_owner_first_name": faker.last_name(),
        }
        if portability
        else {"type": "new"}
    )
    base_ba_isp_info_args = {
        "service_full_street": faker.address(),
        "service_city": faker.city(),
        "service_zip_code": "08015",
        "service_state_id": odoo_env.ref("base.state_es_b").id,
        "service_country_id": odoo_env.ref("base.es").id,
    }

    isp_info_args_switcher = {
        "mobile": {"phone_number": random_mobile_phone(), "icc": random_icc(odoo_env)},
        "pack": {"phone_number": random_mobile_phone(), "icc": random_icc(odoo_env)},
        "shared_data": {
            "phone_number": random_mobile_phone(),
            "shared_bond_id": shared_bond_id,
        },
        "fiber": dict(**base_ba_isp_info_args, phone_number=random_landline_number()),
        "adsl": dict(**base_ba_isp_info_args, phone_number=random_landline_number()),
        "4G": dict(**base_ba_isp_info_args, phone_number="-"),
    }
    model_switcher = {
        "mobile": "mobile.isp.info",
        "pack": "mobile.isp.info",
        "shared_data": "mobile.isp.info",
        "fiber": "broadband.isp.info",
        "adsl": "broadband.isp.info",
        "4G": "broadband.isp.info",
    }
    isp_info = odoo_env[model_switcher[service_category]].create(
        dict(**base_isp_info_args, **isp_info_args_switcher[service_category])
    )
    crm_lead_line_args = {
        "name": "CRM Lead",
        "product_id": product_switcher[service_category].id,
    }
    if service_category in ["fiber", "adsl", "4G"]:
        crm_lead_line_args.update(
            {
                "broadband_isp_info": isp_info.id,
            }
        )
    else:
        crm_lead_line_args.update(
            {
                "mobile_isp_info": isp_info.id,
            }
        )

    return odoo_env["crm.lead.line"].create(crm_lead_line_args)


def crm_lead_create(
    odoo_env,
    partner_id,
    service_category,
    portability=False,
):
    if service_category in ["mobile", "fiber", "adsl", "4G"]:
        crm_lead_line_ids = [
            crm_lead_line_create(odoo_env, service_category, portability).id,
        ]
    elif service_category == "pack":
        crm_lead_line_ids = [
            crm_lead_line_create(odoo_env, "fiber", portability).id,
            crm_lead_line_create(odoo_env, service_category, portability).id,
        ]
    elif service_category == "shared_data":
        crm_lead_line_ids = [
            crm_lead_line_create(odoo_env, "fiber", portability).id,
            crm_lead_line_create(odoo_env, service_category, portability).id,
            crm_lead_line_create(odoo_env, service_category, portability).id,
        ]
    return odoo_env["crm.lead"].create(
        {
            "name": "Test Lead",
            "partner_id": partner_id.id,
            "iban": partner_id.bank_ids[0].sanitized_acc_number,
            "lead_line_ids": [(6, 0, crm_lead_line_ids)],
            "stage_id": odoo_env.ref("crm.stage_lead1").id,
        }
    )


def _mobil_service_product_create_data(odoo_env):
    return {
        "name": "Sense minutes",
        "type": "service",
        "categ_id": odoo_env.ref("somconnexio.mobile_service").id,
    }


def _fiber_service_product_create_data(odoo_env):
    return {
        "name": "Fiber 200 Mb",
        "type": "service",
        "categ_id": odoo_env.ref("somconnexio.broadband_fiber_service").id,
    }


def _adsl_service_product_create_data(odoo_env):
    return {
        "name": "ADSL 20Mb",
        "type": "service",
        "categ_id": odoo_env.ref("somconnexio.broadband_adsl_service").id,
    }


def _4G_service_product_create_data(odoo_env):
    return {
        "name": "Router 4G",
        "type": "service",
        "categ_id": odoo_env.ref("somconnexio.broadband_4G_service").id,
    }
