# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import simplejson
import time

class VitWebsiteSo(http.Controller):

	@http.route('/vit/so',type='http' , auth='public', website=True)
	def index(self, **kw):
		sale_orders = request.env['sale.order'].search([])
		return request.render("vit_website_so.index", {
			'sale_orders': sale_orders
			})
		

	# membuat ajax
	@http.route('/vit/so_ajax',type='http' , auth='public', website=True)
	def index_ajax(self, **kw):
		sale_orders = request.env['sale.order'].search([])
		return request.render("vit_website_so.index_ajax", {
			})

	@http.route('/vit/load_ajax',type='http' , auth='public', website=True)
	def load_ajax(self, **kw):
		sale_orders = request.env['sale.order'].search([])
		result = {}
		result ['data'] = []
		for name in sale_orders:
			result['data'].append([
				name.name,
				name.confirmation_date,
				name.partner_id.name,
				name.user_id.name,
				name.amount_total,
				name.invoice_status,
			])
		return simplejson.dumps(result, default=str)