# -*- coding: utf-8 -*-

from odoo import fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    custom_comment = fields.Text(
        string='Special Instruction',
    )
    custom_partner_ref = fields.Char(
        string='Partner Ref'
    )
    custom_incoterm_id = fields.Many2one(
        'account.incoterms',
        string='Incoterms',
    )