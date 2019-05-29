# -*- coding: utf-8 -*-

from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    custom_date_required = fields.Datetime(
        string='Date Required',
        compute='compute_custom_date_required',
        store=True,
    )
    
    @api.depends('order_line','order_line.date_planned')
    def compute_custom_date_required(self):
        for rec in self:
            rec.custom_date_required = rec.order_line and rec.order_line[0] and rec.order_line[0].date_planned
