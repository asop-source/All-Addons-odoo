# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import simplejson

class VitWebsiteSo(http.Controller):

	@http.route('/vit/so',type='http' , auth='public', website=True)
	def index(self, **kw):
		sale_orders = request.env['sale.order'].search([])
		return request.render("vit_website_so.index", {
			'sale_orders': sale_orders
			})
		
	# membuat ajax
	@http.route('/vit/load_ajax',type='http' , auth='public', website=True)
	def load_ajax(self, **kw):
		return request.render("vit_website_so.index_ajax", {
			})
		sale_orders = request.env['sale.order'].search([])
		result = {}
		result ['data'] = []

		for so in sale_orders:
			result['data'].append([
				so.name,
				so.confirm_date,
				so.partner_id,
				so.user_id,
				so.amount_total,
				so.invoice_status,
			])

		return simplejson.dumps(result)