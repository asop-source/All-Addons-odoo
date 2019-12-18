from odoo import api, fields, models, _

class publish(models.Model):
	_name='master.berita'

	kode = fields.Integer("No ID")
	name= fields.Char("Nama Publish")