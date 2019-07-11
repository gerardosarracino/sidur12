# -*- coding: utf-8 -*-
from odoo import http

# class AutorizacionDeObra(http.Controller):
#     @http.route('/autorizacion_de_obra/autorizacion_de_obra/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/autorizacion_de_obra/autorizacion_de_obra/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('autorizacion_de_obra.listing', {
#             'root': '/autorizacion_de_obra/autorizacion_de_obra',
#             'objects': http.request.env['autorizacion_de_obra.autorizacion_de_obra'].search([]),
#         })

#     @http.route('/autorizacion_de_obra/autorizacion_de_obra/objects/<model("autorizacion_de_obra.autorizacion_de_obra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('autorizacion_de_obra.object', {
#             'object': obj
#         })