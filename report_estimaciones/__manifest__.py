# -*- coding: utf-8 -*-
{
    'name': "report estimaciones",

    'summary': """
       report estimaciones""",

    'description': """
        bienvenido a report report_estimaciones
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
        'report/control_estimaciones_report.xml',
        'report/reporte_control_est.xml',
        'report/relacion_conceptos_report.xml',
        'report/reporte_relacion_conceptos.xml',
        'report/reporte_penas_convencionales.xml',
        'report/penas_convencionales_report.xml'
    ],
    # only loaded in demonstration mode
   'installable': True,
}