from odoo import api, fields, models


class anggota(models.Model):
    _name = 'anggota'
    _description = 'anggota perpus'

    name = fields.Char(string='Nama Anggota')
    no_anggota = fields.Char(string='No Anggota',Required=True , readonly=True, Default='Auto')
    tmp_lahir = fields.Char(string='Tempat Lahir')
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    alamat = fields.Char(string='Alamat')
    no_telp = fields.Char(string='Nomor Telp')
    email = fields.Char(string='Email')
    agama = fields.Selection(string='Agama', selection=[('islam', 'Islam'), ('kristen', 'Kristen'), ('hindu', 'Hindu'), ('budha', 'Budha'), ('lain', 'Lainnya'),], default='islam')
    jenis_kel = fields.Selection(string='Jenis kelamin', selection=[('L', 'laki-laki'), ('P', 'Perempuan'),], default='L')
    propinsi_id = fields.Many2one(comodel_name='ref_propinsi', string='Propinsi')
    kota_id = fields.Many2one(comodel_name='ref_kota', string='Kota')
    kecamatan_id = fields.Many2one(comodel_name='ref_kecamatan', string='Kecamatan')
    image = fields.Binary(string='Foto')
    

    _sql_constraints = [
        ('no_anggota_unique',
        'unique(no_anggota)',
        'Maaf,Nomor Anggota tersebut sudah ada')
    ]

    @api.model
    def create(self, vals):
        vals['no_anggota'] = self.env['ir.sequence'].next_by_code('anggota')
        return super(anggota, self).create(vals)

