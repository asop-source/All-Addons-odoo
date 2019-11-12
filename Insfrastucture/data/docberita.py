from odoo import api, fields, models, _
import time

class DocumentBerita(models.Model):
	_name='management.documentberita'

	judul =fields.Char(string="Judul",)
	start_date = fields.Date(string="Tanggal Posting", required=False,
                        default=lambda self:time.strftime("%Y-%m-%d"))
	publish =fields.Many2one(comodel_name="master.berita",string="Publish",)