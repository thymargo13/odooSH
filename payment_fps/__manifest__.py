# -*- coding: utf-8 -*-

{
    'name': 'FPS Payment Acquirer',
    'category': 'Accounting/Payment Acquirers',
    'summary': 'Payment Acquirer: FPS Implementation',
    'version': '1.0',
    'description': """FPS Payment Acquirer""",
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_fps_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
}
