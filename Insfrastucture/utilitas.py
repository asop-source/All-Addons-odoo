from odoo import api, fields, models, _

class Utilitas(models.Model):
	_name='management.utilitas'

	no =fields.Char(string="No",)
	ip =fields.Char(string="OS/Merk/Tipe/IP",)
	cpu =fields.Char(string="CPU",)
	ram =fields.Char(string="RAM",)
	disk= fields.Char(string="DISK",)
	trafic =fields.Char(string="Trafic in/out",)
	fungsi = fields.Char(string="Fungsi/Note",)