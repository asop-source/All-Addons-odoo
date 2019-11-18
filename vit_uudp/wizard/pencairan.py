from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError
import datetime
from odoo.addons.terbilang import terbilang

class pencairanWizard(models.TransientModel):
	_name = 'pencairan.wizard'

	def _get_active_uudp(self):
		context = self.env.context
		if context.get('active_model') == 'uudp.pencairan':
			return context.get('active_id', False)
		return False

	def _get_active_company(self):
		context = self.env.context
		if context.get('active_model') == 'uudp.pencairan':
			if context.get('active_id', False) :	
				return self.env['uudp.pencairan'].browse(context.get('active_id')).company_id.id

	uudp_pencairan_id = fields.Many2one(comodel_name='uudp.pencairan', 
						  required=False,
					      string='UUDP',
					      default=_get_active_uudp)
	nominal = fields.Float(string="Nominal Pencairan", required=True)
	debit_account_id = fields.Many2one("account.account", string="Different Account", help="Akun di sisi debet (lawan bank/cash)")
	debit_account_notes = fields.Text("Notes", help="Label pada account move line bank/credit")
	company_id = fields.Many2one("res.company", string="Company",default=_get_active_company)
	date = fields.Date(string="Tanggal Pencairan", required=True, default=fields.Date.context_today)
	notes = fields.Text("Notes", help="Label pada account move line bank/credit")

	def action_pencairan(self):
		nominal = self.nominal
		sisa_pencairan = self.uudp_pencairan_id.sisa_pencairan_parsial
		not_confirmed_accounting = self.uudp_pencairan_id.uudp_ids.filtered(lambda x: x.state != 'confirm_accounting')
		if not_confirmed_accounting :
			raise AccessError(_('Ada ajuan yang belum confirm accounting !') )
		now = datetime.datetime.now()
		if nominal <= 0:
			raise UserError(_('Nominal pencairan tidak boleh 0!'))

		if not self.uudp_pencairan_id.sisa_pencairan_parsial and not self.uudp_pencairan_id.journal_entry_ids and nominal > self.uudp_pencairan_id.ajuan_id.total_ajuan:
			raise UserError(_('Nominal pencairan tidak boleh melebihi total ajuan!'))

		if self.uudp_pencairan_id.journal_entry_ids and nominal > sisa_pencairan:
			raise UserError(_('Nominal pencairan tidak boleh melebihi sisa nominal ajuan yang belum dicairkan!'))

		# self._cr.execute("SELECT description FROM uudp_detail WHERE uudp_id=%s" , ( [(self.uudp_pencairan_id.ajuan_id.id)] ))
		# descriptions = self._cr.dictfetchall()
		# des = []
		# for d in descriptions:
		# 	des.append(str(d['description']))

		# all_desciptions = ' '.join(des)
		if not self.uudp_pencairan_id.coa_kredit :
			raise UserError(_('Credit account belum diisi !'))		
		
		account_move_line = []
		debt = self.uudp_pencairan_id.ajuan_id.coa_debit
		if self.debit_account_id :
			debt = self.debit_account_id 
		label_debit = self.debit_account_notes
		if not label_debit :
			label_debit = debt.name
		label_credit = self.notes
		if not label_credit :
			label_credit = self.uudp_pencairan_id.coa_kredit.name
		#account debit
		account_move_line.append((0, 0 ,{'account_id' 	: debt.id, 
										'partner_id'	: self.uudp_pencairan_id.ajuan_id.responsible_id.partner_id.id, 
										'analytic_account_id':self.uudp_pencairan_id.ajuan_id.department_id.analytic_account_id.id,
										'name' 			: label_debit, 
										'debit' 		: self.nominal, 
										'date_maturity' :self.date}))            

		#account credit
		account_move_line.append((0, 0 ,{'account_id' 	: self.uudp_pencairan_id.coa_kredit.id, 
										'partner_id'	: self.uudp_pencairan_id.ajuan_id.responsible_id.partner_id.id, 
										'analytic_account_id':self.uudp_pencairan_id.ajuan_id.department_id.analytic_account_id.id, 
										'name' 			: label_credit, 
										'credit' 		: self.nominal, 'date_maturity':self.date}))

		#create journal entry
		data={"uudp_pencairan_id": self.uudp_pencairan_id.id,
			  "journal_id":self.uudp_pencairan_id.journal_id.id,
			  "ref":self.uudp_pencairan_id.name,
			  "date":self.date,
			  "company_id":self.uudp_pencairan_id.company_id.id,
			  "terbilang": terbilang.terbilang(int(round(self.nominal,0)), "IDR", "id"),
			  "line_ids":account_move_line,}


		journal_entry = self.env['account.move'].create(data)
		if journal_entry:
			journal_entry.post()
			total = 0
			sisa = 0
			for journal in self.uudp_pencairan_id.journal_entry_ids:
				total += journal.amount

			sisa = self.uudp_pencairan_id.ajuan_id.total_ajuan - total

			self.uudp_pencairan_id.write({'sisa_pencairan_parsial':sisa})
			self.uudp_pencairan_id.ajuan_id.write({'total_pencairan':total})

			if total == self.uudp_pencairan_id.ajuan_id.total_ajuan:
				self.uudp_pencairan_id.ajuan_id.write({'state':'done'})
				self.uudp_pencairan_id.write({'state':'done'})
		return journal_entry


class EditAjuanWizard(models.TransientModel):
	_name = 'edit.ajuan.wizard'


	def _get_default_date(self):
		context = self.env.context
		if context.get('active_model') == 'uudp':
			return context.get('active_id', False)
		return False

	date = fields.Date("Date",default=_get_default_date)

EditAjuanWizard()