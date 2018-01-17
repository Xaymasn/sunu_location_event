# -*- coding: utf-8 -*-
{
    'name': "Sunu Location Evenement",
    'summary': """Gestion de la location de matériel d'événementiel""",
    'description': """
        Gestion de la location de matériel :
                - Prise en compte du nombre de jours de location
                - Prise en compte de la date de début de l'événement
                - Prise en compte de la date de fin de l'événement
                - Prise en compte du lieu de livraison du matériel
                - Prise en compte de la date de reprise du matériel
                - Création d'un entrepôt '**Location**' dans Odoo
                - Déplacement automatique (dans Odoo) du matériel loué vers l'entrepôt '**Location**'
        """,
    'author': "Elhadji Malang Diedhiou",
    'website': "http://www.supermalang.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales Management',
    'version': '11.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/saleorder.form.sle.xml',
        'views/saleorder.tree.sle.xml',
        'views/invoice.sle.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}