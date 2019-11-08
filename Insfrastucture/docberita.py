from odoo import api, fields, models, _
import time

class DocumentBerita(models.Model):
	_name='management.documentberita'

	no =fields.Char(string="No",)
	judul =fields.Char(string="Judul",)
	start_date = fields.Date(string="Tanggal Posting", required=False,
                        default=lambda self:time.strftime("%Y-%m-%d"))
	publish =fields.Char(string="Publish",)