from odoo import api, fields, models, _

class Koneksi (models.Model): 
	_name='master.koneksi'

	kode = fields.Integer (string ="ID Koneksi")
	name = fields.Char(string="Nama Koneksi")