from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Buku(models.Model):
    _name = 'perpus.buku'
    _description = 'Master Buku'

    kode = fields.Char('Kode Buku', size=64, required=True,default="New")
    name = fields.Char('Judul Buku', size=100, required=True)
    penerbit = fields.Many2one('res.partner', 'Penerbit', required=True, domain=[('is_penerbit','=',True)], context="{'default_is_penerbit': True}")
    pengarang = fields.Many2one('res.partner', 'Pengarang', required=True, domain=[('is_pengarang', '=', True)], context="{'default_is_pengarang': True}")
    tahun = fields.Char('Tahun', size=4, required=True, index=True)
    state = fields.Selection([('available', 'Available'),
                               ('non_available', 'Non Avalaible')], 'Status', readonly=False, default='available')
    kategori_id = fields.Many2one(comodel_name='perpus.kategori', string='Kategori', required=True)
    harga = fields.Integer('Harga', default=10_000, required=True)

   #kode buku tidak boleh sama
    _sql_constraints = [
        ('unique', 'unique(kode)', 'Kode Buku harus Unik')
    ]

    def tes_buku(self):
        print("ini di buku")
        t = self.env.context.get("keterangan")
        print(t)

    @api.model_create_multi
    def create(self,vals_list):  # ketika action save diklik akan muncul number otomatis, kita melakukan overwrite button save yang sudah ada di Odoo
        if self.kode == 'New' or not self.kode:
            seq = self.env['ir.sequence'].search([("code", "=", "perpus.buku")])
            if not seq:
                raise UserError(_('perpus.buku sequence not found, please create perpus.buku sequence'))
        for val in vals_list:
            val['kode'] = seq.next_by_id()

        return super(Buku, self).create(vals_list)  # Buku yang ada di super ini nama class

