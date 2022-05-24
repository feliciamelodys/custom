from odoo import api, fields, models


class pengarang(models.Model):
    _name = 'pengarang'
    _description = 'Tabel pengarang'

    name = fields.Char(string='Nama pengarang')
    jenis_kel = fields.Selection(string='Jenis kelamin', selection=[('L', 'Laki-laki'), ('P', 'Perempuan'),], default='L')
    tgl_lahir = fields.Date(string='Tanggal lahir')
    tmp_lahir = fields.Char(string='Tempat lahir')
    agama = fields.Selection(string='Agama', selection=[('islam', 'Islam'), ('kristen', 'Kristen'), ('hindu', 'Hindu'), ('budha', 'Budha'), ('lain', 'Lainnya'),], default='islam')
    image = fields.Binary(string='Foto')    

    
    
