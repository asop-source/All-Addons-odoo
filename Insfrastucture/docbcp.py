from odoo import api, fields, models, _

class DocumentBCP(models.Model):
	_name='management.documentbcp'

	no =fields.Char(string="No",)
	code =fields.Char(string="Code",)
	sop =fields.Char(string="BPP Name",)
	data =fields.Char(string="Data Issued",)
	review = fields.Char(string="Data reviewe",)
	resived =fields.Char(string="Data Resived",)