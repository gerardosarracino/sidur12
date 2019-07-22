# -*- coding: utf-8 -*-

from odoo import models, fields, api


class licitacion(models.Model):
    _name = "proceso.licitacion"

    # contratista_participante = fields.Many2many('contratista.contratista', 'name')
    radio = [(
        '1', "Ninguno"), ('2', "Cancelado"), ('3', "Abandonado")]
    estado_radio = fields.Selection(radio, string="Estado de la Obra", default="1")

    fecha_cancelado = fields.Date(string="Fecha de Cancelacion:")
    observaciones_cancelado = fields.Text(string="Observaciones:")

    fecha_desierta = fields.Date(string="Fecha de Desierta:")
    observaciones_desierta = fields.Text(string="Observaciones:")

    # name = fields.Many2one('generales.programas_inversion', 'name')
    programa_inversion = fields.Many2one('generales.programas_inversion', 'name')

    # objetolicitacion = fields.Text(string="Objeto De La Licitación", required=True)
    name = fields.Text(string="Objeto De La Licitación", required=True)

    select = [('1', 'Licitación publica'), ('2', 'Licitación simplificada/Por invitación')]
    tipolicitacion = fields.Selection(select, string="Tipo de Licitación", default="1", required=True)
    numerolicitacion = fields.Char(string="Número de Licitación", required=True)
    convocatoria = fields.Char(string="Convocatoria", required=True)
    fechaconinv = fields.Date(string="Fecha Con/Inv", required=True)
    select1 = [('1', 'Estatal'), ('2', 'Nacional'), ('3', 'Internacional')]
    caracter = fields.Selection(select1, string="Carácter", default="1", required=True)
    select2 = [('1', 'Federal'), ('1', 'Estatal')]
    normatividad = fields.Selection(select2, string="Normatividad", default="1", required=True)
    funcionariopresideactos = fields.Char(string="Funcionario que preside actos", required=True)
    puesto = fields.Text(string="Puesto", required=True)
    numerooficio = fields.Char(string="Numero oficio", required=True)
    fechaoficio = fields.Date(string="Fecha oficio", required=True)
    oficioinvitacioncontraloria = fields.Char(string="Oficio invitación contraloría", required=True)
    fechaoficio2 = fields.Date(string="Fecha oficio", required=True)
    notariopublico = fields.Text(string="Notario publico", required=True)
    fechalimiteentregabases = fields.Date(string="Fecha Límite para la entrega de Bases", required=True)
    fecharegistrocompranet = fields.Date(string="Fecha Registro CompraNet", required=True)
    costobasesdependencia = fields.Float(string="Costo de Bases Dependencia", readonly=True)
    costocompranetbanco = fields.Float(string="Costo CompraNET/Banco", readonly=True)
    fechaestimadainicio = fields.Date(string="Fecha Estimada de Inicio", required=True)
    fechaestimadatermino = fields.Date(string="Fecha Estimada de Termino", required=True)
    plazodias = fields.Integer(string="Plazo de Días", required=True)
    capitalcontable = fields.Float(string="Capital Contable", readonly=True)
    anticipomaterial = fields.Float(string="Anticipo Material %")
    anticipoinicio = fields.Float(string="Anticipo Inicio %")
    puntosminimospropuestatecnica = fields.Char(string="Puntos mínimos propuesta técnica")
    visitafechahora = fields.Datetime(string="Fecha/Hora")
    visitalugar = fields.Text(string="Lugar")
    juntafechahora = fields.Datetime(string="Fecha/Hora")
    juntalugar = fields.Text(string="Lugar")
    aperturafechahora = fields.Datetime(string="Fecha/Hora")
    aperturalugar = fields.Text(string="Lugar")
    fallofechahora = fields.Datetime(string="Fecha/Hora")
    fallolugar = fields.Text(string="Lugar")

    '''participantes= fields = fields.Many2one('proceso.participante',string="Company", default=lambda
        self: self.env['proceso.participante'].search([]))'''


class Participante(models.Model):
    _name = "proceso.participante"

    contratista_participantes = fields.Many2many('contratista.contratista')






# class proc_contratacion(models.Model):
#     _name = 'proc_contratacion.proc_contratacion'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
