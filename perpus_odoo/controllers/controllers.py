# -*- coding: utf-8 -*-
# from odoo import http


# class Smk-telkom(http.Controller):
#     @http.route('/smk-telkom/smk-telkom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smk-telkom/smk-telkom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('smk-telkom.listing', {
#             'root': '/smk-telkom/smk-telkom',
#             'objects': http.request.env['smk-telkom.smk-telkom'].search([]),
#         })

#     @http.route('/smk-telkom/smk-telkom/objects/<model("smk-telkom.smk-telkom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smk-telkom.object', {
#             'object': obj
#         })
