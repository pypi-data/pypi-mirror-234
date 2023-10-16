from odoo import models, fields, _


class CoopAgreement(models.Model):
    _name = 'coop.agreement'
    _description = "Cooperative agreement"
    _rec_name = 'code'
    _sql_constraints = [(
        'default_code_uniq',
        'unique (code)',
        _('The code must be unique')
    )]
    partner_id = fields.Many2one('res.partner',
                                 required=True,
                                 string='Cooperator')
    products = fields.Many2many(comodel_name='product.template',
                                string='Products',
                                required=True,
                                help="Products available for the partners sponsored"
                                " by that cooperative.")
    code = fields.Char(string='Code', required=True, copy=False)

    def copy(self, default=None):
        """
        Duplicate record with given id updating it with default values
        :param default: (type: dictionary) field values to override the
                        original values of the copied record
        """
        if not default:
            default = {}
        default.update({'code': 'new code'})
        return super(CoopAgreement, self).copy(default=default)
