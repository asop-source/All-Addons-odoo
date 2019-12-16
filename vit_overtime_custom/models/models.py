# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomWork(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    work_location = fields.Many2one('account.analytic.tag')