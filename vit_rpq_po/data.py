# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vit_rpqpo(models.Model):
	_name = 'purchase.order.line'
	_inherit = 'purchase.order.line'

	account_analytic_id = fields.Many2one('account.analytic.account', string='Unit')
	analytic_tag_ids = fields.Many2many(comodel_name='account.analytic.tag', string='Lokasi', domain=[('analytic_dimension_id.name','=','LOCATION')])
	bisnis = fields.Many2many(comodel_name='account.analytic.tag', string='Bisnis', domain=[('analytic_dimension_id.name','=','BUSINESS')])