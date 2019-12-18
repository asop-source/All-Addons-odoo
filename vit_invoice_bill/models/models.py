# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vit_rpqpo(models.Model):
	_name = 'account.invoice.line'
	_inherit = 'account.invoice.line'

	account_analytic_id = fields.Many2one(comodel_name='account.analytic.account', string='Unit')
	analytic_tag_ids = fields.Many2many(comodel_name='account.analytic.tag', string='Lokasi', domain=[('analytic_dimension_id.name','=','LOCATION')])
	bisnis = fields.Many2many(comodel_name='account.analytic.tag', string='Bisnis', domain=[('analytic_dimension_id.name','=','BUSINESS')])