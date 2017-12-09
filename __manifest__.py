# -*- coding: utf-8 -*-
{
    'name': "Facture Location",

    'summary': """Colonnes de location de chaises dans la facture""",

    'description': """
        Module de gestion de location d'articles
    """,

    'author': "Elhadji Malang Diedhiou",
    'website': "http://www.supermalang.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}