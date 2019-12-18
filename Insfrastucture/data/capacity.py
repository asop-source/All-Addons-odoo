from odoo import api, fields, models, _

class Capacity(models.Model):
	_name='management.capacity'

	def _get_default_perangkat(self):
		context = self.env.context
		if context.get('active_model') == 'management.perangkatdc':
			return context.get('active_ids', False)
		return False

	perangkat_id = fields.Many2many(comodel_name="management.perangkatdc", string="Daftar Perangkat",
									required=False, default=_get_default_perangkat)

	name = fields.Many2one(comodel_name="master.ruang",
							string="Ruang")
	rack = fields.Many2one(comodel_name="master.rack",
							string="Lokasi Rack")
	available =fields.Integer(string="Available",)

	

	taken_available = fields.Float(compute="_calc_taken_available", string="Taken Available", required=False, )

	taken_used = fields.Integer(compute="onchange_used", string="Used", required=False, )

	@api.depends('perangkat_id','available')
	def _calc_taken_available(self):
		for rec in self:
			if rec.available>0:
				rec.taken_available = 100 * len(rec.perangkat_id)/rec.available
			else:
				rec.taken_available = 0.0

	@api.onchange('perangkat_id')
	def onchange_used(self):
		for rec in self:
			rec.taken_used = len(rec.perangkat_id)


