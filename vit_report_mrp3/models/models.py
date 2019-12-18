# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class vit_report_mrp3(models.Model):
#     _name = 'vit_report_mrp3.vit_report_mrp3'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100