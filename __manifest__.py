# -*- coding: utf-8 -*-
{
    'name': "Sunu Location Evenement",
    'summary': """Gestion de la location de matériel d'événementiel""",
    'description': """Gestion de la location de matériel. Prise en compte du nombre de jours de location, de la date de début, de la date de fin, du lieu de livraison, de la date de montage et démontage, etc.""",
    'author': "Elhadji Malang Diedhiou",
    'website': "http://www.supermalang.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management'],

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