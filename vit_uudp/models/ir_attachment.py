# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017  Odoo SA  (http://www.vitraining.com)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError

class irAttachment(models.Model):
    _name = "ir.attachment"
    _inherit = "ir.attachment"


    @api.multi
    def unlink(self):
        # import pdb;pdb.set_trace()
        for data in self:
            if data.res_model == 'uudp':
                uudp = self.env['uudp'].search([('id','=',self.res_id)])
                if uudp.state != 'draft':
                    raise UserError(_('Attachment hanya bisa dihapus ketika dokumen berstatus draft !'))
        return super(irAttachment, self).unlink()