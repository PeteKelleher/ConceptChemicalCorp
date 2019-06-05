# -*- encoding: utf-8 -*-

##############################################################################
#    Copyright (C) Ioppolo and Associates (I&A) 2015 (<http://ioppolo.com.au>).
###############################################################################
{
    "name" : "Australian CC Reports (CE)",
    "version" : "1.9.6.7",
    "author" : "Ioppolo and Associates",
    "website" : "http://www.ioppolo.com.au",
    "category" : "Sales",
    "summary": "Sales PDF Report",
    "description": """
         Sales PDF Report Custom,
         Add Commercial invoice report,
         Change layout for invoice report,
         Change layout for Stock Delivery report,
         Change Layout for Purchase Order and Request for Quotation report,
    """,
    "depends" : [
        'delivery',
        'stock',
        'account',
        'purchase_stock',
        'sale_stock',
    ],
    "data" : [
        'data/mail_template_data.xml',
        'data/mail_template_data_confirm.xml',
        'report/paper_format_view.xml',
#         'views/res_company_view.xml',
        'views/stock_picking_view.xml',
        'report/invoice_report_view.xml',
        'report/invoice_commercial_report_view.xml',
        'report/report_layout_view.xml',
        'report/purchase_order_report.xml',
        'report/quotation_report.xml',
        'report/report_sale_order_view.xml',
        'report/deivery_slip_report.xml',
        'report/picking_operation.xml',
    ],
    "installable": True,
    "auto_install": False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
