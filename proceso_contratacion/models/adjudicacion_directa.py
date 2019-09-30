# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


class AdjudicacionDirecta(models.Model):
    _name = "proceso.adjudicacion_directa"
    _rec_name = "numerocontrato"

    # CAMPO BOOLEAN PARA VERIFICAR SI YA SE CONTRATO ESTA ADJUDICACION
    contratado = fields.Boolean(string="", compute="VerificarContrato")

    #  HACER LOS FILTROS DE RELACION DE PROGRAMAS DE INVERSION CON OBRAS PROGRAMADAS(partidas)
    name = fields.Text(string="Descripción/Meta", required=True)
    programas_inversion_adjudicacion = fields.Many2one('generales.programas_inversion', 'name')
    # /// Partidas
    programar_obra_adjudicacion = fields.Many2many("partidas.adjudicacion", string="Partida(s):", ondelete="cascade")

    iva = fields.Float(string="I.V.A", default=0.16, required=True)

    importe_adjudicacion = fields.Float(string="Importe",)

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
    contratista = fields.Many2one('contratista.contratista', string='Contratista', required=True)

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

    @api.one
    def VerificarContrato(self):
        contrato = self.env['proceso.elaboracion_contrato'].search_count([('adjudicacion', '=', self.numerocontrato)])
        if contrato > 0:
            self.contratado = True
        else:
            self.contratado = False

    @api.onchange('programar_obra_adjudicacion')
    def importe(self):
        suma = 0
        for i in self.programar_obra_adjudicacion:
            resultado = i.total_partida
            suma += resultado
            self.importe_adjudicacion = suma

    # METODO PARA INGRESAR A RECURSOS CON EL BOTON
    @api.multi
    def recursos(self):
        view = self.env.ref('proceso_contratacion.recursos_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'recursos',
            'res_model': 'proceso.adjudicacion_directa',
            'view_mode': 'form',
            'target': 'new',
            'view_id': view.id,
            'res_id': self.id,
        }

    # METODO DE EXCEPCION DE LA FECHA ANTERIOR
    @api.onchange('fechatermino')
    @api.depends('fechatermino', 'fechainicio')
    def onchange_date(self):
        if str(self.fechatermino) < str(self.fechainicio):
            raise exceptions.Warning('No se puede seleccionar una Fecha anterior a la actual, '
                                     'por favor seleccione una fecha actual o posterior')
        else:
            return False

    # METODO PARA SUMA DE RECURSOS
    @api.depends('recurso_federal', 'recurso_federal_indirecto', 'recurso_estatal', 'recurso_estatal_indirecto',
                 'recurso_municipal', 'recurso_municipal_indirecto', 'recurso_otros')
    def sumaRecursos(self):
        for rec in self:
            rec.update({
                'total_recurso': (rec.recurso_federal + rec.recurso_federal_indirecto + rec.recurso_estatal +
                                  rec.recurso_estatal_indirecto + rec.recurso_municipal + rec.recurso_municipal_indirecto +
                                  rec.recurso_otros)
            })

