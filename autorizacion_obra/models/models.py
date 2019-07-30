# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class AutorizacionDeObra(models.Model):
    _name = 'autorizacion_obra.oficios_autorizacion'
    _rec_name = 'numero_de_oficio'
    name = fields.Char(compute="nombre",store=True)
    numero_de_oficio = fields.Char(string='Número de oficio', required=True)
    fecha_actual = fields.Date(string='Fecha',default=datetime.now().strftime('%Y-%m-%d'), required=True)
    fecha_de_recibido = fields.Date(string='Fecha de recibido', required=True)
    fecha_de_vencimiento = fields.Date(string='Fecha de vencimiento', required=True)
    importe = fields.Float(string='Importe', required=True)
    variable_count = fields.Integer(compute='contar')

    @api.one
    def contar(self):
        count = self.env['autorizacion_obra.at'].search_count([('numero_de_oficio', '=', self.id)])
        self.variable_count = count
    


    @api.one
    def nombre(self):
        self.name = self.numero_de_oficio


    @api.multi
    def anexoTecnico(self):
        context = {
            'default_numero_de_oficio': self.id
        }
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'autorizacion_obra.at',
                'view_mode': 'form',
                'context': context,
                'target': 'new',
                }


class AnexoTecnico(models.TransientModel): 
    _name = 'autorizacion_obra.at'

    name = fields.Char(compute="nombre",store=True)
    numero_de_oficio = fields.Many2one('autorizacion_obra.oficios_autorizacion',string='Número de oficio', readonly=True)
    clave_de_obra = fields.Char(string='Clave de obra', required=True)
    clave_presupuestal = fields.Char(string='Clave presupuestal', required=True)
    monto_federal = fields.Float(string='Monto federal')
    monto_federal_indirecto = fields.Float(string='Monto federal indirecto')
    monto_estatal = fields.Float(string='Monto estatal')
    monto_estatal_indirecto = fields.Float(string='Monto estatal indirecto')
    monto_municipal = fields.Float(string='Monto municipal')
    monto_municipal_indirecto = fields.Float(string='Monto municipal indirecto')
    otros = fields.Float(string='Otros')
    monto_otros_indirecto = fields.Float(string='Otros indirecto')
    suma = fields.Char(string='Total', compute='_suma')


    @api.one
    def nombre(self):
        self.name = self.id


    @api.depends('monto_federal','monto_federal_indirecto',
                 'monto_estatal','monto_estatal_indirecto',
                 'monto_municipal','monto_municipal_indirecto',
                 'otros','monto_otros_indirecto')
    def _suma(self):
        for rec in self: 
            rec.update({
                'suma': sum([rec.monto_federal,
                             rec.monto_federal_indirecto,
                             rec.monto_estatal,
                             rec.monto_estatal_indirecto,
                             rec.monto_municipal,
                             rec.monto_municipal_indirecto,
                             rec.monto_otros_indirecto],rec.otros)
            })

    
