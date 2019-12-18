# -*- coding: utf-8 -*-
from odoo import http

# class AnalysticTag(http.Controller):
#     @http.route('/analystic_tag/analystic_tag/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/analystic_tag/analystic_tag/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('analystic_tag.listing', {
#             'root': '/analystic_tag/analystic_tag',
#             'objects': http.request.env['analystic_tag.analystic_tag'].search([]),
#         })

#     @http.route('/analystic_tag/analystic_tag/objects/<model("analystic_tag.analystic_tag"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('analystic_tag.object', {
#             'object': obj
#         })