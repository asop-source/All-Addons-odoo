from odoo import api, fields, models, _

class Cpu(models.Model):
	_name='master.cpu'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama CPU")