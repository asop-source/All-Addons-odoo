# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpProduction(models.Model):
	_name ='mrp.production'
	_inherit = 'mrp.production'


	@api.model
	def create(self, values):
		res = super(MrpProduction, self).create(values)
		lot_data = {
			'name': res.name,
			'product_id': res.product_id.id
		 }
		self.env['stock.production.lot'].create(lot_data)
		return res