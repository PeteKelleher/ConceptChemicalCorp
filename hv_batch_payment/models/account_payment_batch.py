# -*- coding: utf-8 -*-
from openerp import fields, models, api


class AccountBatchPayment(models.Model):
    _name = 'account.payment.batch'
    _description = 'Batch Payment'

    @api.multi
    @api.onchange('payment_ids')
    def _compute_amount_total(self):
        for record in self:
            amount_total = 0
            if record.payment_ids:
                for payment_id in record.payment_ids:
                        amount_total += payment_id.amount
            record.amount_total = amount_total
            record.count_payment = len(record.payment_ids.ids)

    name = fields.Char(string='Name')
    details = fields.Char(string='Details', size=12)
    amount_total = fields.Float(string='Amount Total', compute='_compute_amount_total')
    count_payment = fields.Float(string='Count Payment', compute='_compute_amount_total')
    payment_ids = fields.One2many(
        'account.payment', 'batch_id', string='Payments', domain=[('partner_type', '=', 'supplier')]
    )
    journal_id = fields.Many2one('account.journal', string='Journal', domain=[('type', 'in', ['bank'])], required=True)
    payment_date = fields.Datetime(string='Payment Date', required=True, default=fields.Datetime.now)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('account.payment.batch')
        return super(AccountBatchPayment, self).create(vals)
