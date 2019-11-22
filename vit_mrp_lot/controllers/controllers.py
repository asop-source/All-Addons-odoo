# -*- coding: utf-8 -*-
from odoo import http

# class VitMrpLot(http.Controller):
#     @http.route('/vit_mrp_lot/vit_mrp_lot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_mrp_lot/vit_mrp_lot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_mrp_lot.listing', {
#             'root': '/vit_mrp_lot/vit_mrp_lot',
#             'objects': http.request.env['vit_mrp_lot.vit_mrp_lot'].search([]),
#         })

#     @http.route('/vit_mrp_lot/vit_mrp_lot/objects/<model("vit_mrp_lot.vit_mrp_lot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_mrp_lot.object', {
#             'object': obj
#         })