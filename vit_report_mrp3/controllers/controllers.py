# -*- coding: utf-8 -*-
from odoo import http

# class VitReportMrp3(http.Controller):
#     @http.route('/vit_report_mrp3/vit_report_mrp3/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_report_mrp3/vit_report_mrp3/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_report_mrp3.listing', {
#             'root': '/vit_report_mrp3/vit_report_mrp3',
#             'objects': http.request.env['vit_report_mrp3.vit_report_mrp3'].search([]),
#         })

#     @http.route('/vit_report_mrp3/vit_report_mrp3/objects/<model("vit_report_mrp3.vit_report_mrp3"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_report_mrp3.object', {
#             'object': obj
#         })