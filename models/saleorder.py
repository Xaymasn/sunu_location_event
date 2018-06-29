# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    lieuEvent = fields.Char("Lieu de l'événement")
    dateEvent = fields.Date("Date l'événement")
    dateMontage = fields.Date("Date de montage")
    dateDemontage = fields.Date("Date de démontage")
    # Le type de remise
    discount_type = fields.Selection(
        [('percent', 'Pourcentage'), ('amount', 'Montant fixe')],
        string='Type de remise',
        readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, default='percent'
    )
    # Le taux de remise
    discount_rate = fields.Float('Remise', digits=dp.get_precision('Account'), readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    # Montant sans taxe
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    # Montant total des taxes
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    # Montant Total
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    # Montant de la remise
    amount_discount = fields.Monetary(string='Remise', store=True, readonly=True, compute='_amount_all', digits=dp.get_precision('Account'), track_visibility='always')
    # Montant négatif de la remise (juste utilisé à des fins d'affichage)
    amount_discount_negative = fields.Monetary(string='Remise', store=True, readonly=True, compute='_amount_all', digits=dp.get_precision('Account'), track_visibility='always')
    # Montant sans rabais (coût initial avant rabais)
    amount_without_discount = fields.Monetary(string='Montant initial', store=True, readonly=True, compute='_amount_all', digits=dp.get_precision('Account'), track_visibility='always')

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Calcul des totaux du devis
        :return:
        """
        for order in self:
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_discount += (line.product_uom_qty * line.price_unit * line.nombrejours * line.discount) / 100

            amount_discount_negative = (-1) * amount_discount

            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_discount': order.pricelist_id.currency_id.round(amount_discount),
                'amount_discount_negative': order.pricelist_id.currency_id.round(amount_discount_negative),
                'amount_total': amount_untaxed + amount_tax,
                'amount_without_discount': amount_untaxed + amount_discount,
            })

    # Si un des champs définis est mis à jour, on met à jour le taux de rabais
    @api.onchange('discount_type', 'discount_rate', 'order_line')
    def supply_rate(self):
        """
        Mise à jour des taux de rremise
        :return:
        """
        for order in self:
            # Si le type de remise est en pourcentage, on applique ce taux sur toutes les lignes
            if order.discount_type == 'percent':
                for line in order.order_line:
                    line.discount = order.discount_rate
            # Sinon, on utilise le montant
            else:
                total = discount = 0.0
                for line in order.order_line:
                    total += round((line.product_uom_qty * line.price_unit * line.nombrejours))
                # Ici on calcule la valeur en % (pourcent) du montant fixe de la remise. Parceque Odoo utilise des valeurs en % pour calculer les remises
                if order.discount_rate != 0:
                    discount = (order.discount_rate / total) * 100
                else:
                    discount = order.discount_rate
                for line in order.order_line:
                    line.discount = discount

    @api.multi
    def _prepare_invoice(self, ):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate
        })
        return invoice_vals

    @api.multi
    def button_dummy(self):
        self.supply_rate()
        return True


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    nombrejours = fields.Integer("Nombre de jours", default=1, required=True)
    discount = fields.Float(string='Remise (%)', digits=(16, 20), default=0.0)

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Calcule et met à jour le montant de chaque ligne de devis
        - 'price_tax' : Le total des taxes de la ligne
        - 'price_total' : Le total TTC de la ligne
        - 'price_subtotal' : Le total HT de la ligne
        """
        for line in self:
            # On multiplie le prix initial par le nombre de jours
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) * line.nombrejours
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })