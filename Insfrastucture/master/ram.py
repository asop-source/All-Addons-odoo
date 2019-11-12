from odoo import api, fields, models, _

class Ram(models.Model):
	_name='master.ram'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama Ram")