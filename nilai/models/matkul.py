from odoo import models, fields, api, _

class matkul(models.Model):
    _name = 'nilai.matkul'
    _description = 'database master mata kuliah'
    _rec_name = 'name'

    kode = fields.Char('Kode Mata Kuliah', size=64, required=True)
    name = fields.Char('Nama', size=64, required=True)
    sks = fields.Integer('SKS', required=True, index=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    def action_done(self):
        self.state = 'done'
    def action_canceled(self):
        self.state = 'canceled'
    def action_settodraft(self):
        self.state = 'draft'