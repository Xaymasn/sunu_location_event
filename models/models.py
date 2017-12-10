# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hdlabs_facture_senegalbaches(models.Model):
    _inherit        = "sale.order.line"
    lieuEvent       = fields.Char()
    dateEvent       = fields.Date()
    dateMontage     = fields.Date()   
    dateDemontage   = fields.Date()
    _columns={
        'nbJours':fields.Integer('Nombre de jours')
    }

#     _column = {'nb_jours': fields.Char('Nombre de jours')}
#     _name = 'hdlabs_facture_senegalbaches.hdlabs_facture_senegalbaches'
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#     self.value2 = float(self.value) / 100