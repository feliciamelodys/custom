from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    nama_barang_id = fields.Many2one('maxtor.nama.barang', string="Nama")
    merk_id = fields.Many2one("maxtor.merk", string="Merk")
    stock = fields.Float("Qty", digits='Discount')

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

    def edit_stock(self):
        return {
            'name': "Product Update Stock",
            'type': 'ir.actions.act_window',
            'res_model': 'maxtor.product.update.stock.wizard',
            'context': {'default_product_id': self.id},
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }


class ProductUpdateStock(models.TransientModel):
    _name = 'maxtor.product.update.stock.wizard'

    product_id = fields.Many2one('product.product', 'Product')
    qty = fields.Float("Qty", digits='Discount')

    def update(self):
        for o in self:
            p = self.env['product.product'].search([('id', '=', o.product_id.id)])
            p.write({'stock': o.qty})