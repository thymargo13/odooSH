# -*- coding: utf-8 -*-

{
    
    'name': 'Odoo Academy',
    'summary': """Academy app to manage Training""",
    'description':"""
        Academy Module to manage Training: 
        - Courses
        - Session
        - Attendees
    """,
    'author': 'Odoo',
    'website':'https://www.odoo.com',
    'category': 'Training',
    'version':'0.1',
    'depends':['sale'],
    'data':[
        'security/academy_security.xml',
        'security/ir.model.access.csv',
        'views/academy_menuitems.xml',
        'views/course_views.xml',
        'views/session_views.xml',
        'views/sale_views_inherit.xml',
        'views/product_views_inherit.xml',
        'wizards/sale_wizard_view.xml',
        'report/session_report_template.xml',
        
    ],
    'demo':[
        'demo/academy_demo.xml'
    ],
}