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
    _columns = {'name': fields.char('Nazwa', required=True),
                'kod': fields.char('Kod', required=True)
                }
    
    def name_get(self, cr, uid, ids, context=None):
        """Overrides orm name_get method"""
        if not isinstance(ids, list) :
            ids = [ids]
        res = []
        if not ids:
            return res
        #reads = self.read(cr, uid, ids, ['client_id', 'month', 'year'], context)
        for record in self.browse(cr, uid, ids):
            res.append((record.id, record.kod + ' - ' + record.name or ''))
        return res
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=0):
        args = []
        if not context:
            context = {}
        
        if name:
            # Be sure name_search is symetric to name_get
            #name = name.split(' / ')[-1]
            name_ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
            kod_ids = self.search(cr, uid, [('kod', operator, name)] + args, limit=limit, context=context)
            ids = name_ids + kod_ids
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
       
        return self.name_get(cr, uid, ids, context)
    
class hr_timesheet_pkp_obiekt(osv.Model):
    _name = 'hr.timesheet.pkp.obiekt'
    _description = 'Obiekt'
    _columns = {'name': fields.char('Nazwa', required=True),
                'kod': fields.char('Kod', required=True)
                }
    
    def name_get(self, cr, uid, ids, context=None):
        """Overrides orm name_get method"""
        if not isinstance(ids, list) :
            ids = [ids]
        res = []
        if not ids:
            return res
        #reads = self.read(cr, uid, ids, ['client_id', 'month', 'year'], context)
        for record in self.browse(cr, uid, ids):
            res.append((record.id, record.kod + ' - ' + record.name or ''))
        return res
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=0):
        args = []
        if not context:
            context = {}
        
        if name:
            # Be sure name_search is symetric to name_get
            #name = name.split(' / ')[-1]
            name_ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
            kod_ids = self.search(cr, uid, [('kod', operator, name)] + args, limit=limit, context=context)
            ids = name_ids + kod_ids
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
       
        return self.name_get(cr, uid, ids, context)

class hr_timesheet_pkp_okres(osv.Model):
    _name = 'hr.timesheet.pkp.okres'
    _description = 'Okres'
    _columns = {'name': fields.char('Nazwa'),
                'od': fields.date('Od', required=True),
                'do': fields.date('Do', required=True),
                'status': fields.selection(STATUSY_OKRESU, 'Status', required=True),
                }
    
    def name_get(self, cr, uid, ids, context=None):
        """Overrides orm name_get method"""
        if not isinstance(ids, list) :
            ids = [ids]
        res = []
        if not ids:
            return res
        #reads = self.read(cr, uid, ids, ['client_id', 'month', 'year'], context)
        for record in self.browse(cr, uid, ids):
            res.append((record.id, record.kod + ' - ' + record.name or ''))
        return res
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=0):
        args = []
        if not context:
            context = {}
        
        if name:
            # Be sure name_search is symetric to name_get
            #name = name.split(' / ')[-1]
            name_ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
            kod_ids = self.search(cr, uid, [('kod', operator, name)] + args, limit=limit, context=context)
            ids = name_ids + kod_ids
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
       
        return self.name_get(cr, uid, ids, context)
    
class hr_timesheet_pkp_cpk(osv.Model):
    _name = 'hr.timesheet.pkp.cpk'
    _description = 'MPK'
    _columns = {'name': fields.char('Nazwa', required=True),
                'kod': fields.char('Kod', required=True)
                }
    
    def name_get(self, cr, uid, ids, context=None):
        """Overrides orm name_get method"""
        if not isinstance(ids, list) :
            ids = [ids]
        res = []
        if not ids:
            return res
        #reads = self.read(cr, uid, ids, ['client_id', 'month', 'year'], context)
        for record in self.browse(cr, uid, ids):
            name = record.name or ''
            res.append((record.id, record.kod + ' - ' + name))
        return res
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=0):
        args = []
        if not context:
            context = {}
        
        if name:
            # Be sure name_search is symetric to name_get
            #name = name.split(' / ')[-1]
            name_ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
            kod_ids = self.search(cr, uid, [('kod', operator, name)] + args, limit=limit, context=context)
            ids = name_ids + kod_ids
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
       
        return self.name_get(cr, uid, ids, context)
class hr_timesheet_pkp_nieobecnosc(osv.Model):
    _name = 'hr.timesheet.pkp.nieobecnosc'
    _description = 'Nieobecnosc'
    _columns = {'name': fields.char('Nazwa', required=True),
                'kod': fields.char('Kod', required=True),
                'enova_kod': fields.char('Kod Enova', required=True),
                }
    
    def name_get(self, cr, uid, ids, context=None):
        """Overrides orm name_get method"""
        if not isinstance(ids, list) :
            ids = [ids]
        res = []
        if not ids:
            return res
        #reads = self.read(cr, uid, ids, ['client_id', 'month', 'year'], context)
        for record in self.browse(cr, uid, ids):
            name = record.name or ''
            kod = record.kod or ''
            res.append((record.id, kod + ' - ' + name))
        return res
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=0):
        args = []
        if not context:
            context = {}
        
        if name:
            # Be sure name_search is symetric to name_get
            #name = name.split(' / ')[-1]
            name_ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
            kod_ids = self.search(cr, uid, [('kod', operator, name)] + args, limit=limit, context=context)
            ids = name_ids + kod_ids
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
       
        return self.name_get(cr, uid, ids, context)
    
class account_analytic_account(osv.osv):
    _name = "account.analytic.account"
    _inherit = "account.analytic.account"
    
    def name_get(self, cr, uid, ids, context=None):
        """Overrides orm name_get method"""
        if not isinstance(ids, list) :
            ids = [ids]
        res = []
        if not ids:
            return res
        #reads = self.read(cr, uid, ids, ['client_id', 'month', 'year'], context)
        for record in self.browse(cr, uid, ids):
            name = record.name or ''
            res.append((record.id, record.code + ' - ' + name))
        return res
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=0):
        if not args:
            args = []
        
        if name:
            # Be sure name_search is symetric to name_get
            #name = name.split(' / ')[-1]
            name_ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
            kod_ids = self.search(cr, uid, [('code', operator, name)] + args, limit=limit, context=context)
            ids = name_ids + kod_ids
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
       
        return self.name_get(cr, uid, ids, context)