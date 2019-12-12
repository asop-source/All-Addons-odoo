# -*- coding: utf-8 -*-
from odoo import http

# class VitInventoryReceipts(http.Controller):
#     @http.route('/vit_inventory_receipts/vit_inventory_receipts/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_inventory_receipts/vit_inventory_receipts/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_inventory_receipts.listing', {
#             'root': '/vit_inventory_receipts/vit_inventory_receipts',
#             'objects': http.request.env['vit_inventory_receipts.vit_inventory_receipts'].search([]),
#         })

#     @http.route('/vit_inventory_receipts/vit_inventory_receipts/objects/<model("vit_inventory_receipts.vit_inventory_receipts"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_inventory_receipts.object', {
#             'object': obj
#         })