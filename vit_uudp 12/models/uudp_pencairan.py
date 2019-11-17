from odoo import api, fields, models, _
import datetime
from odoo.exceptions import UserError, AccessError, ValidationError
# from odoo.addons.terbilang import terbilang


class uudpPencairan(models.Model):
    _name = 'uudp.pencairan'
    _order = 'name desc'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    #########################
    #Fungsi message discuss #
    #########################

    def post_mesages_pencairan(self,state):
        # import pdb;pdb.set_trace();
        ir_model_data_sudo = self.env['ir.model.data'].sudo()

        user_pencairan    = ir_model_data_sudo.get_object('vit_uudp', 'group_user_uudp_pencairan')
        manager_pencairan = ir_model_data_sudo.get_object('vit_uudp', 'group_manager_uudp_pencairan')

        user_pencairan_partner_ids     = user_pencairan.users.mapped('partner_id')
        manager_pencairan_partner_ids  = manager_pencairan.users.mapped('partner_id')

        user_pencairan_partners    =  user_pencairan_partner_ids.ids
        manager_pencairan_partners =  manager_pencairan_partner_ids.ids

        receivers = user_pencairan_partners + manager_pencairan_partners

        subject = _("UUDP Pencairan")
        body = 'UUDP Pencairan ' +str(state)
        messages = self.message_post(body=body, subject=subject)
        messages.update({'needaction_partner_ids' : [(6, 0, list(set(receivers)))]})

        #kirim messages juga ke pengaju bahwa ajuan telah masuk ke tahap pencairan

        if self.type == 'once':
            for uudp in self.uudp_ids:

                subject = _("Pencairan")
                body = 'Pencairan ' +str(state)
                messages = uudp.message_post(body=body, subject=subject)
                messages.update({'needaction_partner_ids' : [(6, 0, [uudp.user_id.partner_id.id])]})

        else:
            subject = _("Pencairan")
            body = 'Pencairan ' +str(state)
            messages = self.ajuan_id.message_post(body=body, subject=subject)
            messages.update({'needaction_partner_ids' : [(6, 0, [self.ajuan_id.user_id.partner_id.id])]})
        return True


    name = fields.Char(string="Nomor Pencairan", readonly=True, default="New")
    tgl_pencairan = fields.Date(string="Tanggal Pencairan", required=True, default=fields.Date.context_today, track_visibility='onchange',)
    user_id = fields.Many2one("res.users", string="User", default=lambda self: self.env.user)
    uudp_ids = fields.Many2many("uudp", string="Detail Ajuan", domain="[('state','=','confirm_finance'),('type','=','pengajuan')]", track_visibility='onchange',)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm_once', 'Confirm'),
                              ('confirm_parsial', 'Confirm'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled'),
                              ('refuse','Refused')], default='draft', required=True, index=True, track_visibility='onchange',)
    journal_id = fields.Many2one("account.journal", string="Journal", required=True, track_visibility='onchange',)
    coa_kredit = fields.Many2one("account.account", string="Account", related="journal_id.default_credit_account_id", help="Credit Account", track_visibility='onchange')
    journal_entry_id = fields.Many2one("account.move", string="Journal Entry", track_visibility='onchange',)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env['res.company']._company_default_get())
    type = fields.Selection([('parsial', 'Parsial'), 
                             ('once', 'At Once'),],string='Type Pencairan', required=True)
    journal_entry_ids = fields.One2many("account.move", string="Journal Entries", inverse_name="uudp_pencairan_id", track_visibility='onchange',)
    ajuan_id = fields.Many2one('uudp', string="Ajuan", track_visibility='onchange',)
    nominal_ajuan = fields.Float(String="Nominal Ajuan", related="ajuan_id.total_ajuan")
    notes = fields.Text(string="Notes", track_visibility='onchange',)
    sisa_pencairan_parsial = fields.Float(string="Sisa Pencairan Parsial")
    total_pencairan = fields.Float(string="Total Pencairan", compute="get_total_pencairan")

    # @api.onchange('uudp_ids')
    # def onchange_uudp_ids(self):
    #     import pdb;pdb.set_trace()
    #     if self.uudp_ids:
    #         active_form = self._context.get('params', False)
    #         if active_form :
    #             exist = self.env['uudp.pencairan'].search([('id','=',active_form['id'])])
    #             todelete = exist.uudp_ids.filtered(lambda x: x.id not in tuple(self.uudp_ids.ids))
    #             for del in todelete :
    #                 del.write({'pencairan_id' : False, 'tgl_pencairan' : False, 'type_pencairan' : False})

    @api.depends('uudp_ids.state','journal_entry_ids.state')
    def get_total_pencairan(self):
        for rec in self:
            total = 0
            if rec.uudp_ids:
                for u in rec.uudp_ids:
                    total += u.total_ajuan
                rec.total_pencairan = total

            elif rec.journal_entry_ids:
                for u in rec.journal_entry_ids:
                    for l in u.line_ids:
                        total += l.credit
                rec.total_pencairan = total


    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('uudp.pencairan') or '/'
        vals['name'] = seq
        return super(uudpPencairan, self).create(vals)

    @api.multi
    def button_confirm(self):
        self.ensure_one()
        if self.type == 'parsial':
            self.ajuan_id.write({'type_pencairan':'parsial','pencairan_id':self.id})
            self.post_mesages_pencairan('Confirmed')
            for uudps in self.uudp_ids :
                uudps.write({'tgl_pencairan': self.tgl_pencairan})
            return self.write({'state' : 'confirm_parsial'})
        elif self.type == 'once':
            for ajuan in self.uudp_ids:
                datas = {'type_pencairan':'once'} 
                # ketika confirm langsung assign
                # if ajuan.cara_bayar == 'cash' :
                datas.update({'total_pencairan'      : ajuan.total_ajuan,
                            'pencairan_id'          : self.id,
                            'tgl_pencairan'         : self.tgl_pencairan,
                            'terbilang'             : terbilang.terbilang(int(round(ajuan.total_ajuan,0)), "IDR", "id"),})    

                ajuan.write(datas)
            self.post_mesages_pencairan('Confirmed')
            return self.write({'state' : 'confirm_once'})

    @api.multi
    def button_cancel(self):
        self.ensure_one()
        if self.type == 'parsial':
            if self.journal_entry_ids:
                raise UserError(_('Pencairan parsial tidak bisa dicancel ketika ajuan sudah pernah dicairkan'))
            self.post_mesages_pencairan('Cancelled')
        elif self.type == 'once':
            if self.uudp_ids:
                for u in self.uudp_ids:
                    if u.state not in ('confirm_accounting','done') :
                        u.write({'type_pencairan':False, 'pencairan_id'  : False, 'tgl_pencairan':False})
        self.post_mesages_pencairan('Cancelled')
        return self.write({'state' : 'cancel'})


    @api.multi
    def button_force_cancel(self):
        self.ensure_one()
        if self.type == 'parsial':
            self.post_mesages_pencairan('Back to Confirm Parsial')
        elif self.type == 'once':
            raise UserError(_('Pencairan once tidak bisa force cancel !'))
        return self.write({'state' : 'confirm_parsial'})

    @api.multi
    def button_set_to_draft(self):
        self.ensure_one()
        self.ajuan_id.write({'type_pencairan' : False,'pencairan_id':False, 'tgl_pencairan':False})
        return self.write({'state' : 'draft'})

    @api.multi
    def button_refuse(self):
        self.ensure_one()
        if self.type == 'parsial':
            if self.journal_entry_ids:
                raise UserError(_('Pencairan parsial tidak bisa direfuse ketika ajuan sudah pernah dicairkan'))
        elif self.type == 'once':
            if self.uudp_ids:
                for u in self.uudp_ids:
                    u.write({'state' : 'refuse'})

        self.post_mesages_pencairan('Refused')
        return self.write({'state' : 'refuse'})

    @api.multi
    def button_done_once(self):
        self.ensure_one()
        total_ajuan = 0
        now = datetime.datetime.now()
        if self.uudp_ids:
            for ajuan in self.uudp_ids:
                tgl_pencairan = self.tgl_pencairan
                if ajuan.tgl_pencairan :
                    tgl_pencairan = ajuan.tgl_pencairan
                #  tansfer tidak langsung create jurnal
                if ajuan.cara_bayar == 'transfer' :
                    datas = {'total_pencairan'          : ajuan.total_ajuan,
                                'state'                 : 'confirm_accounting',
                                'pencairan_id'          : self.id,
                                'tgl_pencairan'         : tgl_pencairan,
                                'terbilang'             : terbilang.terbilang(int(round(ajuan.total_ajuan,0)), "IDR", "id"),}
                    ajuan.write(datas)
                    continue 
                account_move = self.env['account.move']
                reference =  self.name + ' - ' + ajuan.name
                journal_exist = account_move.sudo().search([('ref','=',reference)])
                if not journal_exist :
                #  tansfer langsung create jurnal     
                    account_move_line = []
                    total_kredit = 0
                    # not_confirmed_accounting = ajuan.uudp_ids.filtered(lambda x: x.state != 'confirm_accounting')
                    # if not_confirmed_accounting :
                    #     raise AccessError(_('Ada ajuan yang belum confirm accounting !') )
                    partner = ajuan.responsible_id.partner_id.id
                    for juan in ajuan.uudp_ids :
                        if juan.partner_id :
                            partner = juan.partner_id.id
                        tag_id = False
                        if juan.store_id and juan.store_id.account_analytic_tag_id :
                            tag_id = [(6, 0, [juan.store_id.account_analytic_tag_id.id])]
                        if ajuan.type == 'pengajuan' :
                            debit = ajuan.coa_debit
                            if not debit :
                                raise AccessError(_('Debit acount pada ajuan %s belum diisi !') % (ajuan.name) )
                        else :
                            debit = juan.coa_debit
                            if not debit :
                                raise AccessError(_('Debit Account lines pada ajuan %s belum diisi !') % (ajuan.name) )
                        #account debit
                        if juan.total > 0.0 :
                            account_move_line.append((0, 0 ,{'account_id'       : debit.id,
                                                            'partner_id'        : partner,
                                                            'analytic_account_id' : ajuan.department_id.analytic_account_id.id or False,
                                                            'analytic_tag_ids'  : tag_id,
                                                            'name'              : juan.description,
                                                            'debit'             : juan.total,
                                                            'date'              : tgl_pencairan,
                                                            'date_maturity'     : tgl_pencairan}))
                        elif juan.total < 0.0 :
                            account_move_line.append((0, 0 ,{'account_id'       : debit.id,
                                                            'partner_id'        : partner,
                                                            'analytic_account_id' : ajuan.department_id.analytic_account_id.id or False,
                                                            'analytic_tag_ids'  : tag_id,
                                                            'name'              : juan.description,
                                                            'credit'             : -juan.total,
                                                            'date'              : tgl_pencairan,
                                                            'date_maturity'     : tgl_pencairan}))
                    #account credit bank / hutang
                    notes = ajuan.notes
                    if not notes :
                        notes= self.coa_kredit.name
                    account_move_line.append((0, 0 ,{'account_id'       : self.coa_kredit.id,
                                                    'partner_id'        : ajuan.responsible_id.partner_id.id,
                                                    'analytic_account_id' : ajuan.department_id.analytic_account_id.id or False,
                                                    'name'              : notes,
                                                    'credit'            : ajuan.total_ajuan,
                                                    'date'              : tgl_pencairan,
                                                    'date_maturity'     : tgl_pencairan}))

                    data={"journal_id"  : self.journal_id.id,
                          "ref"         : self.name + ' - ' + ajuan.name,
                          "date"        : tgl_pencairan,
                          "company_id"  : self.company_id.id,
                          "narration"   : self.notes,
                          "terbilang"   : terbilang.terbilang(int(round(ajuan.total_ajuan,0)), "IDR", "id"),
                          "line_ids"    : account_move_line,}

                    journal_entry = self.env['account.move'].create(data)
                    journal_entry.post()
                    if ajuan.state not in ('confirm_accounting','done') :
                        raise AccessError(_('Ajuan %s belum confirm accounting !') % (ajuan.name))
                    ajuan.write({'total_pencairan'      : ajuan.total_ajuan,
                                    'state'             : 'done',
                                    'journal_entry_id'  : journal_entry.id,
                                    'pencairan_id'      : self.id,
                                    'terbilang'         : terbilang.terbilang(int(round(ajuan.total_ajuan,0)), "IDR", "id"),})

        self.post_mesages_pencairan('Done')
        return self.write({'state': 'done'})

    # @api.multi
    # def button_done_once(self):
    #     self.ensure_one()
    #     for ajuan in self.uudp_ids:
    #         ajuan.write({'total_pencairan'      : ajuan.total_ajuan,
    #                             'state'         : 'confirm_accounting',
    #                             'pencairan_id'  : self.id,
    #                             'tgl_pencairan': self.tgl_pencairan,
    #                             'terbilang'     : terbilang.terbilang(int(round(ajuan.total_ajuan,0)), "IDR", "id"),})

    #     self.post_mesages_pencairan('Done')
    #     return self.write({'state': 'done'})

    @api.multi
    def button_done_parsial(self):
        self.ensure_one()
        # if not self.journal_entry_ids:
        #     raise AccessError(_('Ajuan belum pernah dicairkan!') )
        self.ajuan_id.write({'state':'done','total_pencairan' : self.ajuan_id.pencairan_id.total_pencairan})
        self.post_mesages_pencairan('Done')
        return self.write({'state' : 'done'})

    @api.multi
    def unlink(self):
        for ttf in self:
            if ttf.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yang berstatus draft !'))
        return super(uudpPencairan, self).unlink()

uudpPencairan()