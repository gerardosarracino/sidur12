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
    total_at = fields.Float(string='Total suma anexos',compute='suma_total_anexos')
    
    
    @api.one
    def suma_total_anexos(self):
        ids = self.env['autorizacion_obra.aut'].search([('numero_de_oficio', '=', self.id)])
        suma = 0
        for i in ids:
            resultado = self.env['autorizacion_obra.aut'].browse(i.id).suma_
            suma += float(resultado)
        self.total_at = suma


    @api.one
    def contar(self):
        count = self.env['autorizacion_obra.aut'].search_count([('numero_de_oficio', '=', self.id)])
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
                'res_model': 'autorizacion_obra.aut',
                'view_mode': 'form',
                'context': context,
                'target': 'new',
                }
  
class anexo_tecnico(models.Model): 
    _name = 'autorizacion_obra.aut'
    _rec_name = 'suma_'     
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
    suma_ = fields.Float(string='Total', compute='suma')
    obra_programada = fields.Many2one('registro.obra',string='Seleccione la obra a la que corresponde los recursos')
    obra_seleccionada = fields.Char(string='Concepto',compute='obra_selecc')


    @api.onchange('obra_programada')
    def obra_selecc(self):
        resultado = self.env['registro.obra'].browse(int(self.obra_programada)).descripcion 
        self.obra_seleccionada = resultado
    
    @api.one
    def nombre(self):
        self.name = self.id


    @api.depends('monto_federal','monto_federal_indirecto',
                 'monto_estatal','monto_estatal_indirecto',
                 'monto_municipal','monto_municipal_indirecto',
                 'otros','monto_otros_indirecto')
    
    def suma(self):
        for rec in self: 
            rec.update({
                'suma_': sum([rec.monto_federal, 
                             rec.monto_federal_indirecto,
                             rec.monto_estatal,
                             rec.monto_estatal_indirecto,
                             rec.monto_municipal,
                             rec.monto_municipal_indirecto,
                             rec.monto_otros_indirecto],rec.otros)
            })

