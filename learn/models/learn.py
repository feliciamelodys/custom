from odoo import models, fields, api, _
#_ untuk translate

class Idea(models.Model): #inherit dari Model
    _name = 'learn.idea' #attribut dari class Model (lihat dokumen odoo)
    _description = 'class untuk berlatih tentang idea'
    # _rec_name = 'name' #gunanya buat kalau misal di Odoo milih customer ada dropdown ngerecord berdasarkan database (mis: Azure Interior dkk)
    # _order = 'date desc' #defaultnya adalah id, pengaruhnya saat List view
    #id = fields.Interger() #ini otomaris ada di odoo, akan jadi PK, tidak perlu ditulis, semua table odoo sudah ada PK

    #membuat attribute field
    name = fields.Char(string='Number', size=64, required=True,  readonly=True, states={'draft':[('readonly', False)]})
    date = fields.Date(string='Date Release', default=fields.Date.context_today, readonly=True, states={'draft':[('readonly', False)]})
    state = fields.Selection(
        [('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('confirmed', 'CBooleanonfirmed'),
         ('done', 'Done'),
         ('canceled', 'Canceled')], string='State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    description = fields.Text(string='Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean(string='Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm date')
    confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)
    sponsor_ids = fields.Many2many('res.partner', 'Sponsors')  # daripada nulis panjang yang atas mending yang ini lebih singkat cuma tuliskan #co_model dan label nama tabelnya
    score = fields.Integer('Score', default=0, readonly=True)
    owner = fields.Many2one('res.partner', 'Owner', index=True, states={'draft': [('readonly', False)]})

    _sql_constraints = [('name_unik','unique(name)', _('Ideas must unique!'))] #memberikan batasan jadi kalo insert nama yang sama gak boleh harus unik

