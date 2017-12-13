# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sunulocationevent_order(models.Model):
    _inherit = 'sale.order'
    
    lieuEvent = fields.Char("Lieu de l'événement")
    dateEvent = fields.Date("Date l'événement")
    dateMontage = fields.Date("Date de montage")
    dateDemontage = fields.Date("Date de démontage")

class Sunulocationevent_orderline(models.Model):
    _inherit = 'sale.order.line'
    nombreJours = fields.Integer("Nombre de jours")

#     _name = 'hdlabs_facture_senegalbaches.hdlabs_facture_senegalbaches'
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#     self.value2 = float(self.value) / 100