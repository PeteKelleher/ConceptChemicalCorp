# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Sales Report',
    'category': 'Sale',
    'description': """
    """,
    'depends': ['sale', 'stock', 'sale_enterprise'],
    'data': [
        'views/sale_report.xml',
    ],
}