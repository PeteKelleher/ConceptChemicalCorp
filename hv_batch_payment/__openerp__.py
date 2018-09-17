# -*- coding: utf-8 -*-

{
    'name': 'Batch Payment',
    'version': '11.0.0.1.0',
    'summary': 'Generate batch payment for different vendors',
    'description': 'Generate batch payment for different vendors',
    'website': 'http://havi.com.au',
    'category': 'Accounting',
    'images': ['static/description/logo.png'],
    'depends': [
        'account',
    ],
    'author': 'Havi Technology',
    'price': 50,
    'currency': "EUR",
    'data': [
        'data/ir_sequence.xml',
        'wizards/payment_batch.xml',
        'views/payment_batch.xml',
        'views/account_payment.xml',
        'views/menu.xml',
    ],
    'application': True,
}
