from odoo import api, fields, models, _

class Location(models.Model):
	_name='master.location'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama",)