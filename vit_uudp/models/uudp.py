from odoo import api, fields, models, exceptions, _
import datetime
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.addons.terbilang import terbilang
import logging
_logger = logging.getLogger(__name__)


class uudp(models.Model):
    _name = 'uudp'
    _order = 'name desc'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


    #########################
    #Fungsi message discuss #
    #########################
    def post_mesages_uudp(self,state):
        # import pdb;pdb.set_trace();
        ir_model_data_sudo = self.env['ir.model.data'].sudo()

        uudp_user    = ir_model_data_sudo.get_object('vit_uudp', 'group_user_uudp_user')
        uudp_manager = ir_model_data_sudo.get_object('vit_uudp', 'group_user_uudp_manager')
        hrd          = ir_model_data_sudo.get_object('hr','group_hr_manager')
        finance      = ir_model_data_sudo.get_object('account','group_account_manager')

        uudp_user_partner_ids     = uudp_user.users.mapped('partner_id')
        uudp_manager_partner_ids  = uudp_manager.users.mapped('partner_id')
        hrd_partner_ids           = hrd.users.mapped('partner_id')
        finance_ids               = finance.users.mapped('partner_id')

        uudp_user_partners    =  uudp_user_partner_ids.ids
        uudp_manager_partners =  uudp_manager_partner_ids.ids
        hrd_partners          =  hrd_partner_ids.ids
        finance_partners      =  finance_ids.ids

        receivers = False
        if self.type == 'pengajuan':
            if self.need_driver == True:
                receivers = uudp_user_partners + uudp_manager_partners + hrd_partners + finance_partners
            else:
                receivers = uudp_user_partners + uudp_manager_partners + finance_partners
        else:
            receivers = uudp_user_partners + finance_partners
        subject = _("UUDP")
        body = 'UUDP '+ str(self.type) + ' ' +str(state)
        messages = self.message_post(body=body, subject=subject)
        if receivers :
            messages.update({'needaction_partner_ids' : [(6, 0, list(set(receivers)))]})
        return True

    ##########################################################################
    #Fungsi write untuk update data state detail berdasarkan state parentnya #
    ##########################################################################

    def write_state_line(self, state):
        line = self.env['uudp.detail'].search([('uudp_id','=',self.id)])
        if line:
            for l in line:
                l.write({'state' : state})

    #######################################################################################################################
    # Fungsi pengecekan total pengajuan UUDP (untuk cek total penyelesaian agar tidak lebih dari pengajuan)               #
    #                                                                                                                     #
    # Di action write terdapat banyak pengecekan, ini untuk mengecek detail penyelesaian, apakah record ada yg diupdate,  #
    # delete ataupun dicreate, semua total nya selanjutnya dijumlah dan dibandingkan dengan total pengajuan uudp          #
    #######################################################################################################################

    def check_total_uudp(self, action, total_ajuan, uudp_id, uudp_detail):
        if action == 'create':

            total = 0
            for i in uudp_detail:
                total += i[2]['total']
            if total > total_ajuan:
                return True
            return False

        elif action == 'write':

            total = 0

            #cari dulu uudp pengajuan nya
            uudp_pengajuan = self.env['uudp'].sudo().search([('id','=',uudp_id)])

            #lalu cari total uudp pengajuannya
            nominal_uudp = self.env['uudp.detail'].sudo().search([('uudp_id','=',uudp_pengajuan.ajuan_id.id)])
            for n in nominal_uudp:
                total += n.total

            nominal_noupdate = 0
            nominal_update = 0
            nominal_create = 0
            total_nominal = 0
            product = self.env['product.product']
            product_uudp = False
            for line in uudp_detail:
                #kode 0 berarti record baru
                #kode 1 berarti record diupdate
                #kode 2 berarti record didelete
                #kode 4 berarti record tidak diupdate ataupun didelete

                if line[0] == 4 :
                    uudp_line = line[1]
                    uudp_noupdate = self.env['uudp.detail'].sudo().search([('uudp_id','=',uudp_id),('id','=',uudp_line)])
                    for k in uudp_noupdate:
                        nominal_noupdate = nominal_noupdate + k.total

                if line[0] == 0 :
                    nominal_create = nominal_create + line[2]['total']
                    if 'product_id' in line[2] :
                        uudp_exist = product.browse(line[2]['product_id']).name
                        if uudp_exist in ('Piutang UUDP','PIUTANG UUDP') :
                            product_uudp = line[2]['total']
                if line[0] == 1 and 'total' in line[2]:
                    nominal_update = nominal_update + line[2]['total']
                    if 'product_id' in line[2] :
                        uudp_exist = product.browse(line[2]['product_id']).name
                        if uudp_exist in ('Piutang UUDP','PIUTANG UUDP') :
                            product_uudp = line[2]['total']

                if line[0] == 1 and 'total' not in line[2]:
                    line_id = line[1]
                    uudp_update = self.env['uudp.detail'].sudo().search([('uudp_id','=',uudp_id),('id','=',line_id)])
                    for uu in uudp_update:
                        nominal_update = nominal_update + uu.total

                total_nominal = nominal_noupdate + nominal_create + nominal_update
            if uudp_pengajuan.state != 'draft' and uudp_pengajuan.type == 'penyelesaian':
                total_awal = sum(uudp_pengajuan.uudp_ids.mapped('sub_total'))
                if total_nominal > total_awal :
                    sisa_awal = uudp_pengajuan.sisa_penyelesaian
                    sisa_sekarang = uudp_pengajuan.total_ajuan_penyelesaian - total_nominal
                    if product_uudp :
                        if product_uudp != sisa_awal :
                            raise UserError(_('Selain status draft, sisa penyelesaian (%s) harus sama dengan lines Piutang UUDP !')%(sisa_awal))
                    else :
                        raise UserError(_('Selain status draft, sisa penyelesaian (%s) tidak bisa dikurangi (%s) !')%(sisa_awal,sisa_sekarang))
            if round(total_nominal,2) > round(total,2):
                return True
            return False

    #######################################################
    # Default journal untuk uudp berdasarkan company user #
    #######################################################

    def _default_journal(self):
        return self.env.context.get('default_journal_id') or self.env['account.journal'].search([('name', 'ilike', 'Miscellaneous Operation'),
                                                                                              ('company_id','=',self.env['res.company']._company_default_get().id)], limit=1)

    ################################################################
    # Proteksi tidak bisa membuat pengajuan untuk penerima yg sama # 
    # ketika ajuan sebelumnya belum selesai                        #
    ################################################################

    def check_unfinished_submission(self, user_id):
        # import pdb;pdb.set_trace();
        myajuan = self.env['uudp'].sudo().search([('responsible_id','=',user_id),
                                            ('type','=','pengajuan'),
                                            ('id','!=',self.id),
                                            ('state', 'not in', ['refuse','cancel','done','confirm_finance','confirm_accounting'])],
                                             limit=10, order='id desc')
        if myajuan:
            amount = len(myajuan)
            if amount >= 1:
                for m in myajuan:
                    unfinished = self.env['uudp'].sudo().search([('ajuan_id','=',m.id),('type','=','penyelesaian'),('state','=','done')])
                    if not unfinished:
                        raise ValidationError(_("Anda tidak bisa membuat pengajuan untuk penerima yg sama (%s), ketika ajuan sebelumnya (%s) belum penyelesaian (3)!") % (m.responsible_id.name, m.name))
        return True

    @api.multi
    def _subscribe_assigned_to_user(self, subtype_ids=None):
        """If the responsible user, subscribe it."""
        for rec in self:
            if not rec.responsible_id:
                continue
            rec.message_subscribe(partner_ids=[rec.responsible_id.partner_id.id], channel_ids=None, subtype_ids=subtype_ids)
            # rec.message_subscribe_users(
            #     user_ids=[rec.responsible_id.id], subtype_ids=subtype_ids)

    @api.onchange('ajuan_id')
    def onchange_ajuan_id(self):
        if self.ajuan_id:
            ajuan = []
            for juan in self.ajuan_id.uudp_ids :
                ajuan.append([0,0,{'description'    : juan.description,
                                    'qty'           : juan.qty,
                                    'uom'           : juan.uom,
                                    'unit_price'    : juan.unit_price,
                                    'state'         : 'draft',
                                    }])
            self.uudp_ids = ajuan
            self.coa_kredit = juan.coa_debit.id

    name = fields.Char(string="Code", default="New", readonly=True)
    user_id = fields.Many2one("res.users", string="Employee", default=lambda self: self.env.user, store=True, required=True, track_visibility='onchange',)
    department_id = fields.Many2one("hr.department", string="Department", track_visibility='onchange',)
    company_id = fields.Many2one("res.company", string="Company",default=lambda self: self.env['res.company']._company_default_get(), required=True)
    type = fields.Selection([('pengajuan', 'Pengajuan'), 
                             ('penyelesaian', 'Penyelesaian'), 
                             ('reimberse', 'Reimberse'),],string='Type', required=True, track_visibility='onchange',)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Waiting Department'),
                              ('confirm_department', 'Confirmed Department'),
                              ('confirm_department1', 'Waiting HRD'),
                              ('confirm_hrd', 'Confirmed HRD'),
                              ('pending', 'Pending'),
                              ('confirm_finance', 'Confirmed Finance'),
                              ('confirm_accounting', 'Confirmed Accounting'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled'),
                              ('refuse','Refused')], default='draft', required=True, index=True, track_visibility='onchange',)
    uudp_ids = fields.One2many("uudp.detail", inverse_name="uudp_id", track_visibility='onchange',)
    coa_debit = fields.Many2one("account.account", string="Debit Account")
    coa_kredit = fields.Many2one("account.account", string="Credit Account")
    ajuan_id = fields.Many2one('uudp', string="Ajuan", domain="[('type','=','pengajuan')]")
    total_ajuan = fields.Float(string="Total Ajuan", track_visibility='onchange', compute="_get_total_ajuan")
    total_ajuan_penyelesaian = fields.Float(string="Total Pencairan", related="ajuan_id.total_pencairan", readonly=True, track_visibility='onchange',)
    need_driver = fields.Boolean(string="Need a driver?", track_visibility='onchange',)
    selesai = fields.Boolean(string="Selesai")
    journal_id = fields.Many2one("account.journal", string="Journal", track_visibility='onchange')# default=_default_journal)
    journal_entry_id = fields.Many2one("account.move", string="Journal Entry")
    difference = fields.Many2one("account.account", string="Difference Account", track_visibility='onchange')
    difference_notes = fields.Char("Difference Notes", track_visibility='onchange')
    responsible_id = fields.Many2one("res.users", string="Responsible")
    cara_bayar = fields.Selection([('cash', 'Cash'), 
                                   ('transfer', 'Transfer'),],string='Cara Bayar', track_visibility='onchange',)
    bank_id = fields.Many2one("res.bank", string="Bank", track_visibility='onchange',)
    no_rekening = fields.Char(string="Nomor Rekening", track_visibility='onchange',)
    atas_nama = fields.Char(string="Atas Nama", track_visibility='onchange',)
    notes = fields.Text(string="Notes", track_visibility='onchange')
    total_pencairan = fields.Float(string="Total Pencairan", track_visibility='onchange',)
    type_pencairan = fields.Selection([('once', 'Once'), 
                                       ('parsial', 'Parsial'),],string='Type Pencairan')
    date = fields.Date(string="Required Date", required=True, default=fields.Date.context_today, track_visibility='onchange',)
    terbilang = fields.Char(string='Terbilang', translate=True, readonly=True, states={'draft': [('readonly', False)]})
    is_user_pencairan = fields.Boolean(compute="check_validity")
    pencairan_id = fields.Many2one("uudp.pencairan","Pencairan")
    tgl_pencairan = fields.Date("Tanggal Pencairan",)# related="pencairan_id.tgl_pencairan", store=True)
    sisa_penyelesaian = fields.Float("Sisa Penyelesaian", compute="_get_sisa_penyelesaian", store=True,track_visibility='onchange')
    end_date = fields.Date(string="End Date",  track_visibility='onchange',)
    by_pass_selisih = fields.Boolean("By Pass Different Amount",  track_visibility='onchange')
    selesai_id = fields.Many2one('uudp','Selesai ID',compute="search_input_penyelesaian")
    penyelesaian_id = fields.Many2one('uudp','Penyelesaian')# store ke db
    tgl_penyelesaian = fields.Date("Tgl Penyelesaian")


    @api.depends('uudp_ids')
    def _get_total_ajuan(self):
        for rec in self:
            rec.total_ajuan = sum(rec.uudp_ids.mapped('sub_total'))

    @api.depends('uudp_ids.qty','uudp_ids.unit_price','uudp_ids.sub_total')
    def _get_sisa_penyelesaian(self):
        for rec in self:
            total = 0
            for u in rec.uudp_ids:
                total += (u.unit_price*u.qty)
            rec.sisa_penyelesaian = rec.ajuan_id.total_pencairan-total

    @api.depends('is_user_pencairan')
    def check_validity(self):
        for rec in self:
            user_login = self.env.user.id
            res_user = self.env['res.users'].sudo().search([('id', '=',user_login)])
            if res_user.has_group('vit_uudp.group_user_uudp_pencairan') or res_user.has_group('vit_uudp.group_manager_uudp_pencairan'):
                rec.is_user_pencairan = True
            else:
                rec.is_user_pencairan = False

    def search_input_penyelesaian(self):
        #import pdb;pdb.set_trace()
        for rec in self:
            penyelesaian_exist = self.env['uudp'].sudo().search([('ajuan_id', '=',rec.id),('state','!=','refuse')],limit=1)
            if penyelesaian_exist :
                rec.penyelesaian_id = penyelesaian_exist.id
                self.env.cr.execute("update uudp set penyelesaian_id=%s, tgl_penyelesaian=%s where id = %s",
                        ( penyelesaian_exist.id, penyelesaian_exist.date, rec.id,))

    @api.model
    def _get_identifier(self, type):
        result = ""
        if type == "pengajuan":
            result = self.env['ir.sequence'].get('uudp_pengajuan_sequence')
        elif type == "penyelesaian":
            result = self.env['ir.sequence'].get('uudp_penyelesaian_sequence')
        else:
            result = self.env['ir.sequence'].get('uudp_reimburse_sequence')
        return result

    @api.model
    def create(self, vals):
        # import pdb;pdb.set_trace()
        if vals['type'] == 'pengajuan':
            user_id = vals['responsible_id']
            self.check_unfinished_submission(user_id)

        if vals['type'] == 'penyelesaian':

            action = 'create'
            total_ajuan = vals['total_ajuan']
            uudp_detail = vals['uudp_ids']

            error = self.check_total_uudp(action, total_ajuan, False, uudp_detail)
            if error:
                raise ValidationError(_("Total penyelesaian melebihi total pengajuan!"))


        # seq = self.env['ir.sequence'].next_by_code('uudp') or '/'
        vals['name'] = self._get_identifier(vals['type'])

        res = super(uudp, self).create(vals)
        res._subscribe_assigned_to_user()
        total = 0
        coaDebit = False
        # import pdb;pdb.set_trace()
        uudpLine = self.env['uudp.detail'].search([('uudp_id','=',res.id)])
        if uudpLine:
            for g in uudpLine:
                total += g.sub_total
        if res.type != 'penyelesaian':
            res.write({'total_ajuan': total})
        if res.type == 'reimberse':
            res.write({'total_pencairan':total})
        return res

    @api.model
    def write(self, vals, context=None):
        if context != None:
            if 'responsible_id' in context:
                user_id = context['responsible_id']
                if self.type == 'pengajuan' :
                    self.check_unfinished_submission(user_id)

            action = 'write'
            uudp_id = vals[0]
            error = False
            this_uudp = self.env['uudp'].sudo().search([('id','=',uudp_id)])

            # protek hanya user accounting yg bisa edit ketika status selain draft
            if this_uudp.state != 'draft':
                if not self.env.user.has_group('account.group_account_manager') :
                    raise ValidationError(_("Data yang bisa di edit hanya yang berstatus 'Draft' !"))

            # import pdb;pdb.set_trace()
            if 'uudp_ids' in context and this_uudp.type == 'penyelesaian':
                uudp_detail = context['uudp_ids']

                error = self.check_total_uudp(action, False, uudp_id, uudp_detail)

            if error:
                raise ValidationError(_("Total penyelesaian melebihi total pengajuan!"))
            else:
                for tu in this_uudp:
                    total = 0
                    res = tu.write(context)
                    sub = self.env['uudp'].sudo().search([('id','=',uudp_id)])
                    sub._subscribe_assigned_to_user()
                    get_total = self.env['uudp.detail'].sudo().search([('uudp_id','=',tu.id)])
                    for g in get_total:
                        total += g.sub_total
                    if tu.type != 'penyelesaian':
                        res = tu.write({'total_ajuan':total})
                    if tu.type == 'reimberse':
                        res = tu.write({'total_pencairan':total})

                    if res:
                        return True
                    else:
                        return False
        return super(uudp, self).write(vals)

    @api.multi
    def button_confirm(self):
        if self.type == 'reimberse':
            attachment = self.env['ir.attachment'].sudo().search([('res_model','=','uudp'),('res_id','=',self.id)])
            if not attachment:
                raise UserError(_('Attachment masih kosong, silahkan lampirkan file / dokumen pendukung untuk melanjutkan.'))

        self.write_state_line('confirm')
        self.post_mesages_uudp('Confirmed')
        return self.write({'state' : 'confirm'})

    @api.multi
    def button_pending(self):
        self.write_state_line('pending')
        self.post_mesages_uudp('Pending')
        return self.write({'state' : 'pending'})

    @api.multi
    def button_re_confirm_department(self):
        if self.env.user.id != self.department_id.manager_id.user_id.id:
            raise UserError(_('Hanya manager department yang bisa confirm pengajuan'))
        else:
            self.write_state_line('confirm_department')
            self.post_mesages_uudp('Confirmed by Manager')
            return self.write({'state' : 'confirm_department'})

    @api.multi
    def button_confirm_department(self):
        if not self.env.user.has_group('account.group_account_manager') :
            #cek apakah user yg login adalah manager department atau bukan, jika bukan akan muncul warning ketika button confirm ditekan
            if self.env.user.id != self.department_id.manager_id.user_id.id:
                raise UserError(_('Hanya manager department yang bisa confirm pengajuan'))
        if self.need_driver:
            self.write_state_line('confirm_department1')
            self.post_mesages_uudp('Confirmed by Manager')
            return self.write({'state' : 'confirm_department1'})
        else:
            self.write_state_line('confirm_department')
            self.post_mesages_uudp('Confirmed by Manager')
            return self.write({'state' : 'confirm_department'})

    @api.multi
    def button_done_finance(self):
        if self.type == 'penyelesaian':
            partner = self.ajuan_id.responsible_id.partner_id.id
            total_ajuan = 0
            now = datetime.datetime.now()
            total_ajuan = self.total_ajuan
            if self.uudp_ids:
                account_move_line = []

                # sql = "SELECT account_account.name, udel.coa_debit, udel.description, SUM(udel.total) AS total FROM uudp_detail AS udel INNER JOIN uudp ON uudp.id = udel.uudp_id INNER JOIN account_account ON udel.coa_debit = account_account.id WHERE udel.uudp_id=%s GROUP BY udel.coa_debit, account_account.name, udel.description"

                # cr = self.env.cr
                # cr.execute(sql, ([(self.id)]))
                # result = self.env.cr.dictfetchall()
                total_debit = 0.0
                for ajuan in self.uudp_ids:
                    if not ajuan.coa_debit:
                        raise UserError(_('Account atas %s belum di set!')%(ajuan.description))
                    if ajuan.partner_id :
                        partner = ajuan.partner_id.id
                    tag_id = False
                    if ajuan.store_id :
                        tag_id = [(6, 0, [ajuan.store_id.account_analytic_tag_id.id])]
                    ajuan_total = ajuan.sub_total
                    #account debit
                    if ajuan.sub_total > 0.0 :
                        account_move_line.append((0, 0 ,{'account_id'       : ajuan.coa_debit.id,
                                                         'partner_id'       : partner, 
                                                         'analytic_tag_ids' : tag_id,
                                                         'name'             : ajuan.description, 
                                                         'analytic_account_id': self.department_id.analytic_account_id.id,
                                                         'debit'            : ajuan_total, 
                                                         'date_maturity'    : self.date})) #,
                    elif ajuan.sub_total < 0.0 :
                        account_move_line.append((0, 0 ,{'account_id'       : ajuan.coa_debit.id,
                                                         'partner_id'       : partner, 
                                                         'analytic_tag_ids' : tag_id,
                                                         'name'             : ajuan.description, 
                                                         'analytic_account_id': self.department_id.analytic_account_id.id,
                                                         'credit'            : -ajuan_total, 
                                                         'date_maturity'    : self.date})) #,
                    total_debit += ajuan_total    

                # if not self.by_pass_selisih:
                #     if total_debit < total_ajuan and not self.difference: 
                #         raise AccessError(_('Nilai penyelesaian kurang dari nilai ajuan \n Silahkan isi Difference Account untuk memasukan selisih ke journal entry'))
                if round(self.sisa_penyelesaian,2) > 0.0:
                    raise AccessError(_('Sisa penyelesaian harus tetap dimasukan ke detail penyelesaian !'))


                    ################# komen dulu , selisih dimasukan leawat bank statement ###########################
                #     elif total_debit < total_ajuan and self.difference:
                #         selisih = total_ajuan - total_debit
                #         account_move_line.append((0, 0 ,{'account_id'       : self.difference.id, 
                #                                         'partner_id'        : partner, 
                #                                         'analytic_account_id': self.department_id.analytic_account_id.id,
                #                                         'name'              : self.difference_notes, 
                #                                         'debit'             : selisih, 
                #                                         'date_maturity'     :self.date})) #, 
                # else :
                #     total_ajuan = total_debit

                #account credit
                account_move_line.append((0, 0 ,{'account_id' : self.ajuan_id.coa_debit.id, 
                                                'partner_id': partner, 
                                                'analytic_account_id':self.department_id.analytic_account_id.id,
                                                'name' : self.notes, 
                                                # 'credit' : total_ajuan, 
                                                'credit' : total_debit, 
                                                'date_maturity':self.date})) #, 

                #create journal entry
                journal_id = self.ajuan_id.pencairan_id.journal_id
                if not journal_id :
                    journal_id = self.env['account.move'].sudo().search([('ref','ilike','%'+self.ajuan_id.name+'%')],limit=1)
                    if not journal_id :
                        raise AccessError(_('Journal pencairan tidak ditemukan !'))
                    journal_id = journal_id.journal_id
                data={"journal_id":journal_id.id,
                      "ref":self.name + ' - '+ self.ajuan_id.name,
                      "date":self.date,
                      "narration" : self.notes,
                      "company_id":self.company_id.id,
                      "line_ids":account_move_line,}

                journal_entry = self.env['account.move'].create(data)
                if journal_entry:
                    journal_entry.post()
                    self.write_state_line('done')
                    self.ajuan_id.write({'selesai':True})
                    self.post_mesages_uudp('Done')
                    return self.write({'state' : 'done', 'journal_entry_id':journal_entry.id})
                else:
                    raise AccessError(_('Gagal membuat journal entry') )
                return self.write({'state' : 'done'})

    @api.multi
    def button_confirm_finance(self):
        if self.uudp_ids:
            account = self.env['account.account'].sudo()
            for s in self.uudp_ids:
                if not s.product_id :
                    raise UserError(_('Product dengan deskripsi %s belum di set!')%(s.description))
                # if self.type == 'penyelesaian' and self.sisa_penyelesaian > 0.0 and not self.difference:
                #     raise UserError(_('Jika ada sisa penyelesaian, difference account harus diisi !'))
                if self.type == 'penyelesaian' and round(self.sisa_penyelesaian,2) > 0.0 :
                    raise UserError(_('Selisih harus dimasukan ke piutang uudp !'))
                elif s.product_id.property_account_expense_id:
                    uudp_account = account.sudo().search([('code','=',s.product_id.property_account_expense_id.code),
                                                            ('company_id','=',self.company_id.id)],limit=1)
                    if not uudp_account :
                        raise UserError(_('Tidak ditemukan kode CoA %s pada company %s !') % (s.product_id.property_account_expense_id.code,self.company_id.name))
                    self.write({'coa_debit': uudp_account.id})
                elif s.product_id.categ_id.property_account_creditor_price_difference_categ:
                    uudp_account = account.sudo().search([('code','=',s.product_id.categ_id.property_account_creditor_price_difference_categ.code),
                                                    ('company_id','=',self.company_id.id)],limit=1)
                    if not uudp_account :
                        raise UserError(_('Tidak ditemukan kode CoA %s pada company %s !') % (s.product_id.categ_id.property_account_creditor_price_difference_categ.code,self.company_id.name))
                    self.write({'coa_debit': uudp_account.id})
                else:
                    if not s.coa_debit :
                        raise UserError(_('Account atas deskipsi %s belum di set!')%(s.description))
            self.write_state_line('confirm_finance')
            self.post_mesages_uudp('Confirmed by Finance')
            return self.write({'state' : 'confirm_finance'})
        raise AccessError(_('Pengajuan masih kosong') )

    @api.multi
    def button_confirm_accounting(self):
        if self.uudp_ids:
            if self.type != 'pengajuan' :
                account_debit = self.uudp_ids.filtered(lambda x: not x.coa_debit)
                if account_debit :
                    raise UserError(_('Salah satu account lines belum di set!'))
            self.write_state_line('confirm_accounting')
            self.post_mesages_uudp('Confirmed by Accounting')
            return self.write({'state' : 'confirm_accounting'})
        raise AccessError(_('Pengajuan masih kosong'))

    @api.multi
    def button_validate(self):
        self.ensure_one()
        total_ajuan = 0.0
        now = datetime.datetime.now()
        partner = self.responsible_id.partner_id.id
        if self.state != 'confirm_accounting' or not self.pencairan_id:
            raise AccessError(_('Ajuan %s belum confirm accounting atau belum dijadwalkan pencairan!') % (self.name))

        reference =  self.pencairan_id.name + ' - ' + self.name
        account_move = self.env['account.move']
        datas_form = {'state' : 'done'}
        # cek jika journal sdh di create
        journal_exist = account_move.sudo().search([('ref','=',reference)])
        if not journal_exist :
            account_move_line = []
            for juan in self.uudp_ids :
                if juan.partner_id :
                    partner = juan.partner_id.id
                tag_id = False
                if juan.store_id and juan.store_id.account_analytic_tag_id :
                    tag_id = [(6, 0, [juan.store_id.account_analytic_tag_id.id])]
                if self.type == 'pengajuan' :
                    debit = self.coa_debit
                    if not debit :
                        raise AccessError(_('Debit acount pada ajuan %s belum diisi !') % (self.name) )
                else :
                    debit = juan.coa_debit
                    if not debit :
                        raise AccessError(_('Debit Account lines pada ajuan %s belum diisi !') % (self.name) )
                #account debit
                if juan.sub_total > 0.0 :
                    account_move_line.append((0, 0 ,{'account_id'       : debit.id,
                                                    'partner_id'        : partner,
                                                    'analytic_account_id' : self.department_id.analytic_account_id.id or False,
                                                    'analytic_tag_ids'  : tag_id,
                                                    'name'              : juan.description,
                                                    'debit'             : juan.sub_total,
                                                    'company_id'        : self.company_id.id,
                                                    'date'              : self.pencairan_id.tgl_pencairan,
                                                    'date_maturity'     : self.pencairan_id.tgl_pencairan}))
                elif juan.sub_total < 0.0 :
                    account_move_line.append((0, 0 ,{'account_id'       : debit.id,
                                                    'partner_id'        : partner,
                                                    'analytic_account_id' : self.department_id.analytic_account_id.id or False,
                                                    'analytic_tag_ids'  : tag_id,
                                                    'name'              : juan.description,
                                                    'credit'            : -juan.sub_total,
                                                    'date'              : self.pencairan_id.tgl_pencairan,
                                                    'company_id'        : self.company_id.id,
                                                    'date_maturity'     : self.pencairan_id.tgl_pencairan}))
                #account credit bank / hutang
                notes = self.notes
                if not notes :
                    notes= self.coa_kredit.name
            account_move_line.append((0, 0 ,{'account_id'       : self.pencairan_id.coa_kredit.id,
                                            'partner_id'        : self.responsible_id.partner_id.id,
                                            'analytic_account_id' : self.department_id.analytic_account_id.id or False,
                                            'name'              : notes,
                                            'credit'            : self.total_ajuan,
                                            'company_id'        : self.company_id.id,
                                            'date'              : self.pencairan_id.tgl_pencairan,
                                            'date_maturity'     : self.pencairan_id.tgl_pencairan}))

            data={"journal_id": self.pencairan_id.journal_id.id,
                  "ref": reference,
                  "date": self.pencairan_id.tgl_pencairan,
                  "company_id": self.company_id.id,
                  "narration": self.pencairan_id.notes,
                  "terbilang" : terbilang.terbilang(int(round(self.total_ajuan,0)), "IDR", "id"),
                  "line_ids":account_move_line,}

            journal_entry = account_move.create(data)
            journal_entry.post()
            datas_form.update({'journal_entry_id' : journal_entry.id})

        self.post_mesages_uudp('Done')
        return self.write(datas_form)

    @api.multi
    def button_confirm_hrd(self):
        self.write_state_line('confirm_hrd')
        self.post_mesages_uudp('Confirmed by HRD')
        return self.write({'state' : 'confirm_hrd'})

    @api.multi
    def button_cancel(self):
        self.write_state_line('cancel')
        self.post_mesages_uudp('Canceled')
        return self.write({'state' : 'cancel'})

    @api.multi
    def button_set_to_draft(self):
        self.write_state_line('draft')
        return self.write({'state' : 'draft'})

    @api.multi
    def button_refuse(self):
        self.write_state_line('refuse')
        self.post_mesages_uudp('Refused')
        return self.write({'state' : 'refuse'})

    @api.multi
    def button_refuse_finance(self):
        self.write_state_line('refuse')
        self.post_mesages_uudp('Refused')
        return self.write({'state' : 'refuse'})

    @api.onchange('ajuan_id')
    def _get_detail_ajuan(self):
        ajuan = self.ajuan_id
        if ajuan:
            self.total_ajuan = ajuan.total_pencairan
            self.total_pencairan = ajuan.total_pencairan
            self.responsible_id = ajuan.responsible_id.id
            self.cara_bayar = ajuan.cara_bayar
            self.bank_id = ajuan.bank_id.id
            self.no_rekening = ajuan.no_rekening
            self.coa_kredit = ajuan.coa_debit.id

    @api.onchange('responsible_id')
    def _get_department(self):
        responsible = self.responsible_id.id
        if responsible:
            department = self.env['hr.employee'].search([('user_id', '=', responsible)], limit=1).department_id.id
            self.department_id = department

    @api.multi
    def unlink(self):
        for data in self:
            if data.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yang berstatus draft !'))
            else:
                attachment = self.env['ir.attachment'].search([('res_model','=','uudp'),('res_id','=',data.id)])
                if attachment:
                    for a in attachment:
                        a.unlink()
        return super(uudp, self).unlink()

    @api.multi
    def print_pencairan(self):
        view_id = self.env.ref('vit_uudp.view_print_pencairan_wizard').id
        return {
            'name': _('Pencairan Details'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.print.pencairan',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
            'res_id': self.ids[0],
            'context': self.env.context}

    @api.multi
    def alert_uudp_penyelesaian(self, *args):
        """ fungsi di overide di addons vit_uudp+pencairan"""
        return True


uudp()


class uudpDetail(models.Model):
    _name = "uudp.detail"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    uudp_id = fields.Many2one("uudp", string="Nomor UUDP", track_visibility='onchange',)
    product_id = fields.Many2one("product.product", string="Product", track_visibility='onchange',)
    partner_id = fields.Many2one("res.partner", string="Partner", track_visibility='onchange')
    store_id = fields.Many2one("res.partner", string="Store", track_visibility='onchange')
    description = fields.Char(string="Description", required=True, track_visibility='onchange',)
    qty = fields.Float(string="Qty", required=True, default=1, track_visibility='onchange',)
    uom = fields.Char(string="UoM", required=True, track_visibility='onchange', default="Pcs")
    unit_price = fields.Float(string="Unit Price", required=True, default=0, track_visibility='onchange',)
    sub_total = fields.Float(string="Sub Total", compute="_calc_sub_total", store=True)
    total = fields.Float(string="Total", track_visibility='onchange',)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Waiting Department'),
                              ('confirm_department', 'Confirmed Department'),
                              ('confirm_department1', 'Waiting HRD'),
                              ('confirm_hrd', 'Confirmed HRD'),
                              ('pending', 'Pending'),
                              ('confirm_finance', 'Confirmed Finance'),
                              ('confirm_accounting', 'Confirmed Accounting'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled'),
                              ('refuse','Refused')], default='draft', required=True, index=True, track_visibility='onchange',)
    coa_debit = fields.Many2one('account.account', string="Account", track_visibility='onchange')

    @api.onchange('product_id')
    def _get_product_detail(self):
        product = self.product_id
        if product:
            #self.description = p.name
            if not self.uom :
                self.uom = product.uom_id.name
            if self.unit_price == 0.0 :
                self.unit_price = product.lst_price
            # if not self.coa_debit :
            self.coa_debit = product.property_account_expense_id.id


    @api.depends('qty','unit_price','state')
    def _calc_sub_total(self):
        for i in self:
            qty = i.qty
            price = i.unit_price
            sub_total = qty * price
            i.sub_total = sub_total
            i.total = sub_total

    @api.model
    def create(self, vals):
        #import pdb;pdb.set_trace()
        if vals['qty'] == 0.0 or vals['unit_price'] == 0.0:
            raise ValidationError(_("Unit price tidak boleh di isi 0 !"))
        return super(uudpDetail, self).create(vals)

uudpDetail()
