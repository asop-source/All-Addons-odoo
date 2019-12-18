from odoo import api, fields, models, _

class Pendidikan(models.Model):
	_name='master.pendidikan'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Pendidikan")