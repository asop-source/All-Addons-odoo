from odoo import api, fields, models, _
import time

class management(models.Model):
	_name='management.maintenance'

	tiket = fields.Char(string="Tiket",)
	keterangan = fields.Text(string="Keterangan", )
	tujuan = fields.Char(string="Tujuan",)
	status = fields.Boolean(string="Status")
	no = fields.Integer(string="Nomor", required=False, default=False)
	start_date = fields.Date(string="Tanggal Berkunjung", required=False,
                        default=lambda self:time.strftime("%Y-%m-%d"))

	maintenance_id = fields.Many2one(comodel_name="management.perangkatdc")
