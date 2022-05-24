from odoo import models, fields, api, _

class mahasiswa(models.Model):
    _name = 'nilai.mahasiswa'
    _description = 'database master mahasiswa'
    _rec_name = 'name'

    nrp = fields.Char('NRP', size=64, required=True, index=True)
    name = fields.Char('Nama', size=64, required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')
    status = fields.Selection([('active', 'Active'),
                              ('inactive', 'Inactive')], 'State', required=True, readonly=False, default='active')

    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'
    def action_settodraft(self):
        self.state = 'draft'