# -*- coding: utf-8 -*-

from odoo import models, fields, api


class adjudicaciondirecta(models.Model):
    _name = "proceso.adjudicacion_directa"

    programas_inversion_adjudicacion = fields.Many2one('generales.programas_inversion', 'name')

    partidaimporte = fields.Float(string="Importe", required=True)
    partidiva = fields.Float(string="Importe IVA", required=True, default="0.16")
    partidatotal = fields.Float(string="Total", required=True, compute="sumaProgramas")

    name = fields.Text(string="Descripción/Meta", required=True)

    numerocontrato = fields.Char(string="Numero Contrato", required=True)
    fechaadjudicacion = fields.Date(string="Fecha de Adjudicación", required=True)
    dictamen = fields.Char(string="Dictamen", required=True)
    select = [('1', 'Federal'), ('2', 'Estatal')]
    normatividad = fields.Selection(select, string="Normatividad", default="1", required=True)
    importeadjudicacion = fields.Float(string="Importe de Adjudicación", required=True)
    iva = fields.Float(string="I.V.A", default="0.16", required=True)
    importeiva = fields.Float(string="Importe de I.V.A", required=True)
    totaladjudicado = fields.Float(string="Total Adjudicado", required=True)
    anticipoinicio = fields.Float(string="Anticipo Inicio %")
    anticipomaterial = fields.Float(string="Anticipo Material %")
    fechainicio = fields.Date(string="Fecha de Inicio", required=True)
    fechatermino = fields.Date(string="Fecha termino", required=True)
    plazodias = fields.Integer(string="Plazo/Días", required=True)

    contratista = fields.Many2many('contratista.contratista', string='Contratista')

    # Recursos
    # FALTA LA RELACION, NECESITO EL MODULO DE AUTORIZACION DE OBRAS
    # oficio_autorizacion = fields.Many2many('oficios.autorizacion', string="Seleccione un oficio de autorización")

    recurso_federal = fields.Float(string="Federal")
    recurso_federal_indirecto = fields.Float(string="Federal Indirecto")

    recurso_estatal = fields.Float(string="Estatal")
    recurso_estatal_indirecto = fields.Float(string="Estatal Indirecto")

    recurso_municipal = fields.Float(string="Municipal")
    recurso_municipal_indirecto = fields.Float(string="Municipal Indirecto")

    recurso_otros = fields.Float(string="Otros")

    total_recurso = fields.Float(string="Total", compute='sumaRecursos')

    @api.depends('recurso_federal', 'recurso_federal_indirecto', 'recurso_estatal', 'recurso_estatal_indirecto',
                 'recurso_municipal', 'recurso_municipal_indirecto', 'recurso_otros')
    def sumaRecursos(self):
        for rec in self:
            rec.update({
                'total_recurso': (rec.recurso_federal + rec.recurso_federal_indirecto + rec.recurso_estatal +
                                  rec.recurso_estatal_indirecto + rec.recurso_municipal + rec.recurso_municipal_indirecto +
                                  rec.recurso_otros)
            })

    @api.depends('partidaimporte', 'partidiva')
    def sumaProgramas(self):
        for rec in self:
            rec.update({
                'partidatotal': (rec.partidaimporte * rec.partidiva)+rec.partidaimporte
            })
