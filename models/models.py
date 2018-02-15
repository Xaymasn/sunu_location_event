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
    """
        Nous allons mettre à jour le prix pour qu'il soit égal au prix unitaire multiplié par le nombre de jours
    """
    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            # C'est dans cette ligne qu'on multiplie par le nombre de jours
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) * nombreJours
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            #This gets the delivery_price
            total=0
            for delivery_line in line.delivery_lines:
                total+=delivery_line.delivery_price

            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])+total
    return res


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