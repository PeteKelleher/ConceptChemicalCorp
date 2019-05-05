# -*- coding: utf-8 -*-

from odoo import api, fields, models

class MailTemplate(models.Model):
    _inherit = "mail.template"

    @api.model_cr
    def init(self):
        mail = self.env.ref('purchase.email_template_edi_purchase_done')
        mail.write({
            'subject': 'Purchase Order Confirmation ${object.name or "n/a"} from  ${object.company_id.name}',
            'body_html': """<div style="margin: 0px; padding: 0px;">
                            <div style="margin: 0px; padding: 0px;">
                                <p style="margin: 0px; padding: 0px; font-size: 13px;">
                                    Dear ${object.partner_id.name},
                                    % if object.partner_id.parent_id:
                                        (${object.partner_id.parent_id.name})
                                    % endif
                                    <br/><br/>
                                Please find attached our Purchase Order <strong>${object.name}</strong>
                                for Product
                                    % for line in object.order_line:
                                            <strong>
                                                ${line.product_id.name},
                                            </strong>.
                                    % endfor
                                </p>
                            </div>
                        </div>"""
            })