from odoo import models, fields, api,exceptions,_

class Retur(models.Model):
    _name = 'maxtor.retur'
    _description = 'Retur Penjualan Header'

    name = fields.Char('No Nota', default='Generate', readonly=True)
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer', domain="[( 'customer_rank','>', 0)]",
                                  readonly=True,
                                  states={'draft': [('readonly', False)]}, required=True)
    date = fields.Date('Tanggal', default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]}, required=True)
    penjualan_id = fields.Many2one(comodel_name='maxtor.penjualan', string='Penjualan', readonly=True,
                                   states={'draft': [('readonly', False)]},
                                   domain=[('state','in',('confirm','paid'))])
    note = fields.Text('Notes')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('paid', 'Paid'),
                              ('cancel', 'Cancel')], "State", default='draft', readonly=True)
    line_ids = fields.One2many(comodel_name='maxtor.retur.line', inverse_name='retur_id', string='Detail',readonly=True,
                                  states={'draft': [('readonly', False)]})
    total = fields.Float('Total', compute='compute_total', store=True, readonly=True)

    # Function ketika klik confirm maka no retur penjualan akan otomatis terisi
    def action_confirm(self):
        self.write({'state': 'confirm', 'name': self.env['ir.sequence'].next_by_code('maxtor.retur')})
        self.update_stock('add')

    def action_paid(self):
        self.write({'state': 'paid'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
        self.update_stock('min')

    #Function untuk update stock ketika klik confirm stok akan berkurang, ketika klik cancel stok bertambah
    def update_stock(self, mode):
        # Update Stock
        for d in self.line_ids:
            p = self.env['product.template'].search([('id','=',d.product_id.id)])
            if mode == 'add':
                stock = p.stock + d.retur_qty
            else:
                stock = p.stock - d.retur_qty
            p.write({'stock': stock})

    #Function untuk mendapatkan invoice dari customer_id yang dipilih
    @api.onchange('customer_id')
    def onchange_customer_id(self):
        for o in self:
            return {'domain': {'penjualan_id':[('state','in',('confirm','paid')),('customer_id','=',o.customer_id.id)]}}

    #Function untuk menghitung total dan sub total
    @api.depends('line_ids.jumlah')
    def compute_total(self):
        for o in self:
            o.total = sum(o.line_ids.mapped('jumlah'))

    #Function untuk mendapatkan detail penjualan berdasarkan penjualan_id
    @api.onchange('penjualan_id')
    def get_detail(self):
        for o in self:
            o.line_ids = [(5, 0, 0)] #menghapus detail yang ada
            lines = []
            for l in o.penjualan_id.line_ids:
                lines.append((0,0, {
                    'retur_id': o.id,
                    'penjualan_id': l.penjualan_id.id,
                    'product_id': l.product_id.id,
                    'harga': l.harga,
                    'qty': l.qty,
                    'retur_qty': l.qty,
                    'uom_id': l.uom_id.id,
                    'jumlah': l.jumlah,
                    'disc1': l.disc1,
                    'disc2': l.disc2
                }))
            o.line_ids = lines


class ReturLine(models.Model):
    _name = 'maxtor.retur.line'
    _description = 'Retur Penjualan Line'

    retur_id = fields.Many2one(comodel_name='maxtor.retur', string='Retur', ondelete='cascade')
    penjualan_id = fields.Many2one(comodel_name='maxtor.penjualan', string='Penjualan')
    product_id = fields.Many2one(comodel_name='product.product', string='Nama Barang', readonly=True)
    harga = fields.Float('Harga', readonly=True) #related field
    qty = fields.Float("Qty", digits='Discount', readonly=True)
    retur_qty = fields.Float('Retur Qty', digits='Discount') #Pada retur penjualan hanya attribut retur_qty yang dapat di edit
    uom_id = fields.Many2one(comodel_name='uom.uom', string='Satuan', readonly=True) #related field
    jumlah = fields.Float('Jumlah', compute='compute_jumlah', store=True, readonly=True)
    disc1 = fields.Float(string='Disc. 1(%)', digits='Discount', readonly=True)
    disc2 = fields.Float(string='Disc. 2(%)', digits='Discount', readonly=True)

    #Function untuk menghitung jumlah
    @api.depends('retur_qty', 'harga', 'disc1', 'disc2')
    def compute_jumlah(self):
        for o in self:
            price = o.harga * (1 - (o.disc1 or 0.0) / 100.0)
            price *= (1 - (o.disc2 or 0.0) / 100.0)
            o.jumlah = o.retur_qty * price

    #Function unutk mengecek apakah stok mencukupi ketika membuat retur penjualan
    @api.onchange('retur_qty')
    def check_qty(self):
        if self.qty < self.retur_qty:
            raise exceptions.UserError('Product {} (Qty pembelian={}) tidak mencukupi'.format(self.product_id.name, self.qty))
