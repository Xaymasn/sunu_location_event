# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sunulocationevent(models.Model):
    _inherit        = "sale.order.line"
    lieuEvent       = fields.Char()
    dateEvent       = fields.Date()
    dateMontage     = fields.Date()   
    dateDemontage   = fields.Date()
    nbJours         = fields.Integer()

#     _name = 'hdlabs_facture_senegalbaches.hdlabs_facture_senegalbaches'
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#     self.value2 = float(self.value) / 100