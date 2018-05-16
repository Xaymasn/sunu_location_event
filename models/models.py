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

class Sle_accountinvoice(models.Model):
    _inherit = "account.invoice"
    order_id = fields.Many2one('sale.order', 'Related_order')
    lieuEvent = fields.Char(related='order_id.lieuEvent')
    dateEvent = fields.Date(related='order_id.dateEvent')
    dateMontage = fields.Date(related='order_id.dateMontage')
    dateDemontage = fields.Date(related='order_id.dateDemontage')

class Sle_accountinvoiceline(models.Model):
    _inherit = "account.invoice.line"
    #order_id = fields.Many2one('sale.order.line', 'Related_order')
    nombreJours = fields.Integer("Nombre de jours",default=1)
    #nombreJours = fields.Date(related='order_id.nombreJours')


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
