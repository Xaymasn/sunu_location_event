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

<<<<<<< HEAD

class Sle_accountinvoice(models.Model):
    _inherit = "account.invoice"
    order_id = fields.Many2one('sale.order', 'Related_order')
    lieuEvent = fields.Char(related='order_id.lieuEvent')
    dateEvent = fields.Date(related='order_id.dateEvent')
    dateMontage = fields.Date(related='order_id.dateMontage')
    dateDemontage = fields.Date(related='order_id.dateDemontage')

#class Sle_accountinvoiceline(models.Model):
#    _inherit = "account.invoice.line"
#    order_id = fields.Many2one('sale.order.line', 'Related_order')
#    nombreJours = fields.Date(related='order_id.nombreJours')


    #@api.onchange('nombreJours')
    #def _onchange_price(self):
        #for record in self:
            #record.price_subtotal = record.price_subtotal * record.nombreJours
        #self.price_subtotal = self.product_uom_qty * self.nombreJours * self.price_unit
        
        # Can optionally return a warning and domains

    # Calcule automatiquement le nombre de jours de location à partir de la date de montage et de la date de démontage
    
    #@api.depends('dateMontage','dateDemontage')
    #def _autoCalcNbJours(self):
    #    for record in self:
    #        record.nombreJours = (dateDemontage - dateMontage).days
=======
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
>>>>>>> 7194cffcb987ccc6fafa538b295be961e6dfa5e0
