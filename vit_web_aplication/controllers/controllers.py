from odoo import http
from odoo.http import request
import simplejson
import time

class VitWebAplication(http.Controller):

	# @http.route('/vit/attachment',type='http' , auth='public', website=True)
	# def index_attachment(self, **kw):
	# 	ir_attachment = request.env['ir.attachment'].search([])
	# 	return request.render("vit_web_aplication.index_attachment", {
	# 		'ir_attachment': ir_attachment
	# 		})


	# @http.route('/vit/attachment',type='http' , auth='public', website=True)
	# def index_attachment(self, **kw):
	# 	ir_attachment = request.env['ir.attachment'].search([])
	# 	return request.render("vit_web_aplication.index_attachment", {
	# 		})

	# @http.route('/vit/ir_ajax',type='http' , auth='public', website=True)
	# def ir_ajax(self, **kw):
	# 	ir_attachment = request.env['ir.attachment'].search([])
	# 	result = {}
	# 	result ['data'] = []
	# 	for name in ir_attachment:
	# 		result['data'].append([
	# 			name.name,
	# 			name.datas_fname,
	# 			name.res_model,
	# 			name.res_field,
	# 			name.res_id,
	# 			name.type,
	# 			name.create_uid.name,
	# 			name.create_date,
	# 		])
	# 	return simplejson.dumps(result, default=str)

	# membuat ajax
	@http.route('/vit/applicant',type='http' , auth='public', website=True)
	def index(self, **kw):
		web_applicant = request.env['hr.applicant'].search([])
		return request.render("vit_web_aplication.index", {
			})

	@http.route('/vit/web_ajax',type='http' , auth='public', website=True)
	def web_ajax(self, **kw):
		web_applicant = request.env['hr.applicant'].search([])
		result = {}
		result ['data'] = []
		for aplicant in web_applicant:
			result['data'].append([
				aplicant.create_date if aplicant.create_date else '',
				aplicant.name if aplicant.name else '',
				aplicant.partner_name if aplicant.partner_name else '',
				aplicant.email_from if aplicant.email_from else '',
				aplicant.partner_phone if aplicant.partner_phone else '',
				aplicant.job_id.name if aplicant.job_id else '',
				aplicant.stage_id.name if aplicant.stage_id else '',
				aplicant.medium_id.name if aplicant.medium_id else '',
				aplicant.source_id.name if aplicant.source_id else '',
				aplicant.priority if aplicant.priority else '',
				aplicant.user_id.name if aplicant.user_id else ''
			])
		return simplejson.dumps(result, default=str)
