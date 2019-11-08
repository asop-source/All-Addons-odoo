from odoo import api, fields, models, _

class perangkatdc(models.Model):
		_name ='management.perangkatdc'

		no = fields.Char(string="Nomor", required=False, default=False)
		jabatan = fields.Many2one(comodel_name="res.users",
								  string="Posisi")
		penanggung_jawab = fields.Many2one(comodel_name="hr.employee",
											string="SKPD/UKPD/Pemilik")
		no_reg = fields.Char(string="No.Reg/SN/IP")
		active = fields.Boolean(string="DC / Non DC", default=True)
		merk = fields.Many2one(comodel_name="management.merk", string="Merk/Model/Type")
		spesifikasi = fields.Char(string="Spesifikasi")
		fungsi = fields.Char(string="Fungsi")
		visit = fields.Char(string="visit")
		note = fields.Text(string="Note")

		perangkat_id = fields.One2many(comodel_name="management.maintenance", inverse_name="maintenance_id",
									string="Maintenance", required=False)
