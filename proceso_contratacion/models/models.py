# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Licitacion(models.Model):
    _name = "proceso.licitacion"
    _rec_name = 'numerolicitacion'

    licitacion_id = fields.Char(compute="nombre", store=True)

    programa_inversion_licitacion = fields.Many2one('generales.programas_inversion', 'Programa de Inversión')

    programar_obra_licitacion = fields.Many2many("partidas.licitacion", string="Partida(s):", ondelete="cascade")

    name = fields.Text(string="Objeto De La Licitación", )
    select = [('1', 'Licitación publica'), ('2', 'Licitación simplificada/Por invitación')]
    tipolicitacion = fields.Selection(select, string="Tipo de Licitación", default="1", )

    numerolicitacion = fields.Char(string="Número de Licitación", )

    estado_obra_desierta = fields.Integer(compute='estadoObraDesierta')
    estado_obra_cancelar = fields.Integer(compute='estadoObraCancelar')

    convocatoria = fields.Char(string="Convocatoria", )
    fechaconinv = fields.Date(string="Fecha Con/Inv", )
    select1 = [('1', 'Estatal'), ('2', 'Nacional'), ('3', 'Internacional')]
    caracter = fields.Selection(select1, string="Carácter", default="1", )
    select2 = [('1', 'Federal'), ('1', 'Estatal')]
    normatividad = fields.Selection(select2, string="Normatividad", default="1", )
    funcionariopresideactos = fields.Char(string="Funcionario que preside actos", )
    puesto = fields.Text(string="Puesto", )
    numerooficio = fields.Char(string="Numero oficio", )
    fechaoficio = fields.Date(string="Fecha oficio", )
    oficioinvitacioncontraloria = fields.Char(string="Oficio invitación contraloría", )
    fechaoficio2 = fields.Date(string="Fecha oficio", )
    notariopublico = fields.Text(string="Notario publico", )
    fechalimiteentregabases = fields.Date(string="Fecha Límite para la entrega de Bases", )
    fecharegistrocompranet = fields.Date(string="Fecha Registro CompraNet", )
    costobasesdependencia = fields.Float(string="Costo de Bases Dependencia", readonly=True)
    costocompranetbanco = fields.Float(string="Costo CompraNET/Banco", readonly=True)
    fechaestimadainicio = fields.Date(string="Fecha Estimada de Inicio", )
    fechaestimadatermino = fields.Date(string="Fecha Estimada de Termino", )
    plazodias = fields.Integer(string="Plazo de Días", )
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

    variable_count = fields.Integer(compute='contar')

    estatus_licitacion = fields.Selection(
        [('borrador', 'Borrador'), ('confirmado', 'Confirmado'), ('validado', 'Validado'), ],
        default='borrador')

    @api.one
    def borrador_progressbar(self):
        self.write({'estatus_licitacion': 'borrador', })

    @api.one
    def confirmado_progressbar(self):
        self.write({'estatus_licitacion': 'confirmado'})

    @api.one
    def validado_progressbar(self):
        self.write({'estatus_licitacion': 'validado'})

    @api.multi
    @api.onchange('programas_inversion_adjudicacion')
    def BorrarTabla(self):
        self.update({
            'programar_obra_adjudicacion': [[5]]
        })

    # METODO CONTADOR DE PARTICIPANTES
    @api.one
    def contar(self):
        count = self.env['proceso.participante'].search_count([('numerolicitacion', '=', self.id)])
        self.variable_count = count

    # METODO DE OBRA DESIERTA
    @api.one
    def estadoObraDesierta(self):
        resultado = self.env['proceso.estado_obra_desierta'].search_count([('numerolicitacion', '=', self.id)])
        self.estado_obra_desierta = resultado

    # METODO DE OBRA CANCELADA
    @api.one
    def estadoObraCancelar(self):
        resultado = self.env['proceso.estado_obra_cancelar'].search_count([('numerolicitacion', '=', self.id)])
        self.estado_obra_cancelar = resultado

    # ENLACE CON LA LICITACION
    @api.one
    def nombre(self):
        self.licitacion_id = self.numerolicitacion


class Participante(models.Model):
    _name = 'proceso.participante'

    licitacion_id = fields.Char(compute="nombre", store=True)
    numerolicitacion = fields.Many2one('proceso.licitacion', string='Numero Licitación:',
                                       readonly=True)
    contratista_participantes = fields.Many2many('contratista.contratista')

    @api.one
    def nombre(self):
        self.licitacion_id = self.id


class EstadoObraDesierta(models.Model):
    _name = 'proceso.estado_obra_desierta'
    _rec_name = 'estado_obra_desierta'

    obra_id_desierta = fields.Char(compute="estadoObra", store=True)
    licitacion_id = fields.Char(compute="nombre", store=True)
    estado_obra_desierta = fields.Char(string="estado obra", default="Desierta", readonly=True)
    numerolicitacion = fields.Many2one('proceso.licitacion', string='Numero Licitación:',
                                       readonly=True)
    fecha_desierta = fields.Date(string="Fecha de Desierta:")
    observaciones_desierta = fields.Text(string="Observaciones:")

    @api.one
    def estadoObra(self):
        self.obra_id_desierta = self.estado_obra_desierta

    @api.one
    def nombre(self):
        self.licitacion_id = self.id


class EstadoObraCancelar(models.Model):
    _name = 'proceso.estado_obra_cancelar'

    obra_id_cancelar = fields.Char(compute="estadoObra", store=True)
    licitacion_id = fields.Char(compute="nombre", store=True)
    estado_obra_cancelar = fields.Char(string="estado obra", default="Cancelada", readonly=True)
    numerolicitacion = fields.Many2one('proceso.licitacion', string='Numero Licitación:',
                                       readonly=True)
    fecha_cancelado = fields.Date(string="Fecha de Cancelacion:")
    observaciones_cancelado = fields.Text(string="Observaciones:")

    @api.one
    def estadoObraCancelar(self):
        self.obra_id_cancelar = self.estado_obra_cancelar

    @api.one
    def nombre(self):
        self.licitacion_id = self.id

