# -*- coding: utf-8 -*-
from openerp import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    batch_id = fields.Many2one('account.payment.batch', string='Batch Payment')

