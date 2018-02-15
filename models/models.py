# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sle_order(models.Model):
    _inherit = 'sale.order'
    lieuEvent = fields.Char("Lieu de l'événement")
    dateEvent = fields.Date("Date l'événement")
    dateMontage = fields.Date("Date de montage")
    dateDemontage = fields.Date("Date de démontage")

class Sle_orderline(models.Model):
    _inherit = 'sale.order.line'
    nombreJours = fields.Integer("Nombre de jours",default=1)

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'nombreJours')
    def _compute_amount(self):
        """
        Calcule le Sous-Total de chaque ligne de la commande.
        _compute_amount() est une fonction de Odoo overridée.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) * line.nombreJours
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })