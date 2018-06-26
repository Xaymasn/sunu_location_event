# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sle_accountinvoice(models.Model):
    _inherit = "account.invoice"
    lieuEvent_ = fields.Char("Lieu de l'événement")
    dateEvent_ = fields.Date("Date l'événement")
    dateMontage_ = fields.Date("Date de montage")
    dateDemontage_ = fields.Date("Date de démontage")

# Modification des lignes de factures.
# On veut calculer le sous-total en multipliant chaque ligne par le nombre de jours de location
class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    # Nombre de jours de location
    nombrejours = fields.Integer("Nombre de jours",default=1,required=True)

    @api.one
    @api.depends('nombrejours', 'price_unit', 'discount', 'invoice_line_tax_ids', 'quantity', 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id', 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        # Prix unitaire d'un article pendant la durée totale de location:
        rentalprice = self.nombrejours * price
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(rentalprice, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        
        # Calcul du sous-total de la ligne
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price * self.nombrejours
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id._get_currency_rate_date()).compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)
        
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign