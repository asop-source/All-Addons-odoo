# -*- coding: utf-8 -*-
from odoo import http

# class VitProfitAndBalance(http.Controller):
#     @http.route('/vit_profit_and_balance/vit_profit_and_balance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_profit_and_balance/vit_profit_and_balance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_profit_and_balance.listing', {
#             'root': '/vit_profit_and_balance/vit_profit_and_balance',
#             'objects': http.request.env['vit_profit_and_balance.vit_profit_and_balance'].search([]),
#         })

#     @http.route('/vit_profit_and_balance/vit_profit_and_balance/objects/<model("vit_profit_and_balance.vit_profit_and_balance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_profit_and_balance.object', {
#             'object': obj
#         })