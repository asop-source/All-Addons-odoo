from odoo import fields, api, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def name_get(self):
        res = []
        for x in self:
            name = '['+x.login+'] '+x.name
            res.append((x.id, name))
        return res

ResUsers()


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    @api.depends('ref', 'name')
    def name_get(self):
        result = []
        for res in self:
            name = res.name
            if res.ref :
                name = '['+res.ref+'] '+name
            result.append((res.id, name))
        return result


    account_analytic_tag_id = fields.Many2one("account.analytic.tag", string="Analytic Tag",track_visibility='always')

ResPartner()