from odoo import api, fields, models, _
import time
class DocumentBCP(models.Model):
	_name='management.documentbcp' 


	code =fields.Char(string="Code",)
	name =fields.Char(string="SOP Name",)
	data =fields.Date(string="Data Issued",required=False,
                        default=lambda self:time.strftime("%Y-%m-%d"))
	review = fields.Date(string="Data reviewe",required=False,
                        default=lambda self:time.strftime("%Y-%m-%d"))
	resived =fields.Date(string="Data Resived",required=False,
                        default=lambda self:time.strftime("%Y-%m-%d"))