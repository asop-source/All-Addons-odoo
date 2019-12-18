# -*- coding: utf-8 -*-
from odoo import http

# class VitJurnalDraft(http.Controller):
#     @http.route('/vit_jurnal_draft/vit_jurnal_draft/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_jurnal_draft/vit_jurnal_draft/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_jurnal_draft.listing', {
#             'root': '/vit_jurnal_draft/vit_jurnal_draft',
#             'objects': http.request.env['vit_jurnal_draft.vit_jurnal_draft'].search([]),
#         })

#     @http.route('/vit_jurnal_draft/vit_jurnal_draft/objects/<model("vit_jurnal_draft.vit_jurnal_draft"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_jurnal_draft.object', {
#             'object': obj
#         })