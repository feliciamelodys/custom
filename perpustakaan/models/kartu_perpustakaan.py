from datetime import timedelta
from odoo import api, fields, models, exceptions, _

class Kartu(models.Model):
    _name ='perpus.kartu'
    _description = 'Kartu Perpustakaan Header'

    name = fields.Char('No Kartu Perpustakaan', default='Generate', readonly=True)
    peminjam_id = fields.Many2one(comodel_name='res.partner', string='Peminjam', domain=[('is_customer', '=', True)], readonly=False,
                                  states={'confirm': [('readonly', True)]}, context="{'default_is_customer': True}")
    note = fields.Text('Notes')
    state = fields.Selection([('draft','Draft'),
                              ('confirm', 'Confirm')], "State", default='draft', readonly=True)
    line_ids = fields.One2many(comodel_name='perpus.kartu.line', inverse_name='kartu_id', string='Detail', readonly=True,
                               states={'confirm': [('readonly', False)]})
    total = fields.Integer('Total Biaya Peminjaman', compute='compute_total', store=True, readonly=True)

    #member hanya bisa memiliki satu kartu perpus
    _sql_constraints = [('peminjam_unik', 'unique(peminjam_id)', _('Member ini sudah memiliki Kartu Perpustakaan'))]

    @api.depends('line_ids.state')
    def compute_total(self):
        self.total = sum(self.line_ids.filtered(lambda x: x.state=='rent').mapped('harga'))


    #fungsi ketika klik confirm maka no kartu perpustakaan akan otomatis terisi
    def kartu_confirm(self):
        self.write({'state': 'confirm', 'name': self.env['ir.sequence'].next_by_code('perpus.peminjaman')})

    #Jika state tidak draft kartu tidak boleh di delete
    def unlink(self):
        if self.state != 'draft':
            raise exceptions.UserError(("kartu pinjaman tidak bisa dihapus pada state %s !=")(self.state))
        return super().unlink()


class KartuLine(models.Model):
    _name = 'perpus.kartu.line'
    _description = 'Kartu Perpustakaan Detail'

    kartu_id = fields.Many2one(comodel_name='perpus.kartu', string='Kartu')
    buku_id = fields.Many2one(comodel_name='perpus.buku', string='Judul Buku', domain=[('state','=','available')], readonly=True,
                              states={'draft': [('readonly', False)]})
    harga = fields.Integer('Harga', related='buku_id.harga') #related field
    start_date = fields.Date('Start Date', default=fields.Date.context_today, readonly=True,
                              states={'draft': [('readonly', False)]})
    #end_date ditambah 7 dari start_date
    end_date = fields.Date('End Date', default=lambda x: fields.Date.context_today(x) + timedelta(days=7), readonly=True,
                              states={'draft': [('readonly', False)]})
    return_date = fields.Date('Return Date', readonly=True,
                              states={'rent': [('readonly', False)]})
    duration = fields.Integer('Duration (Days)', readonly=True, compute='compute_duration', store=True) #computed field
    denda = fields.Integer('Denda', default=0, readonly=True, compute='compute_denda', store=True) #computed field
    state = fields.Selection([('draft', 'Draft'), ('rent', 'Rented'), ('done', 'Done')], "State", default='draft', readonly=True)

    #constraint untuk mencegah end_date < start_date
    @api.onchange('start_date', 'end_date')
    def check_end_date(self):
        if self.end_date < self.start_date:
            raise exceptions.UserError('End date harus lebih kecil dari Start date')

    def unlink(self):
        if self.state != 'draft':
            raise exceptions.UserError('State {} sudah Done (Tidak Bisa Dihapus)'.format(self.buku_id.name))
        return super().unlink()

    #fungsi untuk menghitung durasi peminjaman
    @api.depends('start_date', 'end_date')
    def compute_duration(self):
        if self.start_date and self.end_date:
            start_date = fields.Datetime.from_string(self.start_date)
            end_date = fields.Datetime.from_string(self.end_date)
            self.duration = abs((end_date - start_date).days)

    #fungsi untuk menghitung denda
    @api.depends('end_date', 'return_date')
    def compute_denda(self):
        if self.end_date and self.return_date:
            end_date = fields.Datetime.from_string(self.end_date)
            return_date = fields.Datetime.from_string(self.return_date)
            if self.return_date < self.end_date :
                self.denda = 0
            else:
                self.denda = abs((return_date - end_date).days) * 1000

    #fungsi untuk mengubah status buku menjadi non available ketika confirm dan status buku di kartu perpus menjadi rent
    def pinjam_confirm(self):
        self.buku_id.state = 'non_available'
        harga = self.harga
        return self.write({'state': 'rent'})

    #fungsi untuk mengubah status buku menjadi available ketikan done dan status buku di kartu perpus menjadi done
    def pinjam_done(self):
        self.buku_id.state = 'available'
        return self.write({'state': 'done'})
