# -*- coding: utf-8 -*-
'''
Created on 27 kwi 2014

@author: sony
'''

import datetime
import base64
import pdb
from gdata.contentforshopping.data import Year

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    
from openerp.osv import osv, fields


months_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

class hr_timesheet_import(osv.osv_memory):
    _name = 'hr.timesheet.import'
    _description = "Import kart pracy"
    _columns = {
                'name' : fields.char('Name'),
                'state': fields.selection([('choose', 'choose'),('get', 'get')]),
                'file_import': fields.binary('Import file'),
                }
    _defaults = { 
        'state': 'choose',
        'name': 'lang.tar.gz',
    }
    
    def timesheet_import(self, cr, uid, ids, context=None):
        #import z pliku
        #pdb.set_trace()
        record = self.browse(cr, uid, ids, context=context)[0]
        
        csvfile = StringIO(base64.b64decode(record.file_import))
        partner_obj = self.pool.get('res.partner')
        
        dict = {'message_follower_ids': False, 'timesheet_ids': [[0, False, {'general_account_id': 23, 
 'godz_nadliczbowe': 1, 'godz_nocne': 1, 'name': '123', 'godz_nieefektywne': 1, 'user_id': 6, 
 'product_uom_id': 5, 'proces_id': False, 'journal_id': 3, 'godz_normalne': 1, 'to_invoice': False, 
 'amount': 0, 'product_id': 1, 'nadplacone': 1, 'unit_amount': 0, 'date': '2015-05-27', 'uciazliwe': 
 1, 'niebezpieczne': 1, 'kierowca': 1, 'obiekt_id': False, 'account_id': 248}]], 'employee_id': 412, 
 'name': False, 'date_from': '2015-04-07', 'attendances_ids': [], 'company_id': 1, 'nieobecnosc': 
 False, 'date_to': '2015-05-27', 'message_ids': False}

        bgt_values = {}
        
        for row in csvfile:
            client_num = None
            brand_name = None
            
            client_id = 0
            month = 0
            year = 0
            category_id = 0
            plan_client_id = 0
            plan_client_brand_id = 0
            product_category_id = 0
            
            row = row.replace('\r\n', '')
            row_tab = row.split(",") 
            
            client_num = row_tab[0]
            brand_name = row_tab[1]
            
            year = 0
            month = 0
            nsh = 0.0
            gp = 0.0
            try:
                year = int(row_tab[2])
                month = row_tab[3].zfill(2)
                nsh = float(row_tab[4])
                gp = float(row_tab[5])
            except:
                continue
            
            client_id = partner_obj.search(cr, uid, [('ref','ilike', client_num)])
        
        for row in bgt_values:
            print row
        return True
