from odoo import api, fields, models, _
import time

class DocumentAgenda(models.Model):
	_name='management.documentagenda'

	no =fields.Char(string="No",)
	tema =fields.Char(string="Tema",)
	mulai = fields.Date(string="Tanggal Mulai", required=False,
                        default=lambda self:time.strftime("%Y-%m-%d"))
	Selesai = fields.Date(string="Tanggal Selesai", required=False,
                        default=lambda self:time.strftime("%Y-%m-%d"))