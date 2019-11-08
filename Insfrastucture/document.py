from odoo import api, fields, models, _

class Document(models.Model):
	_name='management.document'

	no =fields.Char(string="No",)
	name =fields.Char(string="Nama",)
	kode =fields.Char(string="Kode",)
	kelamin =fields.Char(string="Jenis kelamin",)
	usia = fields.Char(string="Usia",)
	pendidikan =fields.Char(string="Pendidikan",)
	telp =fields.Char(string="Telp/Hp",)
	email = fields.Char(string="Email",)
	file =fields.Char(string="File",)
	pengalaman =fields.Char(string="Pengalaman",)
	catatan = fields.Char(string="Catatan",)