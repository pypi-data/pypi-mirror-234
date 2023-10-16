from odoo.addons.base_iban.models.res_partner_bank import \
    normalize_iban, pretty_iban, _map_iban_template


class BankFromIbanGetter:

    def __init__(self, env, iban):
        self.iban = iban
        self.env = env

    def get_bank(self):
        # Code copied from base_bank_from_iban module:
        # https://github.com/OCA/community-data-files/blob/12.0/base_bank_from_iban/models/res_partner_bank.py#L13  # noqa
        acc_number = pretty_iban(normalize_iban(self.iban)).upper()
        country_code = acc_number[:2].lower()
        iban_template = _map_iban_template[country_code]
        first_match = iban_template[2:].find('B') + 2
        last_match = iban_template.rfind('B') + 1
        bank_code = acc_number[first_match:last_match].replace(' ', '')
        bank = self.env['res.bank'].sudo().search([
            ('code', '=', bank_code),
            ('country.code', '=', country_code.upper()),
        ], limit=1)
        return bank
