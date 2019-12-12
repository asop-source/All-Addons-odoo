# -*- coding: utf-8 -*-
from odoo import http

# class VitPr(http.Controller):
#     @http.route('/vit_pr/vit_pr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_pr/vit_pr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_pr.listing', {
#             'root': '/vit_pr/vit_pr',
#             'objects': http.request.env['vit_pr.vit_pr'].search([]),
#         })

#     @http.route('/vit_pr/vit_pr/objects/<model("vit_pr.vit_pr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_pr.object', {
#             'object': obj
#         })