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
        emp_obj = self.pool.get('hr.employee')
        cpk_obj = self.pool.get('hr.timesheet.pkp.cpk')
        obiekt_obj = self.pool.get('hr.timesheet.pkp.obiekt')
        proces_obj = self.pool.get('hr.timesheet.pkp.proces')
        nieobecnosc_obj = self.pool.get('hr.timesheet.pkp.nieobecnosc')
        line_obj = self.pool.get('hr.analytic.timesheet')
        sheet_obj = self.pool.get('hr_timesheet_sheet.sheet')
        account_obj = self.pool.get('account.analytic.account')
        
        dict = {'message_follower_ids': False, 'timesheet_ids': [[0, False, {'general_account_id': 23, 
 'godz_nadliczbowe': 1, 'godz_nocne': 1, 'name': '123', 'godz_nieefektywne': 1, 'user_id': 6, 
 'product_uom_id': 5, 'proces_id': False, 'journal_id': 3, 'godz_normalne': 1, 'to_invoice': False, 
 'amount': 0, 'product_id': 1, 'nadplacone': 1, 'unit_amount': 0, 'date': '2015-05-27', 'uciazliwe': 
 1, 'niebezpieczne': 1, 'kierowca': 1, 'obiekt_id': False, 'account_id': 248}]], 'employee_id': 412, 
 'name': False, 'date_from': '2015-04-07', 'attendances_ids': [], 'company_id': 1, 'nieobecnosc': 
 False, 'date_to': '2015-05-27', 'message_ids': False}

        bgt_values = {}
        kz_dict = {}
                
        for row in csvfile:
            emp_name = None
            emp_id = None
            cpk_id = None
            proces_id = None
            obiekt_id = None
            projekt_id = None
            nieobecnosc_id = None
            sheet_id = None
            
            row = row.replace('\r\n', '')
            row_tab = row.split(";") 
            
            
            emp_name = row_tab[22]
            data = row_tab[1]
            cpk = row_tab[2]
            proces = row_tab[3]
            obiekt = row_tab[4]
            projekt = row_tab[6]
            nieobecnosc = row_tab[8]
            nieefektywne = row_tab[9]
            normalne = row_tab[10]
            nadliczbowe = row_tab[11]
            nadliczbowe_sw = row_tab[12]
            noc = row_tab[13]
            uciazliwe = row_tab[14]
            kierowcy = row_tab[15]
            niebezpieczne = row_tab[16]
            swieta = row_tab[17]
            nadpracowane = row_tab[18]
            
            emp_id = emp_obj.search(cr, uid, [('name', '=', emp_name.rstrip('\n'))])
            cpk_id = cpk_obj.search(cr, uid, [('kod', '=', cpk)])
            proces_id = proces_obj.search(cr, uid, [('kod', '=', proces)])
            nieobecnosc_id = nieobecnosc_obj.search(cr, uid, [('kod', '=', nieobecnosc)])
            
            obiekt_id = obiekt_obj.search(cr, uid, [('kod', '=', obiekt)])
            if not obiekt_id:
                obiekt_id = obiekt_obj.search(cr, uid, [('kod', '=', '000')])
            
            projekt_id = account_obj.search(cr, uid, [('code', '=', projekt)])
            if not projekt_id:
                projekt_id = account_obj.search(cr, uid, [('code', '=', '0000')])
                
            if emp_id:
                emp_id = emp_id[0]
                sheet_id = sheet_obj.search(cr, uid, [('date_from', '=', data),('employee_id','=', emp_id),('import','=', False)])
            else:
                continue
            
            if sheet_id:
                continue
            
            emp = emp_obj.browse(cr, uid, emp_id)
            
            sheet_id = sheet_obj.search(cr, uid, [('date_from', '=', data),('employee_id','=', emp_id),('import','=', True)])
            
            if sheet_id:
                sheet_id = sheet_id[0]
            else:
                sheet_dict = {'employee_id': emp_id,
                              'name': False,
                              'date_from': data, 
                              'company_id': 1, 
                              'nieobecnosc': nieobecnosc_id and nieobecnosc_id[0] or False, 
                              'date_to': data,
                              'import': True,
                              'state': 'draft',
                              'department_id': emp.department_id.id}
                sheet_id = sheet_obj.create(cr, uid, sheet_dict)
                
            sheet = sheet_obj.browse(cr, uid, sheet_id)
            
            line_dict = {'general_account_id': 23, 
                         'godz_nadliczbowe': float(nadliczbowe) + float(nadliczbowe_sw), 
                         'godz_nocne': float(noc), 
                         'name': 'brak', 
                         'godz_nieefektywne': float(nieefektywne),
                         'user_id': sheet[0].user_id.id,
                         'product_uom_id': 5,
                         'proces_id': proces_id[0],
                         'journal_id': 3,
                         'godz_normalne': float(normalne) + float(swieta),
                         'to_invoice': False,
                         'amount': 0,
                         'product_id': 1,
                         'nadplacone': float(nadpracowane),
                         'unit_amount': 0,
                         'date': data,
                         'uciazliwe': float(uciazliwe),
                         'niebezpieczne': float(niebezpieczne),
                         'kierowca': float(kierowcy),
                         'obiekt_id': obiekt_id[0],
                         'account_id': projekt_id[0],
                         'sheet_id': sheet_id,
                         'import': True}
            
            #pdb.set_trace()
            line_obj.create(cr, uid, line_dict)
            #dodac wiersz do karty 
                
                
        
            
            #client_id = partner_obj.search(cr, uid, [('ref','ilike', client_num)])
        
        for row in bgt_values:
            print row
        return True
