from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contract_type = fields.Char(string="Contract type")