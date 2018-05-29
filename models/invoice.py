# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sle_accountinvoice(models.Model):
    _inherit = "account.invoice"
    lieuEvent_ = fields.Char("Lieu de l'événement")
    dateEvent_ = fields.Date("Date l'événement")
    dateMontage_ = fields.Date("Date de montage")
    dateDemontage_ = fields.Date("Date de démontage")

class Sle_accountinvoiceline(models.Model):
    _inherit = "account.invoice.line"
    nombreJours_ = fields.Integer("Nombre de jours",default=1)