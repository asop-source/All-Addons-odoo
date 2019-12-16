# -*- coding: utf-8 -*-
from odoo import http

# class VitOvertimeCustom(http.Controller):
#     @http.route('/vit_overtime_custom/vit_overtime_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_overtime_custom/vit_overtime_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_overtime_custom.listing', {
#             'root': '/vit_overtime_custom/vit_overtime_custom',
#             'objects': http.request.env['vit_overtime_custom.vit_overtime_custom'].search([]),
#         })

#     @http.route('/vit_overtime_custom/vit_overtime_custom/objects/<model("vit_overtime_custom.vit_overtime_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_overtime_custom.object', {
#             'object': obj
#         })