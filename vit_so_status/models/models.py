# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
	_name = 'sale.order'
	_inherit ='sale.order'

	state = fields.Selection([
        ('draft', 'Quotation'),
        ('approve', 'Approve1'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')



# class vit_so_status(models.Model):
#     _name = 'vit_so_status.vit_so_status'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100