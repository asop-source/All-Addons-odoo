from odoo import api, fields, models, _

class Utilitas(models.Model):
	_name='management.utilitas'

	name =fields.Many2one(comodel_name="management.merk", string="OS/Merk/Tipe/IP",)
	cpu =fields.Many2one(comodel_name="master.cpu" , string="CPU",)
	ram =fields.Many2one(comodel_name="master.ram", string="RAM",)
	disk= fields.Many2one(comodel_name="master.disk",string="DISK",)
	trafic =fields.Char(string="Trafic in/out",)
	fungsi = fields.Char(string="Fungsi/Note",)