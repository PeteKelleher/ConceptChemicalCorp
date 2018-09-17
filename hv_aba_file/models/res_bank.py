# -*- coding: utf-8 -*-
from openerp import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    bsb = fields.Char(
        string='BSB Number', required=True, size=7,
        help="Bank/State/Branch number of the funds account with a hyphen in the 4th character position. e.g. 013-999")
    deu_id = fields.Char(string='Direct Entry User Identification', required=True, size=6)
    fic = fields.Char(
        string='Financial Institution Code', required=True, size=3,
        help="Must contain the bank mnemonic that is associated with the BSB of the funds account. e.g. ‘ANZ’, ‘WBC’.")

