# -*- coding: utf-8 -*-
from openerp import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    user_of_supplying_file = fields.Char(string='Name of User supplying File', size=26)
    name_of_remitter = fields.Char(string='Name of Remitter', size=16)
