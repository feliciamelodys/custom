from datetime import datetime, timedelta
from odoo import api,fields,models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class PenjualanReport(models.TransientModel):
    _name = 'maxtor.penjualan.report.wizard'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)
    customer_id = fields.Many2one(comodel_name='res.partner', domain=[('customer_rank','>',0)])

    def print(self):
        data = {
            # 'ids': self.ids,
            # 'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'customer_id': self.customer_id.id,
                'customer_name': self.customer_id.name
            },
        }
        return self.env.ref('maxtor.penjualan_report').report_action(self, data=data)


class PenjualanReportView(models.AbstractModel):
    _name = 'report.maxtor.penjualan_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['maxtor.penjualan'].search([('customer_id','=',data['form']['customer_id']),
                                                         ('date','>=',data['form']['date_start']),
                                                         ('date','<=',data['form']['date_end'])])
        return {
            # 'doc_ids': docs.ids,
            # 'doc_model': data['model'],
            'date_start': data['form']['date_start'],
            'date_end': data['form']['date_end'],
            'customer_name': data['form']['customer_name'],
            'docs': docs,
        }
