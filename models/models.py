# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sle_order(models.Model):
    _inherit = 'sale.order'
    lieuEvent = fields.Char("Lieu de l'événement")
    dateEvent = fields.Date("Date l'événement")
    dateMontage = fields.Date("Date de montage")
    dateDemontage = fields.Date("Date de démontage")
    nombreJours = fields.Integer("Nombre de jours")

class Sle_orderline(models.Model):
    _inherit = 'sale.order.line'
    nombreJours = fields.Integer("Nombre de jours")

    @api.onchange('product_uom_qty', 'nombreJours','unit_price')
    def _onchange_price(self):
        self.price_subtotal = self.product_uom_qty * self.nombreJours * self.unit_price
        # Can optionally return a warning and domains


#
#     @api.depends('value')
#     def _value_pc(self):
#     self.value2 = float(self.value) / 100