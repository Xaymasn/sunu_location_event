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
    nombreJours = fields.Integer("Nombre de jours",default=1,required=True)

    @api.one
    @api.depends('nombreJours','price_unit', 'discount', 'invoice_line_tax_ids', 'quantity', 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id', 'invoice_id.date_invoice', 'invoice_id.date')

    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.nombreJours, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)

        # Calcul du sous-total de la ligne
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price * self.nombreJours
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal

        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id._get_currency_rate_date()).compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)

        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign

# Modification du modèle de Taxes
class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.multi
    def compute_all(self, price_unit, currency=None, nombreJours=1, quantity=1.0, product=None, partner=None):
        if len(self) == 0:
            company_id = self.env.user.company_id
        else:
            company_id = self[0].company_id
        if not currency:
            currency = company_id.currency_id
        taxes = []
        prec = currency.decimal_places
        round_tax = False if company_id.tax_calculation_rounding_method == 'round_globally' else True
        round_total = True
        if 'round' in self.env.context:
            round_tax = bool(self.env.context['round'])
            round_total = bool(self.env.context['round'])

        if not round_tax:
            prec += 5
        # total_excluded = total_included = base = round(price_unit * quantity, prec)
        # Modification du calcul de taxe
        total_excluded = total_included = base = price_unit * float(quantity) * int(nombreJours)

        for tax in self.sorted(key=lambda r: r.sequence):
            if tax.amount_type == 'group':
                ret = tax.children_tax_ids.compute_all(price_unit, currency, quantity, product, partner)
                total_excluded = ret['total_excluded']
                base = ret['base']
                total_included = ret['total_included']
                tax_amount = total_included - total_excluded
                taxes += ret['taxes']
                continue

            tax_amount = tax._compute_amount(base, price_unit, quantity, product, partner)
            if not round_tax:
                tax_amount = round(tax_amount, prec)
            else:
                tax_amount = currency.round(tax_amount)

            if tax.price_include:
                total_excluded -= tax_amount
                base -= tax_amount
            else:
                total_included += tax_amount
            
            tax_base = base
            
            if tax.include_base_amount:
                base += tax_amount

            taxes.append({
                'id': tax.id,
                'name': tax.with_context(**{'lang': partner.lang} if partner else {}).name,
                'amount': tax_amount,
                'sequence': tax.sequence,
                'account_id': tax.account_id.id,
                'refund_account_id': tax.refund_account_id.id,
                'analytic': tax.analytic,
                'base': tax_base,
            })
        return {
            'taxes': sorted(taxes, key=lambda k: k['sequence']),
            'total_excluded': total_excluded,
            'total_included': total_included,
            'base': base,
    }