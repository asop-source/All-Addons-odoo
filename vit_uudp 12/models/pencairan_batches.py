from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError, AccessError, ValidationError
# from odoo.addons.terbilang import terbilang


class pencairanBatches(models.Model):
    _name = 'pencairan.batches'
    _order = 'name desc'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, track_visibility='onchange')
    start_date = fields.Date(string="Start Date", track_visibility='onchange')
    end_date = fields.Date(string="End Date", track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Waiting Approval'),
                              ('done', 'Done'),], default='draft', required=True, index=True, track_visibility='onchange',)
    date_planned = fields.Date(string="Tanggal Rencana Bayar", track_visibility='onchange', required=True)
    bank_id = fields.Many2one("account.journal", string="Bank", track_visibility='onchange', required=True)
    pencairan_ids = fields.Many2many("uudp.pencairan", string="Pencairans", track_visibility='onchange',)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env['res.company']._company_default_get(), required=True)

    @api.multi
    def button_done(self):
        if not self.pencairan_ids:
            raise AccessError(_('Line pencairan masih kosong!') )
        for p in self.pencairan_ids:
            p.write({'coa_kredit':self.bank_id.default_credit_account_id.id})
            p.button_done_once()
        return self.write({'state':'done'})

    @api.multi
    def button_confirm(self):
        return self.write({'state':'confirm'})

    @api.multi
    def add_pencairan(self):
        self._cr.execute("DELETE FROM pencairan_batches_uudp_pencairan_rel WHERE pencairan_batches_id = %s" , ( [(self.id)] ))
        if self.start_date and not self.end_date:
            pencairans = self.env['uudp.pencairan'].search([('type','=','once'),('state','=','confirm_once'),('tgl_pencairan','>=',self.start_date)])
        elif not self.start_date and self.end_date:
            pencairans = self.env['uudp.pencairan'].search([('type','=','once'),('state','=','confirm_once'),('tgl_pencairan','<=',self.end_date)])
        elif self.start_date and self.end_date:
            pencairans = self.env['uudp.pencairan'].search([('type','=','once'),('state','=','confirm_once'),('tgl_pencairan','>=',self.start_date),('tgl_pencairan','<=',self.end_date)])
        else:
            pencairans = self.env['uudp.pencairan'].search([('type','=','once'),('state','=','confirm_once')])
        if not pencairans:
            raise AccessError(_('Data pencairan tidak ditemukan!') )
        self.pencairan_ids = [(6, 0, pencairans.ids)]

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yang berstatus draft !'))
        return super(pencairanBatches, self).unlink()