# -*- coding: utf-8 -*-
from odoo import http

# class HdlabsFactureSenegalbaches(http.Controller):
#     @http.route('/hdlabs_facture_senegalbaches/hdlabs_facture_senegalbaches/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hdlabs_facture_senegalbaches/hdlabs_facture_senegalbaches/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hdlabs_facture_senegalbaches.listing', {
#             'root': '/hdlabs_facture_senegalbaches/hdlabs_facture_senegalbaches',
#             'objects': http.request.env['hdlabs_facture_senegalbaches.hdlabs_facture_senegalbaches'].search([]),
#         })

#     @http.route('/hdlabs_facture_senegalbaches/hdlabs_facture_senegalbaches/objects/<model("hdlabs_facture_senegalbaches.hdlabs_facture_senegalbaches"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hdlabs_facture_senegalbaches.object', {
#             'object': obj
#         })