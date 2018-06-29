# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    lieuEvent_ = fields.Char("Lieu de l'événement")
    dateEvent_ = fields.Date("Date l'événement")
    dateMontage_ = fields.Date("Date de montage")
    dateDemontage_ = fields.Date("Date de démontage")
    # Le type de remise
    discount_type = fields.Selection([('percent', 'Pourcentage'), ('amount', 'Montant fixe')], string='Type de remise', readonly=True, states={'draft': [('readonly', False)]}, default='percent')
    # Le taux de remise
    discount_rate = fields.Float('Remise', digits=(16, 2), readonly=True, states={'draft': [('readonly', False)]})
    # Montant de la remise
    amount_discount = fields.Monetary(string='Remise', store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    # Montant négatif de la remise (juste utilisé à des fins d'affichage)
    amount_discount_negative = fields.Monetary(string='Remise', store=True, readonly=True, compute='_compute_amount', digits=dp.get_precision('Account'), track_visibility='always')
    # Montant sans rabais (coût initial avant rabais)
    amount_without_discount = fields.Monetary(string='Montant initial', store=True, readonly=True, compute='_compute_amount', digits=dp.get_precision('Account'), track_visibility='always')

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding', 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        for line in self.invoice_line_ids:
            # Le sous-total (HT) des articles
            self.amount_untaxed += line.price_subtotal
            # La remise totale des articles
            self.amount_discount += (line.quantity * line.price_unit * line.discount * line.nombrejours) / 100

        for line in self.tax_line_ids:
            # Le montant des taxes
            self.amount_tax += line.amount_total

        self.amount_total = self.amount_untaxed + self.amount_tax

        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

        self.amount_discount_negative = (-1) * self.amount_discount
        self.amount_without_discount = self.amount_untaxed + self.amount_discount

    @api.onchange('discount_type', 'discount_rate', 'invoice_line_ids')
    def supply_rate(self):
        """
        Mise à jour des taux de remise linéaire
        :return:
        """
        for inv in self:
            if inv.discount_type == 'percent':
                for line in inv.invoice_line_ids:
                    line.discount = inv.discount_rate
            else:
                total = discount = 0.0
                for line in inv.invoice_line_ids:
                    total += (line.quantity * line.price_unit)
                if inv.discount_rate != 0:
                    discount = (inv.discount_rate / total) * 100
                else:
                    discount = inv.discount_rate
                for line in inv.invoice_line_ids:
                    line.discount = discount

    @api.multi
    def compute_invoice_totals(self, company_currency, invoice_move_lines):
        """
        Calcul des différents totaux de la facture : Total HT/TTC de la facure, rabais, etc.
        :param company_currency:
        :param invoice_move_lines:
        :return:
        """
        total = 0
        total_currency = 0
        for line in invoice_move_lines:
            if self.currency_id != company_currency:
                currency = self.currency_id.with_context(
                    date=self.date or self.date_invoice or fields.Date.context_today(self))
                line['currency_id'] = currency.id
                line['amount_currency'] = currency.round(line['price'])
                line['price'] = currency.compute(line['price'], company_currency)
            else:
                line['currency_id'] = False
                line['amount_currency'] = False
                line['price'] = line['price']
            if self.type in ('out_invoice', 'in_refund'):
                total += line['price']
                total_currency += line['amount_currency'] or line['price']
                line['price'] = - line['price']
            else:
                total -= line['price']
                total_currency -= line['amount_currency'] or line['price']
        return total, total_currency, invoice_move_lines

    @api.multi
    def button_dummy(self):
        self.supply_rate()
        return True


# Modification des lignes de factures.
# On veut calculer le sous-total en multipliant chaque ligne par le nombre de jours de location
class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    # Nombre de jours de location
    nombrejours = fields.Integer("Nombre de jours",default=1,required=True)
    # Taux de remise linéaire
    discount = fields.Float(string='Discount (%)', digits=(16, 20), default=0.0)

    @api.one
    @api.depends('nombrejours', 'price_unit', 'discount', 'invoice_line_tax_ids', 'quantity', 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id', 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        """
        Calcul des différents prix de la ligne de facture : Prix de l'article, prix de la location, rabais, montants HT/TTC de la ligne
        :return:
        """
        currency = self.invoice_id and self.invoice_id.currency_id or None
        # Prix de vente d'un article
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        # Prix de vente * 'Durée de location' d'un article
        rentalprice = self.nombrejours * price
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(rentalprice, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        
        # Total HT de la ligne de facture
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price * self.nombrejours
        # Total TTC de la ligne de facture
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id._get_currency_rate_date()).compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)
        
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign