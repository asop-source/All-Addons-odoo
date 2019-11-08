from odoo import api, fields, models, _

class merk(models.Model):
	_name='management.merk'


	kode = fields.Integer(string="No ID")
	name = fields.Char(string="Nama",)
