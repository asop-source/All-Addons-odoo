from datetime import datetime
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_round, float_is_zero


class stockMoveLine(models.Model):
	_name ='stock.move'
	_inherit = 'stock.move'

	lot = fields.Many2one('stock.production.lot','Lot/Serial number', compute='create_data')

	def create_data(self):
		for ress in self:
			data = self.env['stock.production.lot'].search([
				('product_id','=', ress.product_id.id),
				('name', '=', ress.picking_id.origin)
				])
			ress.lot = data.id