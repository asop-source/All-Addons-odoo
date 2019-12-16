# -*- coding: utf-8 -*-
from odoo import http

# class VitOvertimeMounth(http.Controller):
#     @http.route('/vit_overtime_mounth/vit_overtime_mounth/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_overtime_mounth/vit_overtime_mounth/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_overtime_mounth.listing', {
#             'root': '/vit_overtime_mounth/vit_overtime_mounth',
#             'objects': http.request.env['vit_overtime_mounth.vit_overtime_mounth'].search([]),
#         })

#     @http.route('/vit_overtime_mounth/vit_overtime_mounth/objects/<model("vit_overtime_mounth.vit_overtime_mounth"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_overtime_mounth.object', {
#             'object': obj
#         })