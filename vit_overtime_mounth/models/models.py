# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
# from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class vit_overtime_mounth(models.Model):
	_name = "hr.overtime"
	_inherit = "hr.overtime"


	@api.onchange('date_from')
	def _calc_date(self):
		if self.date_from != 0:
			self.date_to = self.date_from + relativedelta(months=1)