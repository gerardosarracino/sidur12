# -*- coding: utf-8 -*-
{
    'name': "report invoice test",

    'summary': """
       report invoice test""",

    'description': """
        bienvenido a report invoice test
    """,

    'author': "Biblioteca inc.",
    'website': "http://www.biblioinc.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['ejecucion_obra'],

    # always loaded
    'data': [
        'data/paperformat.xml',
        'report/reports.xml',
        'report/account_invoice_report.xml'
    ],
    # only loaded in demonstration mode
   'installable': True,
}