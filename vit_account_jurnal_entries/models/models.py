# -*- coding: utf-8 -*-

from odoo import models, fields, api


class vit_rpqpo(models.Model):
	_name = 'account.move.line'
	_inherit = 'account.move.line'

	analytic_account_id = fields.Many2one('account.analytic.account', string='Unit')
	analytic_tag_ids = fields.Many2many(comodel_name='account.analytic.tag', string='Lokasi', domain=[('analytic_dimension_id.name','=','LOCATION')])
	bisnis = fields.Many2many(comodel_name='account.analytic.tag', string='Bisnis', domain=[('analytic_dimension_id.name','=','BUSINESS')])