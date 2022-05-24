from odoo import api, fields, models, exceptions


class katu_perpustakaan(models.Model):
    _name = 'kartu_perpustakaan'
    _description = 'Tabel kartu perpustakaan'

    kartu_lines = fields.One2many(comodel_name='kartu_perpustakaan_line', inverse_name='kartu_id',
                                  string='kartu perpustakaan line', readonly=True,
                                  states={'confirm': [('readonly', False)]})
    name = fields.Char(string='No referensi', readonly=True, default="Auto")
    anggota_id = fields.Many2one(comodel_name='anggota', string='Nama Anggota', Required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], "State", default='draft', readonly=True)
    note = fields.Text('Notes')

    def kartu_confirm(self):
        return self.write({'state': 'confirm'})

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('kartu_perpustakaan')
        return super(katu_perpustakaan, self).create(vals)

    def unlink(self):
        if self.state != 'draft':
            raise exceptions.UserError(("kartu pinjaman tidak bisa dihapus pada state %s !=")(self.state))
        return super(katu_perpustakaan, self).unlink()


class kartu_perpustakaan_line(models.Model):
    _name = 'kartu_perpustakaan_line'

    kartu_id = fields.Many2one(comodel_name='kartu_perpustakaan', string='Kartu Perpustakaan', required=True,
                               ondelete='cascade')
    buku = fields.Many2one(comodel_name='buku', string='buku', )
    state = fields.Selection([('draft', 'Draft'), ('rent', 'Rented'), ('return', 'Done')], "State", default='draft',
                             readonly=True)
    start_date = fields.Date('Start Date', default=fields.Date.context_today)
    end_date = fields.Date('End Date', default=fields.Date.context_today)
    duration = fields.Integer('Duration (Days)', readonly=True, compute='compute_day', store=True)

    anggota_id = fields.Many2one(comodel_name='anggota', string='Member', related="kartu_id.anggota_id", store=True,
                                 readonly=True)
    nama_kartu = fields.Char(string='Card', related='kartu_id.name', readonly=True, store=True)

    def unlink(self):
        if self.state != 'draft':
            raise exceptions.UserError(("Data buku pinjaman tidak bisa dihapus pada state %s !") % (self.state))
        return super(kartu_perpustakaan_line, self).unlink()

    @api.depends('start_date', 'end_date')
    def compute_day(self):
        if self.start_date and self.end_date:
            start_date = fields.Datetime.from_string(self.start_date)
            end_date = fields.Datetime.from_string(self.end_date)
            self.duration = abs((end_date - start_date).days) + 1

    def pinjaman_confirm(self):
        self.buku.state = 'rent'
        return self.write({'state': 'rent'})

    def pinjaman_done(self):
        self.buku.state = 'available'
        return self.write({'state': 'return'})    
    