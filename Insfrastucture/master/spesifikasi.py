from odoo import api, fields, models, _

class Spesifikasi(models.Model):
	_name='master.spesifikasi'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama Spesifikasi")