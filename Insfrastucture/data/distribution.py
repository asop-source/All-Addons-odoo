from odoo import api, fields, models, _

class Distribusi(models.Model):
	_name='management.distribution'


	ruang =fields.Many2one(comodel_name="master.ruang", string="Ruang",)
	posisi =fields.Many2one(comodel_name="master.posisi", string="Posisi",)
	name =fields.Char(string="No.Reg/SN",)
	merk =fields.Many2one(comodel_name="management.merk", string="Merk/Model/Type",)
	fungsi =fields.Many2one(comodel_name="master.fungsi",string="Fungsi",)
	koneksi =fields.Many2one(comodel_name="master.koneksi",string="Koneksi Listrik",)
	distribusi =fields.Integer(string="Distribusi")

	visit = fields.Integer(string="Visit",)

	note = fields.Char(string="Note",)

	taken_visit = fields.Float(compute="_oc_taken_visit", string ="Taken Visit", required =False, )


	@api.depends('visit')
	def _oc_taken_visit(self):
		for rec in self:
			if rec.visit>0:
				rec.taken_visit = 100.0/rec.visit
			else:
				rec.taken_visit = 0.0

	@api.onchange('visit')
	def onchange_seats(self):
		if self.visit>0:
			self.taken_visit = 100.0/self.visit
		else:
			self.taken_visit = 0.0