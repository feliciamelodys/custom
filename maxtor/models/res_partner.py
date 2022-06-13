from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner' #inherit dari res.partner odoo
    #Required dijadikan false agar dapat menyimpan customer dimana seharusnya customer depends pada modul accounting
    property_account_payable_id = fields.Many2one('account.account', required=False)
    property_account_receivable_id = fields.Many2one('account.account', required=False)

    #Function untuk melihat histori transaksi yang ditunjukkan dari transaksi customer yang memiliki status "Paid"
    def maxtor_penjualan_action(self):
        action = self.env['ir.actions.act_window']._for_xml_id('maxtor.maxtor_penjualan_action')
        action['context'] = "{'search_default_customer_id': " + str(self.id) +", 'search_default_state': 'paid'}"
        return action
