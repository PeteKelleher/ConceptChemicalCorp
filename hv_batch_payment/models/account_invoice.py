# -*- coding: utf-8 -*-
from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    payment_amount = fields.Float(string='Payment Amount', default=0.0)
