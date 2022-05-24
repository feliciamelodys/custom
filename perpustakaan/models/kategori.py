from odoo import models, fields, api, _


class Kategori(models.Model):
    _name = 'perpus.kategori'
    _description = 'Master Kategori Buku'

    kode = fields.Char('Kode Kategori', size=10, required=True)
    name = fields.Char('Nama Kategori', size=100, required=True)

    #kode kategori harus unik
    _sql_constraints = [
        ('unique', 'unique(kode)', 'Kode Kategori Harus Unik')
    ]