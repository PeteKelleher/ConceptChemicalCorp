# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit="sale.order"

    scheduled_date_picking = fields.Datetime(compute="get_scheduled_date_picking",store=True)

    @api.depends('picking_ids')
    def get_scheduled_date_picking(self):
        #We add this compute field taking the first scheduled_date of the pickings of the sale.order (if any).
        for rec in self:
            schedule_dates = rec.picking_ids and rec.picking_ids.mapped('scheduled_date')
            if schedule_dates:
                rec.scheduled_date_picking = schedule_dates[0]



class SaleReport(models.Model):
    _inherit = "sale.report"

    scheduled_date_order = fields.Datetime("Scheduled Delivery Date",readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        # We modify the query parameters of the sale.report to add our new field 
        # taking into account the scheduled_date_picking of the sale.order created above.
        fields['scheduled_date_order'] = ",  s.scheduled_date_picking as scheduled_date_order"

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)