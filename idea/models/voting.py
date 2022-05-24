from odoo import models, fields, api, _
from odoo.exceptions import UserError
#_ untuk translate

class voting(models.Model): #inherit dari Model
    _name = 'idea.voting' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel
    _description = 'class untuk berlatih tentang voting'
    _rec_name = 'name' #gunanya buat kalau misal di Odoo milih customer ada dropdown ngerecord berdasarkan database (mis: Azure Interior dkk)
    _order = 'date desc' #defaultnya adalah id, pengaruhnya saat List view
    #id = fields.Interger() #ini otomaris ada di odoo, akan jadi PK, tidak perlu ditulis, semua table odoo sudah ada PK

    #membuat attribute field
    name = fields.Char(string='Number', size=64, required=True, index=True, readonly=True,default="New",
                       states={}) #index = true karena field ini yang biasanya sering dipake
    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,
                       states={})
    state = fields.Selection([('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                             ('voted', 'Voted'),
                             ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
                             default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    vote = fields.Selection([('yes', 'Yes'),
                             ('no', 'No'),
                             ('abstain', 'Abstain')], 'Vote', required=True, readonly=False)



    #by convention, many2one fields end with '_id'
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete="cascade",default=lambda self: self.env.user)
    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done'),('active','=','True')]")
    idea_date = fields.Date("Idea date", related='idea_id.date', store=True)

    def action_canceled(self):
        self.state='canceled'

    def action_voted(self):
        self.state='voted'
        if self.name == 'New' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])

            self.name = seq.next_by_id()

    @api.model_create_multi
    def create(self, vals_list): #ketika action save diklik akan muncul number otomatis, kita melakukan overwrite button save yang sudah ada di Odoo
        if self.name == 'New' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])
            if not seq:
                raise UserError(_('idea.idea sequence not found, please create idea.idea sequence'))
            for val in vals_list:
                val['name'] = seq.next_by_id()

        return super(voting,self).create(vals_list) #voting yang ada di super ini nama class

    def action_settodraft(self):
        self.state='draft'
