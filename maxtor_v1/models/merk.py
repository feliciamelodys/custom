from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Merk(models.Model):
    _name = 'maxtor.merk'
    _description = 'Master Merk'

    name = fields.Char('Merk', size=100, required=True)

    # # Nama merk harus unik
    # _sql_constraints = [
    #     ('unique', 'unique(name)', 'Merk Harus Unik')
    # ]