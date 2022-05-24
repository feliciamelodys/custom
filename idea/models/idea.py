from odoo import models, fields, api, _
from odoo.exceptions import UserError
#_ untuk translate

class idea(models.Model): #inherit dari Model
    _name = 'idea.idea' #attribut dari class Model (lihat dokumen odoo)
    _description = 'class untuk berlatih tentang idea'
    _rec_name = 'name' #gunanya buat kalau misal di Odoo milih customer ada dropdown ngerecord berdasarkan database (mis: Azure Interior dkk)
    _order = 'date desc' #defaultnya adalah id, pengaruhnya saat List view
    #id = fields.Interger() #ini otomaris ada di odoo, akan jadi PK, tidak perlu ditulis, semua table odoo sudah ada PK

    #membuat attribute field
    name = fields.Char(string='Number', size=64, required=True, index=True, readonly=True,default='New',
                       states={})#index = true karena field ini yang biasanya sering dipake
    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,
                       states={'draft':[('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
                             ('confirmed', 'Confirmed'),
                             ('done', 'Done'),
                             ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
                             default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    #Description is read-only when not draft
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm date')
    #by convention, many2one fields end with '_id'
    confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)

    # sponsor_ids = fields.Many2many(#co_model 'res.partner', #tabel satune'idea_ide_res_partner_rel', #primary key dari tabel idea'idea_idea_id', #primary key dari rest_partner'res_partner_id','Sponsors')
    sponsor_ids = fields.Many2many('res.partner', string='Sponsors') #daripada nulis panjang yang atas mending yang ini lebih singkat cuma tuliskan #co_model dan label nama tabelnya
    voting_ids = fields.One2many('idea.voting', 'idea_id', string='Votes')
    total_yes = fields.Integer("Yes",compute="_computer_vote", store=True, default=0)
    total_no = fields.Integer("No",compute="_computer_vote", store=True, default=0)
    total_abstain = fields.Integer("Abstain",compute="_computer_vote", store=True, default=0)

    score = fields.Integer('Score', default=0, readonly=True)
    owner = fields.Many2one('res.partner', 'Owner', index=True, states={'draft': [('readonly', False)]})
    _sql_constraints = [('name_unik','unique(name)', _('Ideas must unique!'))]

    @api.depends("voting_ids","voting_ids.vote", "voting_ids.state")
    #function ini dijalankan jika record voting (voting_ids) berubah (new atau delete), atau
    #atau saat vote(voting_ids.vote) berubah, atau
    #saat state (voting_ids.state) berubah
    #@api.onchange("voting_ids", "voting_ids.vote", "voting_ids.state")
    #mirip dengan depends tapi ini perubahannya jika hanya melalui UI
    #Kalau depends bisa lewat python code maupun UI, misal kita bikin function automatic vote dari program, nah
    #itu tidak bisa dihandle oleh @api.onchange

    def _computer_vote(self):
        for idea in self.filtered(lambda s:s.state=='done'):
            val = {
                "total_yes": 0,
                "total_no": 0,
                "total_abstain": 0,
            }
            #for rec in idea.voting_ids:
            for rec in idea.voting_ids.filtered(lambda s:s.state=='voted'):
        #lambda adalah on the fly function dari python
        #s ini adalah self dari voting_ids, fungsi filtered ini akan memfilter khusus yang voting_ids
        #bisa juga pakai looping tapi lebih lama, jadi sebelum masuk loop dilakukan filter dulu
                if rec.vote == 'yes':
                    val['total_yes'] += 1
                elif rec.vote == 'no':
                    val['total_no'] += 1
                else:
                    val['total_abstain'] += 1
            idea.update(val) #untuk update 1 record idea

    def action_done(self):
        self.state = 'done'
        t = self.env.context
        print(t.get('keterangan'))

    def action_canceled(self):
        self.state='canceled'

    def action_confirmed(self):
        self.state='confirmed'
        if self.name == 'New' or not self.name:
            seq = self.env['ir.sequence'].search([("code","=","idea.idea")])
            if not seq:
                raise UserError(_('idea.idea sequence not found, please create idea.idea sequence'))
            self.name = seq.next_by_id(sequence_date=self.date)

    def action_settodraft(self):
        self.state='draft'

    def action_tes(self):
        #contoh ambil active user
        print(self.env.user.name)
        #contoh ambil active company
        print(self.env.company.name)
        #contoh common orm method search
        a = self.env['res.partner'].search([('name','ilike','Gemini')])
        a = self.env['res.partner'].search([], limit=2)
        for rec in a:
            print(rec.name)

        #contoh context
        print(self.env.context.get('lang'))
        t = self.env.context.copy()
        t['keterangan']='Ideku'
        self.with_context(t).action_done()
        #
        b = self.env['perpus.buku']  # b adalah object dari model library.bookrent
        b.with_context(t).tes_buku()  # memanggil function di object dari model lain dengan memassingkan context

        # contoh query select
        query = "select name from res_partner order by name desc limit 3"
        self.env.cr.execute(query)
        res = self.env.cr.fetchall() #yang perlu di fetch hanya perintah select
        for data in res:
            print(data[0])

        #contoh query update
        query = "update idea_idea set state='done' where state in ('confirmed','draft')"
        self.env.cr.execute(query)
        self.env.cr.rollback()

        #contoh query delete
        #query = "delete idea_idea where state='draft' "
        self.env.cr.execute(query)
        self.env.cr.rollback()

        #contoh browse
        query = "select * from res_partner limit 3"
        self.env.cr.execute(query)
        res = self.env['res.partner'].browse([row[0] for row in self.env.cr.fetchall()])
        for rec in res:
            print(rec.name)

        #contoh search
        a = self.env["res.partner"]
        res = a.search([], order="name asc", offset=2, limit=6)
        for rec in res:
            print(rec.name)

        #contoh search_count
        count = self.env['res.partner']





    # self.env.cr.execute
    # self.env.cr.commit()
    # self.env.cr.rollback()


