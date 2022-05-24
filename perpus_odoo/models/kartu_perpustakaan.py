from odoo import api, fields, models, exceptions




class kartu_perpustakaan(models.Model):
    _name = 'perpus.kartu'
    _description = 'Peminjaman Header'

    lines_ids = fields.One2many(comodel_name='perpus.kartu.line', inverse_name='kartu_id',
                                  string='Detail', readonly=True,
                                  states={'confirm': [('readonly', False)]})
    name = fields.Char(string='No Kartu Perpustakaan', readonly=True, default="Auto")
    peminjam_id = fields.Many2one('res.partner', 'Peminjam', domain=[('is_customer', '=', True)])
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], "State", default='draft', readonly=True)
    notes = fields.Text('Notes')

    def kartu_confirm(self):
        return self.write({'state': 'confirm'})

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('kartu_perpustakaan')
        return super(katu_perpustakaan, self).create(vals)

    # def unlink(self):
    #     if self.state != 'draft':
    #         raise exceptions.UserError(("kartu pinjaman tidak bisa dihapus pada state %s !=")(self.state))
    #     return super(katu_perpustakaan, self).unlink()


class kartu_perpustakaan_line(models.Model):
    _name = 'perpus.kartu.line'

    kartu_id = fields.Many2one(comodel_name='perpus.kartu', string='Nomor Kartu Perpusatakaan', required=True,
                               ondelete='cascade')
    buku_id = fields.Many2one('perpus.buku', 'Judul Buku', domain=[('status', '=', 'available')])
    state = fields.Selection([('draft', 'Draft'), ('rent', 'Rented'), ('return', 'Done')], "State", default='draft',
                             readonly=True)
    start_date = fields.Date('Start Date', default=fields.Date.context_today)
    end_date = fields.Date('End Date', default=fields.Date.context_today)
    return_date = fields.Date('Return Date', default=fields.Date.context_today)
    denda = fields.Integer('Denda', readonly=True, compute='compute_denda', store=True)
    duration = fields.Integer('Duration (Days)', readonly=True, compute='compute_day', store=True)
    harga = fields.Integer('Harga', related='buku_id.harga')
    peminjam_id = fields.Many2one(comodel_name='res.partner', string='Peminjam', related="kartu_id.peminjam_id", store=True,
                                 readonly=True)
    no_kartu = fields.Char(string='No Kartu', related='kartu_id.name', readonly=True, store=True)

    # def unlink(self):
    #     if self.state != 'draft':
    #         raise exceptions.UserError(("Data buku pinjaman tidak bisa dihapus pada state %s !") % (self.state))
    #     return super(kartu_perpustakaan_line, self).unlink()

    @api.depends('start_date', 'end_date')
    def compute_day(self):
        if self.start_date and self.end_date:
            start_date = fields.Datetime.from_string(self.start_date)
            end_date = fields.Datetime.from_string(self.end_date)
            self.duration = abs((end_date - start_date).days) + 1

    @api.depends('end_date', 'return_date')
    def compute_denda(self):
        if self.end_date and self.return_date:
            end_date = fields.Datetime.from_string(self.end_date)
            return_date = fields.Datetime.from_string(self.return_date)
            self.denda = abs((return_date - end_date).days) * 10000

    def pinjam_confirm(self):
        self.buku.state = 'rent'
        return self.write({'state': 'rent'})

    def pinjam_done(self):
        self.buku.state = 'available'
        return self.write({'state': 'return'})
