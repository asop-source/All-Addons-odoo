from odoo import api, fields, models, _

class Landistribusi(models.Model):
	_name = 'management.landistribusi'

	ruang =fields.Char(string="Ruang",)
	posisi =fields.Char(string="Posisi",)
	no_reg =fields.Char(string="No.Reg/SN",)
	merk =fields.Char(string="Merk/Model/Type",)
	fungsi = fields.Char(string="Fungsi",)
	koneksi = fields.Char(string="Koneksi LAN",)
	distribusi = fields.Char(string="Distribusi",)
	visit = fields.Char(string="Visit",)
	note = fields.Char(string="Note",)