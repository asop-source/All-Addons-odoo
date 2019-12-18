from odoo import api, fields, models, _

class Fungsi(models.Model):
	_name='master.fungsi'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama Fungsi")