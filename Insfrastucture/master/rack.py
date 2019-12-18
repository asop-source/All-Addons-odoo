from odoo import api, fields, models, _

class SubRuang(models.Model):
	_name='master.rack'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama Rack")