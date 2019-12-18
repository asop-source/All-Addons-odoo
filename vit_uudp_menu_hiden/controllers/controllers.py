# -*- coding: utf-8 -*-
from odoo import http

# class VitUudpMenuHiden(http.Controller):
#     @http.route('/vit_uudp_menu_hiden/vit_uudp_menu_hiden/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vit_uudp_menu_hiden/vit_uudp_menu_hiden/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vit_uudp_menu_hiden.listing', {
#             'root': '/vit_uudp_menu_hiden/vit_uudp_menu_hiden',
#             'objects': http.request.env['vit_uudp_menu_hiden.vit_uudp_menu_hiden'].search([]),
#         })

#     @http.route('/vit_uudp_menu_hiden/vit_uudp_menu_hiden/objects/<model("vit_uudp_menu_hiden.vit_uudp_menu_hiden"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vit_uudp_menu_hiden.object', {
#             'object': obj
#         })