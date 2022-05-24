from odoo import api, fields, models


class propinsi(models.Model):
    _name = 'ref_propinsi'
    _description = 'Tabel Propinsi'

    name = fields.Char(string='Nama Propinsi')
    singkatan = fields.Char(string='Singkatan')
    deskripsi = fields.Char(string='Deskripsi')
    kota_ids = fields.One2many(comodel_name='ref_kota', inverse_name='propinsi_id', string='Kota')
    


class kota(models.Model):
    _name = 'ref_kota'
    _description = 'Tabel Kota'

    name = fields.Char(string='Nama Kota')
    singkatan = fields.Char(string='singkatan')
    deskripsi = fields.Char(string='deskripsi')
    propinsi_id = fields.Many2one(comodel_name='ref_propinsi', string='Nama propinsi')
    kecamatan_ids = fields.One2many(comodel_name='ref_kecamatan', inverse_name='kota_id', string='Kecamatan')
    


class kecamatan(models.Model):
    _name = 'ref_kecamatan'
    _description = 'Tabel Kecamatan'

    name = fields.Char(string='Nama Kecamatan')
    singkatan = fields.Char(string='Kecamatan')
    deskripsi = fields.Char(string='deskripsi')
    kota_id = fields.Many2one(comodel_name='ref_kota', string='Nama Kota')
    
   
    
    
   

    
    
