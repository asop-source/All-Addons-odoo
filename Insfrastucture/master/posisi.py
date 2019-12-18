from odoo import api, fields, models, _

class Posisi(models.Model):
	_name='master.posisi'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama Posisi",)