from odoo import api, fields, models, _

class Layout(models.Model):
	_name='management.data'

	name = fields.Char(string="Nama")
	layout = fields.Binary(string="Image")