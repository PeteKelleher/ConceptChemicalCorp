# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = "res.company"
    
    custom_footer_note = fields.Text(
        string='Footer Note',
    )