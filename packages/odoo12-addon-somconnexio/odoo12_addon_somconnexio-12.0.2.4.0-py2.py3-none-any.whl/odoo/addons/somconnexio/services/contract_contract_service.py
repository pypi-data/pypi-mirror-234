from odoo import _
from odoo.addons.base_rest.http import wrapJsonException
from odoo.exceptions import MissingError
from otrs_somconnexio.otrs_models.configurations.changes.change_tariff import (
    ChangeTariffSharedBondTicketConfiguration,
    ChangeTariffTicketConfiguration,
)
from otrs_somconnexio.services.search_tickets_service import SearchTicketsService
from werkzeug.exceptions import BadRequest

from .res_partner_service import AddressService


class ContractService:
    def __init__(self, env):
        self.env = env
        self.Contract = self.env["contract.contract"]

    def search(self, **params):
        code = params.get("code")
        phone_number = params.get("phone_number")
        partner_vat = params.get("partner_vat")
        limit = params.get("limit", 10)
        offset = params.get("offset", 0)
        sortBy = params.get("sortBy", "")
        sortOrder = params.get("sortOrder", "")
        customer_ref = params.get("customer_ref", "")
        if limit:
            if isinstance(limit, int) or isinstance(limit, str) and limit.isdigit():
                limit = int(limit)
            else:
                raise wrapJsonException(
                    BadRequest("Limit must be numeric"),
                    include_description=True,
                )
        if offset:
            if isinstance(offset, int) or isinstance(offset, str) and offset.isdigit():
                offset = int(offset)
            else:
                raise wrapJsonException(
                    BadRequest("Offset must be numeric"),
                    include_description=True,
                )
        if sortBy:
            if sortBy not in self.env["contract.contract"].fields_get():
                raise wrapJsonException(
                    BadRequest("Invalid field to sortBy"), include_description=True
                )
        if sortOrder:
            if sortOrder == "ASCENDENT":
                pass
            elif sortOrder == "DESCENDENT":
                sortOrder = " DESC"
            else:
                raise wrapJsonException(
                    BadRequest("sortOrder must be ASCENDING or DESCENDING"),
                    include_description=True,
                )

        if code:
            domain = [("code", "=", code)]
            search_param = "code"
        elif customer_ref:
            domain = [("partner_id.ref", "=", customer_ref)]
            search_param = "customer_ref"
        elif phone_number:
            domain = [("phone_number", "=", phone_number)]
            search_param = "phone_number"
        elif partner_vat:
            domain = [
                ("partner_id.vat", "=", partner_vat),
                ("partner_id.parent_id", "=", False),
            ]
            search_param = "partner_vat"
        domain += [("is_terminated", "=", False)]
        contracts = self.Contract.sudo().search(
            domain, limit=limit, offset=offset, order=sortBy + sortOrder
        )
        if not contracts:
            raise MissingError(
                _('No contract with {}: {} could be found'.format(
                    search_param, params.get(search_param)))
                )

        ret = {"contracts": [self._to_dict(contract) for contract in contracts]}
        if limit or offset or sortBy:
            ret["paging"] = {
                "limit": limit,
                "offset": offset,
                "totalNumberOfRecords": self.Contract.sudo().search_count(domain),
            }
            if sortBy:
                ret["paging"].update(
                    {
                        "sortBy": sortBy,
                        "sortOrder": "DESCENDENT"
                        if sortOrder == " DESC"
                        else "ASCENDENT",
                    }
                )
        return ret

    def create(self, **params):
        self.Contract.with_delay().create_contract(**params)
        return {"result": "OK"}

    def count(self):
        domain_contracts = [('is_terminated', '=', False)]
        domain_members = [
            ('parent_id', '=', False), ('customer', '=', True),
            '|', ('member', '=', True), ('coop_candidate', '=', True)
        ]
        number = self.Contract.sudo().search_count(domain_contracts)
        result = {"contracts": number}
        number = self.env['res.partner'].sudo().search_count(domain_members)
        result['members'] = number
        return result

    def get_fiber_contracts_to_pack(self, **params):
        """
        Returns all contracts from the requested that match these
        conditions:
        - Own by requested partner (ref)
        - Supplier MM
        - Technology fiber
        - Not in pack (if not mobiles_sharing_data)
        """

        partner_ref = params.get('partner_ref')

        partner = self.env['res.partner'].sudo().search([
            ('parent_id', '=', False),
            ('ref', '=', partner_ref)
        ])

        if not partner:
            raise MissingError(
                "Partner with ref {} not found".format(
                    partner_ref)
                )

        contracts = self.Contract.sudo().search(
            [
                ("partner_id", "=", partner.id),
                ("is_terminated", "=", False),
                (
                    "service_technology_id",
                    "=",
                    self.env.ref("somconnexio.service_technology_fiber").id,
                ),
            ]
        )
        if params.get('mobiles_sharing_data') == 'true':
            contracts = contracts.filtered(
                lambda c: len(c.children_pack_contract_ids) == 1
                or not c.children_pack_contract_ids
            )
        else:
            contracts = contracts.filtered(
                lambda c: not c.children_pack_contract_ids
            )

        contracts = self._filter_out_fibers_used_in_OTRS_tickets(contracts)
        contracts = self._filter_out_fibers_used_in_ODOO_lead_lines(contracts)

        if not contracts:
            raise MissingError(
                _("No fiber contracts available to pack found with this user")
            )

        result = [self._to_dict(contract) for contract in contracts]

        return result

    def _to_dict(self, contract):
        contract.ensure_one()

        fiber_signal = contract.fiber_signal_type_id and \
            contract.fiber_signal_type_id.code or False

        return {
            "id": contract.id,
            "code": contract.code,
            "email": contract.partner_id.email,
            "customer_firstname": contract.partner_id.firstname,
            "customer_lastname": contract.partner_id.lastname,
            "customer_ref": contract.partner_id.ref,
            "customer_vat": contract.partner_id.vat,
            "phone_number": contract.phone_number,
            "current_tariff_product": contract.current_tariff_product.default_code,
            "description": contract.current_tariff_product.with_context(
                lang=contract.lang
            ).custom_name,
            "ticket_number": contract.ticket_number,
            "technology": contract.service_technology_id.name,
            "supplier": contract.service_supplier_id.name,
            "lang": contract.lang,
            "iban": contract.mandate_id.partner_bank_id.sanitized_acc_number,
            "is_terminated": contract.is_terminated,
            "date_start": contract.date_start,
            "date_end": contract.date_end,
            "fiber_signal": fiber_signal,
            "subscription_type": (
                "mobile" if contract.service_contract_type == "mobile" else "broadband"
            ),
            "address": AddressService(self.env, contract.service_partner_id).__dict__,
            "subscription_technology": (
                contract.service_contract_type
                if contract.service_contract_type in (
                    "adsl", "mobile"
                )
                else "fiber"
            ),
            "available_operations": self._available_operations(contract),
            "parent_contract": contract.parent_pack_contract_id.code
            if contract.parent_pack_contract_id
            else "",
            "shared_bond_id": contract.shared_bond_id,
            "price": self._product_price(contract.current_tariff_product),
            "has_landline_phone": not bool(contract.current_tariff_product.without_fix)
            if contract.service_contract_type != "mobile"
            else False,
            "bandwidth": int(
                contract.current_tariff_product.without_lang().get_catalog_name(
                    "Bandwidth"
                )
                or 0
            ),
        }

    def _available_operations(self, contract):
        if contract.service_contract_type == "mobile":
            if contract.shared_bond_id:
                return ["AddOneShotMobile"]
            else:
                return ["ChangeTariffMobile", "AddOneShotMobile"]
        elif contract.current_tariff_product.without_fix:
            return ["ChangeTariffFiberOutLandline"]
        elif contract.service_contract_type == "adsl":
            return ["ChangeTariffFiberLandline"]
        return []

    def _filter_out_fibers_used_in_OTRS_tickets(self, contracts):
        """
        From a list of fiber contracts, search if any of their codes are
        already referenced in OTRS new mobile change tariff tickets
        (DF OdooContractRefRelacionat).
        If so, that fiber contract is about to be linked to a mobile offer,
        and shouldn't be available for others.
        Returns the original contract list excluding, if found,
        those referenced in OTRS.
        """

        if not contracts:
            return []

        partner = contracts[0].partner_id
        service = SearchTicketsService(
            [
                ChangeTariffTicketConfiguration,
                ChangeTariffSharedBondTicketConfiguration,
            ]
        )
        df_dct = {"OdooContractRefRelacionat": [c.code for c in contracts]}
        tickets_found = service.search(partner.ref, df_dct=df_dct)

        fiber_contracts_used_otrs = []
        for ticket in tickets_found:
            # Review: https://git.coopdevs.org/coopdevs/som-connexio/otrs-somconnexio/-/issues/6  # noqa
            code = ticket.response.dynamic_field_get("OdooContractRefRelacionat").value
            fiber_contracts_used_otrs.append(code)

        return contracts.filtered(lambda c: c.code not in fiber_contracts_used_otrs)

    def _filter_out_fibers_used_in_ODOO_lead_lines(self, contracts):
        """
        From a list of fiber contracts, search if any of them is
        already referenced in a mobile provisioning crm lead line
        (field `linked_fiber_contract_id`).
        If so, that fiber contract is about to be linked to a mobile
        offer, and shouldn't be available for others.
        Returns the original contract list excluding, if found,
        those linked in mobile lead lines.
        """

        if not contracts:
            return []

        stages_to_discard = [
            self.env.ref('crm.stage_lead4').id,
            self.env.ref('somconnexio.stage_lead5').id,
        ]
        partner_id = contracts[0].partner_id.id
        mbl_lead_lines = self.env["crm.lead.line"].search([
            ('partner_id', '=', partner_id),
            ('mobile_isp_info', '!=', False),
            ('stage_id', 'not in', stages_to_discard)
        ])

        already_linked_contracts = mbl_lead_lines.mapped(
            'mobile_isp_info').mapped('linked_fiber_contract_id')

        return contracts - already_linked_contracts

    def _product_price(self, product):
        pricelist_id = self.env["product.pricelist"].search([("code", "=", "21IVA")])
        return product.with_context(pricelist=pricelist_id.id).price
