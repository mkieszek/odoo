# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
import time

from openerp.osv import fields, osv
from openerp.tools.translate import _

class hr_timesheet_copy_wizard(osv.osv_memory):
    _name = 'hr.timesheet.copy.wizard'
    _description = 'hr.timesheet.copy.wizard'
    
    _columns = {
                'employee_id': fields.many2one('hr.employee', 'Employee', required=True),
                }

    def copy_timesheet(self, cr, uid, ids, context=None):
        if 'sheet_id' not in context:
            return False
        
        record = self.browse(cr, uid, ids, context=context)[0]
        
        hr_timesheet_obj = self.pool.get('hr_timesheet_sheet.sheet')
        
        default = {'employee_id': record.employee_id.id}
        
        timesheet_id = hr_timesheet_obj.copy(cr, uid, context['sheet_id'], default, context)
        
        domain = "[('user_id','=', {0})]".format(record.employee_id.user_id.id)
        
        value = {
            'domain': domain,
            'name': _('Open Timesheet'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr_timesheet_sheet.sheet',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'res_id': timesheet_id
        }
        
        return value


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
