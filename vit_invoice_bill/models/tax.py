# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Tax(models.Model):
	_name = 'account.invoice.tax'
	_inherit = 'account.invoice.tax'

	account_analytic_id = fields.Many2one(comodel_name='account.analytic.account', string='Unit')
	analytic_tag_ids = fields.Many2many(comodel_name='account.analytic.tag', string='Lokasi', domain=[('analytic_dimension_id.name','=','LOCATION')])
	bisnis = fields.Many2many(comodel_name='account.analytic.tag', string='Bisnis', domain=[('analytic_dimension_id.name','=','BUSINESS')])