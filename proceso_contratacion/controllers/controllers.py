# -*- coding: utf-8 -*-
from odoo import http

# class ProcContratacion(http.Controller):
#     @http.route('/proc_contratacion/proc_contratacion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/proc_contratacion/proc_contratacion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('proc_contratacion.listing', {
#             'root': '/proc_contratacion/proc_contratacion',
#             'objects': http.request.env['proc_contratacion.proc_contratacion'].search([]),
#         })

#     @http.route('/proc_contratacion/proc_contratacion/objects/<model("proc_contratacion.proc_contratacion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proc_contratacion.object', {
#             'object': obj
#         })