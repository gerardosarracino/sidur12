# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class AutorizacionDeObra(models.Model):
    _name = 'autorizacion_de_obra.oficios_de_autorizacion'
    fecha_actual = fields.Date(string='Fecha',default=fields.Date.today(), required=True)
    fecha_de_recibido = fields.Date(string='Fecha de recibido', required=True)
    fecha_de_vencimiento = fields.Date(string='Fecha de vencimiento', required=True)
    numero_de_oficio = fields.Char(string='Número de oficio', required=True)
    importe = fields.Float(string='Importe', required=True)


class AnexoTecnico(models.Model): 
    _name = 'autorizacion_de_obra.anexo_tecnico'
    clave_de_obra = fields.Char(string='Clave de obra', required=True)
    clave_presupuestal = fields.Char(string='Clave presupuestal', required=True)
    monto_federal = fields.Float(string='Monto federal')
    monto_estatal = fields.Float(string='Monto estatal')
    monto_municipal = fields.Float(string='Monto municipal')
    total = fields.Float(string='Total :',compute='suma')

    @api.depends('monto_federal', 'monto_estatal', 'monto_municipal')
    def suma(self):
        for rec in self:
            rec.update({

                'total': (rec.monto_federal + rec.monto_estatal) + rec.monto_municipal,

            })

        # self.campos = sum([self.monto_federal,self.monto_estatal],self.monto_municipal)
        # self.suma = self.campos
        # return self.suma
