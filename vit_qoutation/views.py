# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrderLine(models.Model):
	_name = 'sale.order.line'
	_inherit = 'sale.order.line'

	account_analytic_id = fields.Many2one('account.analytic.account', string='Unit')
	analytic_tag_ids = fields.Many2many(comodel_name='account.analytic.tag', string='Lokasi', domain=[('analytic_dimension_id.name','=','LOCATION')])
	bisnis = fields.Many2many(comodel_name='account.analytic.tag', string='Bisnis', domain=[('analytic_dimension_id.name','=','BUSINESS')])