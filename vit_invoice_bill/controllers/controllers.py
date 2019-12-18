# -*- coding: utf-8 -*-
from odoo import http

# class VitInvoiceBill(http.Controller):
#     @http.route('/vit_invoice_bill/vit_invoice_bill/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_invoice_bill/vit_invoice_bill/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_invoice_bill.listing', {
#             'root': '/vit_invoice_bill/vit_invoice_bill',
#             'objects': http.request.env['vit_invoice_bill.vit_invoice_bill'].search([]),
#         })

#     @http.route('/vit_invoice_bill/vit_invoice_bill/objects/<model("vit_invoice_bill.vit_invoice_bill"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_invoice_bill.object', {
#             'object': obj
#         })