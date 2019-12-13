# -*- coding: utf-8 -*-
from odoo import http

# class VitAccountJurnalEntries(http.Controller):
#     @http.route('/vit_account_jurnal_entries/vit_account_jurnal_entries/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_account_jurnal_entries/vit_account_jurnal_entries/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_account_jurnal_entries.listing', {
#             'root': '/vit_account_jurnal_entries/vit_account_jurnal_entries',
#             'objects': http.request.env['vit_account_jurnal_entries.vit_account_jurnal_entries'].search([]),
#         })

#     @http.route('/vit_account_jurnal_entries/vit_account_jurnal_entries/objects/<model("vit_account_jurnal_entries.vit_account_jurnal_entries"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_account_jurnal_entries.object', {
#             'object': obj
#         })