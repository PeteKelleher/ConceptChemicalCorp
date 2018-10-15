# -*- coding: utf-8 -*-
from openerp import _, api, fields, models
from openerp.exceptions import Warning


class WizardBatchPayment(models.TransientModel):
    _name = 'wizard.payment.batch'
    _description = 'Batch Payment'

    msg_notify = fields.Char(string='Notify Message', readonly=True)
    amount_total = fields.Float(string='Amount Total', readonly=True)
    sum_partner = fields.Integer(string='Sum Partner', readonly=True)
    invoice_ids = fields.Many2many('account.invoice', string='Invoices')
    journal_id = fields.Many2one('account.journal', string='Journal', domain=[('type', 'in', ['bank'])], required=True)
    payment_date = fields.Date(string='Payment Date', default=fields.Date.context_today)
    details = fields.Char(string='Details')

    @api.model
    def default_get(self, values):
        data = super(WizardBatchPayment, self).default_get(values)
        invoice_ids = self.env['account.invoice'].browse(self.env.context.get('active_ids', []))
        if invoice_ids:
            amount_total = float(data.get('amount_total') or 0)
            count_vendor = 0
            list_vendor = []
            list_invoice = []
            for invoice_id in invoice_ids:
                if invoice_id.state == 'open':
                    amount_total += invoice_id.amount_total
                    if invoice_id.partner_id.id not in list_vendor:
                        count_vendor += 1
                        list_vendor.append(invoice_id.partner_id.id)
                    invoice_id.payment_amount = invoice_id.residual_signed
                    list_invoice.append(invoice_id.id)
                else:
                    raise Warning(_("Please select only open invoices."))
            data.update({
                'amount_total': amount_total,
                'sum_partner': count_vendor,
                'invoice_ids': [(6, 0, list_invoice)] if list_invoice != [] else False,
            })
        return data

    @api.multi
    @api.onchange('invoice_ids')
    def onchange_payment_amount(self):
        amount_total = 0
        currency_id = self.env['res.currency'].browse()
        for invoice in self.invoice_ids:
            if invoice.payment_amount < 0 or invoice.payment_amount > invoice.residual_signed:
                invoice.payment_amount = invoice.residual_signed
                raise Warning(_(
                    'Payment amount is must greater than 0 and less than %s.')
                              % invoice.residual_signed)
            else:
                amount_total += invoice.payment_amount
                currency_id = invoice.currency_id
        if amount_total:
            str_msg_notify = 'You are going to pay %s %s to %s vendors?' % (
                currency_id.symbol or '', amount_total, self.sum_partner)
            self.update({
                'msg_notify': str_msg_notify,
            })
        return {}

    @api.multi
    def repair_data(self, invoices):
        dict_invoice = {}
        for invoice in invoices:
            if invoice.state == 'open':
                list_invoice = []
                if invoice.partner_id.id not in dict_invoice:
                    list_invoice.append(invoice.id)
                    dict_invoice[invoice.partner_id.id] = list_invoice
                else:
                    dict_invoice[invoice.partner_id.id].append(invoice.id)
        return dict_invoice

    @api.multi
    def confirm_button(self):
        ctx = self.env.context.copy()
        dict_data = self.repair_data(self.env['account.invoice'].browse(self.env.context.get('active_ids', [])))
        batch_id = self.env['account.payment.batch'].create({
            'details': self.details,
            'payment_date': self.payment_date,
            'journal_id': self.journal_id.id,
        })
        for data in dict_data:
            invoices = self.env['account.invoice'].browse(dict_data[data])
            for invoice in invoices:
                pay_amount = 0
                communication = ''
                if invoice.payment_amount < 0 or invoice.payment_amount > invoice.residual_signed:
                    invoice.payment_amount = invoice.residual_signed
                    raise Warning(_(
                        'Payment amount is must greater than 0 and less than %s.')
                                  % invoice.residual_signed)
                communication += invoice.type in (
                    'in_invoice', 'in_refund') and invoice.reference or invoice.number + ', '
                pay_amount += invoice.payment_amount
                payment = self.env['account.payment'].create({
                    'journal_id': self.journal_id.id,
                    'payment_method_id': self.env['account.payment.method'].search([], limit=1).id,
                    'payment_date': self.payment_date,
                    'communication': communication,
                    'invoice_ids': [(6, 0, [invoice.id])],
                    'payment_type': invoice.type in ('out_invoice', 'in_refund') and 'inbound' or 'outbound',
                    'amount': pay_amount,
                    'partner_id': self.env['res.partner'].browse(data).id,
                    'partner_type': invoice.type in ('out_invoice', 'out_refund') and 'customer' or 'supplier',
                    'currency_id': invoice.currency_id.id,
                    'batch_id': batch_id.id,
                })
                payment.post()
        view = self.env.ref('hv_batch_payment.batch_payments_form_view')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Registered Batch',
            'res_id': batch_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view.id,
            'views': [(view.id, 'form')],
            'res_model': 'account.payment.batch',
            'target': 'current',
            'context': ctx,
        }
