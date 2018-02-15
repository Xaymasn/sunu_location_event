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

   # price_subtotal = fields.Float(compute='_amount_line', string='Subtotal')
    

    #self._columns['price_subtotal']._fnct = _amount_line


    # @api.onchange('product_uom_qty','nombreJours','price_unit')
    #def _autoCalcSubTotal(self):
    #   self._columns['price_subtotal']._fnct = _amount_line
    #    for record in self:
    #        record.price_subtotal = record.product_uom_qty * record.nombreJours * record.price_unit
        
        # Can optionally return a warning and domains

    # Calcule automatiquement le nombre de jours de location à partir de la date de montage et de la date de démontage
    
    #@api.depends('dateMontage','dateDemontage')
    #def _autoCalcNbJours(self):
    #    for record in self:
    #        record.nombreJours = (dateDemontage - dateMontage).days