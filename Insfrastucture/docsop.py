from odoo import api, fields, models, _

class DocumentSOP(models.Model):
	_name='management.documentsop'

	no =fields.Char(string="No",)
	code =fields.Char(string="Code",)
	sop =fields.Char(string="SOP Name",)
	data =fields.Char(string="Data Issued",)
	review = fields.Char(string="Data reviewe",)
	resived =fields.Char(string="Data Resived",)