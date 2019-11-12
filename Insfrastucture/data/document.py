from odoo import api, fields, models, _

class Document(models.Model):
	_name='management.document'

	no =fields.Integer(string="No",)
	kelamin =fields.Many2one(comodel_name="master.kelamin", string="Jenis Kelamin",)
	kode =fields.Char(string="Kode",)
	name =fields.Char(string="Nama",)
	usia = fields.Char(string="Usia",)
	pendidikan =fields.Many2one(comodel_name="master.pendidikan", string="Pendidikan",)
	telp =fields.Char(string="Telp/Hp",)
	email = fields.Char(string="Email",)
	file =fields.Binary(string="File",)
	pengalaman =fields.Char(string="Pengalaman",)
	catatan = fields.Char(string="Catatan")