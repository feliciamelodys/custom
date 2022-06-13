from odoo import models, fields, api, exceptions,_
from odoo.exceptions import UserError


class Penjualan(models.Model):
    _name = 'maxtor.penjualan'
    _description = 'Nota Penjualan Header'

    name = fields.Char('No Nota', default='Generate', readonly=True)
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer', domain="[( 'customer_rank','>', 0)]", readonly=True,
                                  states={'draft': [('readonly', False)]}, required=True)
    date = fields.Date('Tanggal', default=fields.Date.context_today,readonly=True,
                                  states={'draft': [('readonly', False)]}, required=True)
    note = fields.Text('Notes')
    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'),
                              ('paid', 'Paid'), ('cancel','Cancel')], "State", default='draft', readonly=True)
    line_ids = fields.One2many(comodel_name='maxtor.penjualan.line', inverse_name='penjualan_id', string='Detail',readonly=True,
                                  states={'draft': [('readonly', False)]})
    sub_total = fields.Integer('Sub Total', compute='compute_total', store=True, readonly=True)
    total = fields.Integer('Total', compute='compute_total', store=True, readonly = True)
    disc_header = fields.Float(string='Disc. (%)', digits='Discount',readonly=True,
                                  states={'draft': [('readonly', False)]})

    #Function untuk menghitung total dan subtotal
    @api.depends("line_ids.jumlah", "disc_header")
    def compute_total(self):
        for o in self:
            o.sub_total = sum(o.line_ids.mapped('jumlah'))
            o.total = o.sub_total * (1 - (o.disc_header or 0.0) / 100.0)

    # Function ketika klik confirm maka no nota penjualan akan otomatis terisi
    def action_confirm(self):
        self.write({'state': 'confirm', 'name': self.env['ir.sequence'].next_by_code('maxtor.penjualan')})
        self.update_stock('min')

    def action_paid(self):
        self.write({'state': 'paid'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
        self.update_stock('add')

    #Function untuk update stock ketika klik confirm stok akan berkurang, ketika klik cancel stok bertambah
    def update_stock(self, mode):
        #Check stock
        if mode == 'min':
            for d in self.line_ids:
                p = self.env['product.template'].search([('id','=',d.product_id.id)])
                if p.stock - d.qty < 0:
                    raise exceptions.UserError('Product {} (Stock={}) stock tidak mencukupi'.format(p.name, p.stock))
        # Update Stock
        for d in self.line_ids:
            p = self.env['product.template'].search([('id','=',d.product_id.id)])
            if mode == 'add':
                stock = p.stock + d.qty
            else:
                stock = p.stock - d.qty
            p.write({'stock': stock})

    #Function constraint bahwa jika state tidak sama dengan draft, nota penjualan yang sudah dibuat tidak dapat dihapus
    # @api.model
    def unlink(self):
        if self.state != 'draft':
            raise exceptions.UserError('State {} sudah Confirm/Paid (Tidak Bisa Dihapus)'.format(self.name))
        return super().unlink()


class PenjualanLine(models.Model):
    _name = 'maxtor.penjualan.line'
    _description = 'Notal Penjualan Detail'

    penjualan_id = fields.Many2one(comodel_name='maxtor.penjualan', string='Penjualan', ondelete='cascade')
    product_id = fields.Many2one(comodel_name='product.product', string='Nama Barang')
    harga = fields.Float('Harga', related='product_id.product_tmpl_id.list_price') #related field
    qty = fields.Float("Qty", digits='Discount')
    uom_id = fields.Many2one(comodel_name='uom.uom', string='Satuan', related='product_id.product_tmpl_id.uom_id') #related field
    jumlah = fields.Float('Jumlah', compute='compute_jumlah', store=True, readonly=True)
    disc1 = fields.Float(string='Disc. 1(%)', digits='Discount')
    disc2 = fields.Float(string='Disc. 2(%)', digits='Discount')

    #Function untuk menghitung jumlah
    @api.depends('qty', 'harga', 'disc1', 'disc2')
    def compute_jumlah(self):
        for o in self:
            price = o.harga * (1 - (o.disc1 or 0.0) / 100.0)
            price *= (1 - (o.disc2 or 0.0) / 100.0)
            o.jumlah = o.qty * price

    #Function unutk mengecek apakah stok mencukupi ketika membuat invoice
    @api.onchange('qty')
    def check_qty(self):
        if self.product_id.stock < self.qty:
            raise exceptions.UserError('Product {} (Stock={}) tidak mencukupi'.format(self.product_id.name, self.product_id.stock))
