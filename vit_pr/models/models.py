# -*- coding: utf-8 -*-

from odoo import models, fields, api

class product_request(models.Model):
    _name = 'vit.product.request'
    _inherit = 'vit.product.request'

    location_id = fields.Many2one(comodel_name="account.analytic.tag", string="Location", required=False, )
    business_id = fields.Many2one(comodel_name="account.analytic.tag", string="Business", required=False, )