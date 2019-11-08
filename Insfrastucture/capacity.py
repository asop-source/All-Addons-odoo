from odoo import api, fields, models, _

class Capacity(models.Model):
	_name='management.capacity'

	no =fields.Char(string="No",)
	rack =fields.Char(string="Rack",)
	used =fields.Char(string="Used",)
	available =fields.Char(string="Available",)
	lokasi = fields.Char(string="Nama Tempat",)