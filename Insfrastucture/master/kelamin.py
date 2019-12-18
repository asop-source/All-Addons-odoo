from odoo import api, fields, models, _

class Kelamin(models.Model):
	_name='master.kelamin'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Jenis Kelamin")