# -*- coding: utf-8 -*-
# from odoo import http


# class Installments(http.Controller):
#     @http.route('/installments/installments', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/installments/installments/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('installments.listing', {
#             'root': '/installments/installments',
#             'objects': http.request.env['installments.installments'].search([]),
#         })

#     @http.route('/installments/installments/objects/<model("installments.installments"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('installments.object', {
#             'object': obj
#         })
