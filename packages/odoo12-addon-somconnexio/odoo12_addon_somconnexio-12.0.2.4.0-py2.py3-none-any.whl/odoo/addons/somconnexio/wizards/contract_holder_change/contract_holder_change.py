from datetime import date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import MissingError

from ...services.contract_contract_service import ContractService


class ContractHolderChangeWizard(models.TransientModel):
    _name = 'contract.holder.change.wizard'
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
    )
    contract_id = fields.Many2one('contract.contract')
    change_date = fields.Date('Change Date', required=True)
    payment_mode = fields.Many2one(
        'account.payment.mode',
        string='Payment mode',
        required=True,
    )
    banking_mandate_required = fields.Boolean(
        related="payment_mode.payment_method_id.bank_account_required"
    )
    available_banking_mandates = fields.Many2many(
        'account.banking.mandate',
        compute="_compute_available_banking_mandates"
    )
    banking_mandate_id = fields.Many2one(
        'account.banking.mandate',
        string='Banking mandate',
    )
    email_ids = fields.Many2many(
        'res.partner',
        string='Emails',
        required=True,
    )
    available_email_ids = fields.Many2many(
        "res.partner", string="Available Emails", compute="_compute_available_email_ids"
    )
    notes = fields.Text(
        string='Notes',
    )
    has_mobile_pack_offer_text = fields.Selection(
        [("yes", _("Yes")), ("no", "No")],
        string="Is mobile pack offer available?",
        compute="_compute_has_mobile_pack_offer_text",
        readonly=True,
    )
    available_products = fields.Many2many(
        "product.product",
        compute="_compute_available_products",
    )
    fiber_contract_to_link = fields.Many2one(
        "contract.contract",
        string="Fiber contract to link",
        compute="_compute_fiber_contract_to_link"
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults["contract_id"] = self.env.context["active_id"]
        contract = self.env["contract.contract"].browse(self.env.context["active_id"])
        defaults["payment_mode"] = self.env.ref(
            "somconnexio.payment_mode_inbound_sepa"
        ).id
        defaults["change_date"] = date.today()
        defaults["product_id"] = contract.current_tariff_product.id
        return defaults

    @api.depends("partner_id")
    def _compute_available_email_ids(self):
        if self.partner_id:
            self.available_email_ids = [
                (6, 0, self.partner_id.get_available_email_ids())
            ]

    @api.multi
    @api.depends("partner_id")
    def _compute_available_banking_mandates(self):
        if self.partner_id:
            partner_mandates = self.env['account.banking.mandate'].search([
                ('partner_id', '=', self.partner_id.id),
            ])
            self.available_banking_mandates = partner_mandates

    @api.multi
    @api.depends("partner_id")
    def _compute_fiber_contract_to_link(self):
        if self.partner_id:
            service = ContractService(self.env)
            try:
                fiber_contracts = service.get_fiber_contracts_to_pack(
                    partner_ref=self.partner_id.ref
                )
            except MissingError:
                self.fiber_contract_to_link = False
            else:
                self.fiber_contract_to_link = fiber_contracts[0]["id"]

    @api.depends("fiber_contract_to_link")
    def _compute_has_mobile_pack_offer_text(self):
        self.has_mobile_pack_offer_text = "yes" if self.fiber_contract_to_link else "no"

    @api.depends("fiber_contract_to_link")
    def _compute_available_products(self):
        old_contract_category = (
            self.contract_id.current_tariff_product.product_tmpl_id.categ_id
        )
        product_templates = self.env["product.template"].search(
            [
                ("categ_id", "=", old_contract_category.id),
            ]
        )
        product_search_domain = [
            ("product_tmpl_id", "in", product_templates.ids),
            ("public", "=", "True"),
        ]
        if (
            old_contract_category == self.env.ref('somconnexio.mobile_service')
            and self.fiber_contract_to_link
                ):
            product_search_domain = product_search_domain[:-1]
            product_search_domain.extend(
                [
                    "|",
                    (
                        "attribute_value_ids",
                        "=",
                        self.env.ref("somconnexio.IsInPack").id,
                    ),
                    ("public", "=", "True"),
                ]
            )
        self.available_products = self.env['product.product'].search(
            product_search_domain
        )

    @api.multi
    def button_change(self):
        self.ensure_one()
        crm_lead_line = self._create_new_crm_lead_line()
        new_contract = self._create_new_contract(crm_lead_line)
        self._terminate_contract(new_contract)
        return True

    def _get_or_create_service_partner_id(self):

        service_partner = self.env['res.partner'].search([
            ('parent_id', '=', self.partner_id.id),
            ('type', '=', 'service'),
            ('street', 'ilike', self.contract_id.service_partner_id.street),
        ], limit=1)

        if not service_partner:
            service_partner = self.env['res.partner'].create({
                'parent_id': self.partner_id.id,
                'name': 'New partner service',
                'type': 'service',
                'street': self.contract_id.service_partner_id.street,
                'street2': self.contract_id.service_partner_id.street2,
                'city': self.contract_id.service_partner_id.city,
                'zip': self.contract_id.service_partner_id.zip,
                'state_id': self.contract_id.service_partner_id.state_id.id,
                'country_id': self.contract_id.service_partner_id.country_id.id,
            })

        return service_partner

    def _create_new_crm_lead_line(self):
        isp_info_params = {
            "type": "holder_change",
            "phone_number": self.contract_id.phone_number,
        }
        line_params = {
            "name": self.contract_id.current_tariff_product.name,
            "product_id": self.product_id.id,
            "product_tmpl_id": self.contract_id.current_tariff_product.product_tmpl_id.id,  # noqa
            "category_id": self.contract_id.current_tariff_product.product_tmpl_id.categ_id.id,  # noqa
        }
        if self.contract_id.is_broadband:
            broadband_isp_info = self.env["broadband.isp.info"].create(isp_info_params)
            line_params.update({"broadband_isp_info": broadband_isp_info.id})
        else:
            if (self.contract_id.is_mobile and self.fiber_contract_to_link and
                    self.product_id.product_is_pack_exclusive):
                isp_info_params[
                    "linked_fiber_contract_id"
                ] = self.fiber_contract_to_link.id
            mobile_isp_info = self.env["mobile.isp.info"].create(isp_info_params)
            line_params.update({"mobile_isp_info": mobile_isp_info.id})

        crm_lead_line = self.env["crm.lead.line"].create(line_params)

        self.env['crm.lead'].create({
            "name": _("Change Holder process"),
            "description": self.notes,
            "partner_id": self.partner_id.id,
            "lead_line_ids": [(6, 0, [crm_lead_line.id])],
            "iban": self.banking_mandate_id.partner_bank_id.sanitized_acc_number,
            "stage_id": self.env.ref("crm.stage_lead4").id
        })
        return crm_lead_line

    def _create_new_contract(self, crm_lead_line):
        service_partner = self._get_or_create_service_partner_id()
        new_contract_params = {
            'partner_id': self.partner_id.id,
            'service_partner_id': service_partner.id,
            'payment_mode_id': self.payment_mode.id,
            'mandate_id': self.banking_mandate_id.id,
            'email_ids': [(6, 0, [email.id for email in self.email_ids])],
            'journal_id': self.contract_id.journal_id.id,
            'service_technology_id': self.contract_id.service_technology_id.id,
            'service_supplier_id': self.contract_id.service_supplier_id.id,
            'contract_line_ids': [
                (0, 0, self._prepare_create_line(line))
                for line in self.contract_id.contract_line_ids
                if (
                    (not line.date_end or line.date_end > date.today()) and
                    line.product_id.categ_id not in (
                        self.env.ref('somconnexio.mobile_oneshot_service'),
                        self.env.ref('somconnexio.broadband_oneshot_service'),
                        self.env.ref('somconnexio.broadband_oneshot_adsl_service'),
                    )
                )
            ],
            'crm_lead_line_id': crm_lead_line.id,
        }

        # TODO: This code is duplicated in ContractServiceProcess
        if self.contract_id.mobile_contract_service_info_id:
            name_contract_info = "mobile_contract_service_info_id"
        elif self.contract_id.adsl_service_contract_info_id:
            name_contract_info = "adsl_service_contract_info_id"
        elif self.contract_id.vodafone_fiber_service_contract_info_id:
            name_contract_info = "vodafone_fiber_service_contract_info_id"
        elif self.contract_id.mm_fiber_service_contract_info_id:
            name_contract_info = "mm_fiber_service_contract_info_id"
        elif self.contract_id.router_4G_service_contract_info_id:
            name_contract_info = "router_4G_service_contract_info_id"
        contract_info = getattr(self.contract_id, name_contract_info)
        new_contract_params["name"] = contract_info.phone_number
        new_contract_params[name_contract_info] = contract_info.copy().id

        if (self.contract_id.is_mobile and self.fiber_contract_to_link and
                self.product_id.product_is_pack_exclusive):
            new_contract_params[
                "parent_pack_contract_id"
            ] = self.fiber_contract_to_link.id
        return self.env["contract.contract"].create(new_contract_params)

    def _terminate_contract(self, new_contract):
        self.contract_id.terminate_contract(
            self.env.ref('somconnexio.reason_holder_change'),
            'New contract created with ID: {}\nNotes: {}'.format(
                new_contract.id,
                self.notes or ''
            ),
            self.change_date,
            self.env.ref('somconnexio.user_reason_other'),
        )

        message = _("""
            Holder change wizard
            New contract created with ID: {}
            Notes: {}
            """)
        self.contract_id.message_post(
            message.format(new_contract.id, self.notes or '')
        )

    def _prepare_create_line(self, line):
        return {
            "name": self.product_id.name,
            "product_id": self.product_id.id,
            "date_start": self.change_date + timedelta(days=1),
        }

    @api.onchange('partner_id')
    def check_partner_id_change(self):
        self.service_partner_id = False
        self.bank_id = False
        self.email_ids = False

        if not self.partner_id:
            partner_id_domain = []
            bank_domain = []
        else:
            partner_id_domain = [
                '|',
                ('id', '=', self.partner_id.id),
                ('parent_id', '=', self.partner_id.id)
            ]
            bank_domain = [
                ('partner_id', '=', self.partner_id.id)
            ]

        return {
            'domain': {
                'service_partner_id': partner_id_domain,
                'bank_id': bank_domain
            }
        }
