# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


class AdjudicacionDirecta(models.Model):
    _name = "proceso.adjudicacion_directa"

    #  HACER LOS FILTROS DE RELACION DE PROGRAMAS DE INVERSION CON OBRAS PROGRAMADAS(partidas)
    programas_inversion_adjudicacion = fields.Many2one('generales.programas_inversion', 'name')
    # /// Partidas
    programar_obra_adjudicacion = fields.Many2many("partidas.partidas", string="Partida(s):")

    iva = fields.Float(string="I.V.A", default=0.16, required=True)

    name = fields.Text(string="Descripción/Meta", required=True)

    numerocontrato = fields.Char(string="Numero Contrato", required=True)
    fechaadjudicacion = fields.Date(string="Fecha de Adjudicación", required=True)
    dictamen = fields.Char(string="Dictamen", required=True)
    select = [('1', 'Federal'), ('2', 'Estatal')]
    normatividad = fields.Selection(select, string="Normatividad", default="1", required=True)

    anticipoinicio = fields.Float(string="Anticipo Inicio %")
    anticipomaterial = fields.Float(string="Anticipo Material %")

    fechainicio = fields.Date(string="Fecha de Inicio", required=True, default=fields.Date.today())

    fechatermino = fields.Date(string="Fecha termino", required=True, )

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

    @api.onchange('fechatermino')
    @api.depends('fechatermino', 'fechainicio')
    def onchange_date(self):
        if str(self.fechatermino) < str(self.fechainicio):
            raise exceptions.Warning('No se puede seleccionar una Fecha anterior a la actual, '
                                     'por favor seleccione una fecha actual o posterior')
        else:
            return False

    # Meotod de suma de los recursos
    @api.depends('recurso_federal', 'recurso_federal_indirecto', 'recurso_estatal', 'recurso_estatal_indirecto',
                 'recurso_municipal', 'recurso_municipal_indirecto', 'recurso_otros')
    def sumaRecursos(self):
        for rec in self:
            rec.update({
                'total_recurso': (rec.recurso_federal + rec.recurso_federal_indirecto + rec.recurso_estatal +
                                  rec.recurso_estatal_indirecto + rec.recurso_municipal + rec.recurso_municipal_indirecto +
                                  rec.recurso_otros)
            })

    @api.model
    def create(self, values):
        '''ok = self.programar_obra_adjudicacion
        for i in ok:
            ok['adjudicacion'] = self.id
        return super(AdjudicacionDirecta, self).create(values)'''
