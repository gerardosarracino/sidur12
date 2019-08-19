# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProcesoPartidas(models.Model):
    _name = 'proceso.partidas'

    obra = fields.Many2one('registro.programarobra')


class LicitacionPartidas(models.Model):
    _name = 'proceso.licitacion_partidas'
    _rec_name = "obra"

    obra = fields.Many2one('registro.programarobra')
    programaInversion = fields.Many2one('generales.programas_inversion', related="obra.programaInversion")
    monto_partida = fields.Float(string="Monto",  required=False, )
    iva_partida = fields.Float(string="Iva",  required=False, compute="iva")
    total_partida = fields.Float(string="Total",  required=False, compute="sumaPartidas")

    # NOTA CAMBIAR DESPUES LOS VALORES DE IVA A PERSONALIZADOS NO FIJOS
    # METODOS DE SUMA DEL MANY2MANY 'programar_obra'

    # CONCEPTOS CONTRATADOS DE PARTIDAS
    contrato_partida = fields.Many2many('proceso.contrato_partidas')
    conceptos_partidas = fields.Many2many('proceso.conceptos_part')
    name = fields.Many2one('proceso.elaboracion_contrato', readonly=True)
    total = fields.Float(string="Monto Total Contratado:", readonly=True, compute="totalContrato")
    total_contrato = fields.Float(string="Monto Total del Catálogo:", readonly=True, compute="xd")
    diferencia = fields.Float(string="Diferencia:", compute="Diferencia")

    @api.one
    def sumaConcepto(self):
        self.diferencia = 5

    @api.one
    def totalContrato(self):
        self.total = self.total_partida

    @api.one
    def Diferencia(self):
        self.diferencia = self.total - self.total_contrato

    @api.depends('monto_partida')
    def sumaPartidas(self):
        for rec in self:
            rec.update({
                'total_partida': (rec.monto_partida * 0.16) + rec.monto_partida
            })

    @api.depends('monto_partida')
    def iva(self):
        for rec in self:
            rec.update({
                'iva_partida': (rec.monto_partida * 0.16)
            })

    # METODO PARA SUMAR LOS IMPORTES DE LOS CONCEPTOS
    @api.multi
    def xd(self):
        ids = self.env['proceso.conceptos_part'].search([('importe', '=', self.id)])
        # r = self.env['proceso.elaboracion_contrato'].sudo().search([('adjudicacion', '=', self.id)])
        suma = 0
        for i in ids:
            # imp = i.importe
            resultado = self.env['proceso.conceptos_part'].browse(i.id).importe
            suma = suma + resultado
            self.total_contrato = suma


class Licitacion(models.Model):
    _name = "proceso.licitacion"
    _rec_name = 'numerolicitacion'

    licitacion_id = fields.Char(compute="nombre", store=True)

    programa_inversion_licitacion = fields.Many2one('generales.programas_inversion', 'name')
    programar_obra_licitacion = fields.Many2many("proceso.licitacion_partidas", string="Partida(s):")
    # obra = fields.Many2many('proceso.partidas')

    name = fields.Text(string="Objeto De La Licitación", required=True)
    select = [('1', 'Licitación publica'), ('2', 'Licitación simplificada/Por invitación')]
    tipolicitacion = fields.Selection(select, string="Tipo de Licitación", default="1", required=True)

    numerolicitacion = fields.Char(string="Número de Licitación", required=True)

    estado_obra_desierta = fields.Integer(compute='estadoObraDesierta')
    estado_obra_cancelar = fields.Integer(compute='estadoObraCancelar')

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

    variable_count = fields.Integer(compute='contar')

    cuadro = fields.Integer(compute='contar2')

    @api.one
    def contar(self):
        count = self.env['proceso.participante'].search_count([('numerolicitacion', '=', self.id)])
        self.variable_count = count

    @api.one
    def contar2(self):
        count = self.env['proceso.participante'].search_count([('numerolicitacion', '=', self.id)])
        self.cuadro = count

    @api.one
    def estadoObraDesierta(self):
        resultado = self.env['proceso.estado_obra_desierta'].search_count([('numerolicitacion', '=', self.id)])
        self.estado_obra_desierta = resultado

    @api.one
    def estadoObraCancelar(self):
        resultado = self.env['proceso.estado_obra_cancelar'].search_count([('numerolicitacion', '=', self.id)])
        self.estado_obra_cancelar = resultado

    @api.one
    def nombre(self):
        self.licitacion_id = self.numerolicitacion


class Participante(models.Model):
    _name = "proceso.participante"

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

