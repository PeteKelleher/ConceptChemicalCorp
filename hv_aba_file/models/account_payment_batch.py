# -*- coding: utf-8 -*-
from openerp import models, api, _
from openerp.exceptions import except_orm
from datetime import datetime
import base64

import logging

_logger = logging.getLogger(__name__)


class AccountBatchPayment(models.Model):
    _inherit = 'account.payment.batch'

    @api.multi
    def check_data(self):
        list_vendor_bank_account = []
        list_vendor_bank_for_bank_account = []
        for payment in self.payment_ids:
            if not payment.journal_id.bank_id:
                raise except_orm(
                    _('Please configure Bank for journal %s' % payment.journal_id.name),
                    _('- Accounting > Configuration > Accounting > Journals \n'
                      '- Select journals \n'
                      '- Go to BANK ACCOUNT tab \n'
                      '- Set Bank'))
            if payment.partner_id.bank_account_count == 0 and payment.partner_id.name not in list_vendor_bank_account:
                list_vendor_bank_account.append(payment.partner_id.name)
            banks = self.env['res.partner.bank'].search([('partner_id', '=', payment.partner_id.id)])
            if banks:
                for bank in banks:
                    if not bank.bank_id and bank.partner_id.name not in list_vendor_bank_for_bank_account:
                        list_vendor_bank_for_bank_account.append(payment.partner_id.name)
        if list_vendor_bank_account:
            raise except_orm(
                _('Please configure Bank Account for below Vendor(s)'),
                _('- Vendor(s): %s \n'
                  '- Accounting > Purchases > Vendors \n'
                  '- Go to Sales & Purchases tab \n'
                  '- Configure Bank Account under Payments section' % ', '.join(list_vendor_bank_account)))
        if list_vendor_bank_for_bank_account:
            raise except_orm(
                _('Please configure Bank for Bank Account for below Vendor(s)'),
                _('- Vendor(s): %s \n'
                  '- Accounting > Purchases > Vendors \n'
                  '- Go to Sales & Purchases tab \n'
                  '- Click on Bank Account under Payments section \n'
                  '- Open vendor Bank Account \n'
                  '- Make sure Bank has been selected for vendor Bank Account' %
                  ', '.join(list_vendor_bank_for_bank_account)))

    @api.multi
    def format_amount(self, str_amount, str_len):
        """
        Attention: some float value exp: 11.50, 2.80 => when pass in python, it's only appear 11.5, 2.8
        So, we can not align right, because it will cause '5' -> '05' (origin is '50')
        We must align left, '5' -> '50'
        """
        lst_str_amount = str(str_amount).split('.')
        if len(lst_str_amount) >= 2:
            lst_str_amount[1] = '{:0<2}'.format(lst_str_amount[1])
        amount_string = str(''.join(lst_str_amount))
        return '0'*(int(str_len)-len(amount_string)) + amount_string

    @api.multi
    def format_number(self, str_amount, str_len):
        amount_string = ''
        if str_amount:
            amount_string = str(int(str_amount))
        return '0'*(int(str_len)-len(amount_string)) + amount_string

    @api.multi
    def repair_data(self):
        self.check_data()
        list_details = []
        dist_data = {
            'header': {
                'record_type': 0,
                'sequence_number': '01',
                'ufi': self.journal_id.bank_id.fic,
                'usf': self.journal_id.user_of_supplying_file,
                'uin': self.journal_id.bank_id.deu_id,
                'description': self.details,
                'date': datetime.strptime(self.payment_date, '%Y-%m-%d %H:%M:%S').strftime('%d%m%y'),
            },
            'details': {},
            'footer': {
                'record_type': 7,
                'batch_net_total_amount': self.amount_total - 0,
                'batch_credit_total_amount': self.amount_total,
                'batch_debit_total_amount': 0,
                'batch_total_item_count': self.count_payment,
            },
        }
        for payment in self.payment_ids:
            banks = self.env['res.partner.bank'].search([('partner_id', '=', payment.partner_id.id)])
            if banks:
                list_details.append({
                    'record_type': 1,
                    'bsb': banks[0].bank_id.bsb,
                    'account_number': banks[0].acc_number,
                    'transaction_code': 50,
                    'amount': payment.amount,
                    'title': payment.partner_id.name,
                    'reference': payment.communication,
                    'trace_bsb': payment.journal_id.bank_id.bsb,
                    'trace_account_number': payment.journal_id.bank_acc_number,
                    'payer': payment.journal_id.name_of_remitter,
                })
        dist_data['details'] = list_details
        return dist_data

    @api.multi
    def get_line_header(self, dict_data):
        line = ''
        line += '{:1}'.format(dict_data.get('record_type') or '0')
        line += '{:>19}'.format('{:>2}'.format(dict_data.get('sequence_number') or ''))
        line += '{:10}'.format('{:3}'.format(dict_data.get('ufi') or ''))
        line += '{:26}'.format(dict_data.get('usf')[:26] or '')
        line += '{:>6}'.format(dict_data.get('uin') or '')
        line += '{:12}'.format(dict_data.get('description') or '')
        line += '{:46}'.format('{:6}'.format(dict_data.get('date') or ''))
        return line

    @api.multi
    def get_line_details(self, dict_data):
        line = ''
        line += '{:1}'.format(dict_data.get('record_type') or '')
        line += '{:7}'.format(dict_data.get('bsb') or '')
        line += '{:>9}'.format(dict_data.get('account_number') or '')
        line += ' ' + '{:2}'.format(dict_data.get('transaction_code') or '')
        line += '{:0>10}'.format(self.format_amount(dict_data.get('amount') or '', 10))
        line += '{:25}'.format(dict_data.get('title') or '')
        line += '{:18}'.format(dict_data.get('reference')[:18] or '')
        line += '{:7}'.format(dict_data.get('trace_bsb') or '')
        line += '{:>9}'.format(dict_data.get('trace_account_number') or '')
        line += '{:16}'.format(dict_data.get('payer') or '')
        line += '{:8}'.format('0'*8)

        return line

    @api.multi
    def get_line_footer(self, dict_data):
        line = ''
        line += '{:20}'.format('{:8}'.format(str(dict_data.get('record_type')) + '999-999' or ''))
        line += '{:0>10}'.format(self.format_amount(dict_data.get('batch_net_total_amount') or '', 10))
        line += '{:0>10}'.format(self.format_amount(dict_data.get('batch_credit_total_amount') or '', 10))
        line += '{:0>10}'.format(self.format_amount(dict_data.get('batch_debit_total_amount') or '', 10))
        line += '{:70}'.format('{:>30}'.format('{:0>6}'.format(
            self.format_number(dict_data.get('batch_total_item_count') or '', 6)
        )))

        return line

    @api.multi
    def generate_aba_file(self):
        dist_data = self.repair_data()
        list_line = []
        list_line.append(self.get_line_header(dist_data['header']))
        for dict_detail in dist_data['details']:
            list_line.append(self.get_line_details(dict_detail))
        list_line.append(self.get_line_footer(dist_data['footer']))
        # check ABA line length
        for line in list_line:
            if len(line) != 120:
                _logger.info("LINE %s has incorrect length %s", line, len(line))
        cotent_file = '\n'.join(list_line)
        attachment_value = {
            'name': self.name,
            'res_name': self.name,
            'res_model': 'account.payment.batch',
            'res_id': self.id,
            'datas': base64.b64encode(cotent_file.encode()),
            'datas_fname': self.name + '.aba',
        }
        new_attachment = self.env['ir.attachment'].create(attachment_value)
        self.write({
            'attachment_ids': [(6, 0, [new_attachment.id])]
        })



