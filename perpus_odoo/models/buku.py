from odoo import api, fields, models


class buku(models.Model):
    _name = 'buku'
    _description = 'tabel buku'

    name = fields.Char(string='Judul Buku')
    image = fields.Binary(string='Cover')
    jumlah = fields.Integer(string='Jumlah Buku')
    pengarang = fields.Many2one(comodel_name='pengarang', string='Nama Pengarang')
    deskripsi = fields.Text(string='Deskripsi')
    categori = fields.Many2many(comodel_name='categori', string='Kategori')
    lokasi = fields.Many2one(comodel_name='lokasi', string='Lokasi')
    state = fields.Selection([('available', 'TERSEDIA'), ('rent', 'DISEWA')], 'State', readonly=True, default='available')

  
    
    
    
    