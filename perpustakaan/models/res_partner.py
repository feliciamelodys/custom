from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner' #inherit dari res.partner odoo

    is_penerbit = fields.Boolean('Is Penerbit')
    is_pengarang = fields.Boolean('Is Pengarang')
    is_customer = fields.Boolean('Is Customer')