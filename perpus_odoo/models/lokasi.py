from odoo import api, fields, models

class lokasi(models.Model):
    _name = 'lokasi'
    _description = 'lokasi buku'

    name = fields.Char(string='name')
    lokasi = fields.One2many(comodel_name='lokasi', inverse_name='lokasi', string='Lokasi')
    buku = fields.Many2many(comodel_name='buku', string='Buku')