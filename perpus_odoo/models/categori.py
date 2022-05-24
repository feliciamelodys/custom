from odoo import api, fields, models

class categori(models.Model):
        _name = 'categori'
        _deskripsi = 'categori buku'

        name = fields.Char(string='Nama Kategori')        
        

        
