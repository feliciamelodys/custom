from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    nama_barang_id = fields.Many2one('maxtor.nama.barang', string="Nama")
    merk_id = fields.Many2one("maxtor.merk", string="Merk")
    stock = fields.Integer("Stok Tersedia", store=True)

    #Function untuk memberikan nama barang dimana nama barang didapat dari nama_barang + merk
    @api.onchange('nama_barang_id', 'merk_id')
    def onchange_name(self):
        nama_barang = self.nama_barang_id.name or ''
        merk = self.merk_id.name or ''
        self.name = nama_barang + ' ' + merk



    #Sequence Barcode Product
    @api.model
    def create(self, vals):
        vals['barcode'] = self.env['ir.sequence'].next_by_code('product.barcode')
        return super(ProductTemplate, self).create(vals)
