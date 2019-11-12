from odoo import api, fields, models, _

class publish(models.Model):
	_name='master.berita'

	no = fields.Integer("No ID")
	name= fields.Char("Nama Publish")