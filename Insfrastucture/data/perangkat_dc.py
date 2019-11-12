from odoo import api, fields, models, _

class perangkatdc(models.Model): 
		_name ='management.perangkatdc'

		no = fields.Char(string="Nomor", required=False, default=False)
		posisi= fields.Many2one(comodel_name="master.ruang",
								  string="Posisi")
		penanggung_jawab = fields.Many2one(comodel_name="hr.employee",
											string="SKPD/UKPD/Pemilik")
		name = fields.Char(string="No.Reg/SN/IP")
		active = fields.Boolean(string="DC / Non DC", default=True)
		merk = fields.Many2one(comodel_name="management.merk", string="Merk/Model/Type")
		spesifikasi = fields.Many2one(comodel_name="master.spesifikasi", string="Spesifikasi")
		fungsi = fields.Many2one(comodel_name= "master.fungsi" ,string="Fungsi")

		visit = fields.Integer(string="Visit" ,required=False, )
		note = fields.Text(string="Note")

		perangkat_id = fields.One2many(comodel_name="management.maintenance", inverse_name="maintenance_id",
									string="Maintenance", required=False)

		taken_visit = fields.Float(compute="_calc_taken_visit", string="Taken Visit", required=False, )

		@api.depends('perangkat_id','visit')
		def _calc_taken_visit(self):
			for rec in self:
				if rec.visit>0:
					rec.taken_visit = 100 * len(rec.perangkat_id)/rec.visit
				else:
					rec.taken_visit = 0.0

		@api.onchange('visit')
		def onchange_seats(self):
			if self.visit>0:
				self.taken_visit = 100.0 * len(self.perangkat_id)/self.visit
			else:
				self.taken_visit = 0.0