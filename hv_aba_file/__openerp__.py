# -*- coding: utf-8 -*-

{
    'name': 'ABA file',
    'version': '11.0.0.1.0',
    'summary': 'Generate ABA file to submit to bank',
    'description': 'Generate ABA file to submit to bank',
    'website': 'http://havi.com.au',
    'category': 'Accounting',
    'images': ['static/description/logo.png'],
    'depends': [
        'hv_batch_payment', 'document',
    ],
    'author': 'Havi Technology',
    'price': 149,
    'currency': "EUR",
    'data': [
        'views/res_bank.xml',
        'views/account_journal.xml',
        'views/payment_batch.xml',
    ],
    'application': True,
}
