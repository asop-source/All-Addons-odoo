from odoo import fields, api, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.depends('product_uom_qty', 'price_unit')
    def _calc_sub_total(self):
        for i in self:
            qty = i.product_uom_qty
            price = i.price_unit
            sub_total = qty * price
            i.sub_total = sub_total
            i.total = sub_total

    uudp_id = fields.Many2one('uudp', string='UUDP', ondelete='cascade')
    sub_total = fields.Float(string="Sub Total", compute="_calc_sub_total", store=True)
