# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sunulocationevent_order(models.Model):
    _inherit = 'sale.order.line'
    
    lieuEvent = fields.Char("Lieu de l'événement")
    dateEvent = fields.Date("Date l'événement")
    dateMontage = fields.Date("Date de montage")
    dateDemontage = fields.Date("Date de démontage")
    nombreJours = fields.Integer("Nombre de jours")

    # onchange handler
    @api.onchange('product_uom_qty', 'nombreJours')
    def _onchange_price(self):
        # set auto-changing field
        self.price_subtotal = self.product_uom_qty * self.nombreJours
        # Can optionally return a warning and domains


#
#     @api.depends('value')
#     def _value_pc(self):
#     self.value2 = float(self.value) / 100