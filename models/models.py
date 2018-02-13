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
    nombreJours = fields.Integer(string="Nombre de jours", compute="_autoCalcNbJours")
    #nombreJours = fields.Integer("Nombre de jours",default=1)


    #@api.onchange('nombreJours')
    #
    @api.multi
    def _autoCalcNbJours(self):
        for record in self:
            record.nombreJours = 3
        #self.price_subtotal = self.product_uom_qty * self.nombreJours * self.price_unit
        
        # Can optionally return a warning and domains

    # Calcule automatiquement le nombre de jours de location à partir de la date de montage et de la date de démontage
    
    #@api.depends('dateMontage','dateDemontage')
    #def _autoCalcNbJours(self):
    #    for record in self:
    #        record.nombreJours = (dateDemontage - dateMontage).days