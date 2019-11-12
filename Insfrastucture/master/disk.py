from odoo import api, fields, models, _

class Disk(models.Model):
	_name='master.disk'

	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama Disk")