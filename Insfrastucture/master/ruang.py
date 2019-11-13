from odoo import api, fields, models, _

class Ruang(models.Model):
	_name='master.ruang'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama Ruang")
