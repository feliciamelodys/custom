from odoo import models, fields, api, _
from odoo.exceptions import UserError

class NamaBarang(models.Model):
    _name = 'maxtor.nama.barang'
    _description = 'Master Nama Barang'

    name = fields.Char('Nama Barang', size=100, required=True)

    # # Nama barang harus unik
    # _sql_constraints = [
    #     ('unique', 'unique(name)', 'Nama Barang Harus Unik')
    # ]