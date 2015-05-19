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
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone
import pytz

from openerp import api, models
from openerp.osv import fields, osv
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _

STATUSY_OKRESU = [('o', 'Otwarty'), ('z', 'Zamknięty')]

class hr_timesheet_pkp_proces(osv.Model):
    _name = 'hr.timesheet.pkp.proces'
    _description = 'Proces'
    _columns = {'name': fields.char('Nazwa')
                }
    
class hr_timesheet_pkp_obiekt(osv.Model):
    _name = 'hr.timesheet.pkp.obiekt'
    _description = 'Obiekt'
    _columns = {'name': fields.char('Nazwa')
                }

class hr_timesheet_pkp_okres(osv.Model):
    _name = 'hr.timesheet.pkp.okres'
    _description = 'Okres'
    _columns = {'name': fields.char('Nazwa'),
                'od': fields.date('Od', required=True),
                'do': fields.date('Do', required=True),
                'status': fields.selection(STATUSY_OKRESU, 'Status', required=True),
                }
    
    def name_get(self, cr, uid, ids, context=None):
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            #name = record.name
            #if not record.limit:
            #    name = name + ('  (%g/%g)' % (record.leaves_taken or 0.0, record.max_leaves or 0.0))
            res.append((record.id, 'dupa'))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('number', '=', name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()
    
class hr_timesheet_pkp_cpk(osv.Model):
    _name = 'hr.timesheet.pkp.cpk'
    _description = 'CPK'
    _columns = {'name': fields.char('Nazwa')
                }