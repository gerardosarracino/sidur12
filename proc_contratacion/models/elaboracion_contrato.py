# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ElaboracionContratos(models.Model):
    _name = "proceso.elaboracion_contrato"
    _rec_name = 'contrato'

    contrato_partida = fields.Many2many('proceso.contrato_partidas')

    contrato_id = fields.Char(compute="nombre", store=True)
    obra = fields.Many2one('proceso.licitacion', string="Seleccionar obra")

    adjudicacion = fields.Many2one('proceso.adjudicacion_directa', string="Nombre de Adjudicacion")

    fecha = fields.Date(string="Fecha", required=True)

    contrato = fields.Char(string="Contrato")

    name = fields.Text(string="Descripción/Meta", required=True)
    descripciontrabajos = fields.Text(string="Descripción trabajos:", required=True)
    unidadresponsableejecucion = fields.Char(string="Unidad responsable de su ejecución", required=True)
    supervisionexterna = fields.Text(string="Supervisión externa")
    # relacion con autorizacion de obra pendiente
    supervisionexterna1 = fields.Char(string="Supervisión externa")

    importe_contrato = fields.Float(string="Importe:")
    iva_contrato = fields.Float(string="IVA:")
    portentaje_iva_contrato = fields.Float(string="% IVA:")
    total_contrato = fields.Float(string="Total:")

    total = fields.Float(string="Total", readonly=True)

    # falta relacion con el contratista de la obra seleccionada, nose cuando aparece
    contratista = fields.Char(string="Contratista", readonly=True, default=".")
    fechainicio = fields.Date(string="Fecha de Inicio", required=True)
    fechatermino = fields.Date(string="Fecha de Termino", required=True)
    select = [('1', 'Diario'), ('2', 'Mensual'), ('3', 'Ninguno')]
    periodicidadretencion = fields.Selection(select, string="Periodicidad Retención", required=True, default="3")
    retencion = fields.Float(string="% Retencion")

    new_field_ids = fields.Many2many(comodel_name="proceso.anticipo_contratos")

    # FALTA HACER LOS CAMPOS DE LA TABLA EN MODO EDITAR, CLAVE PRESUPUESTAL, RECURSOS AUTORIZADOS ETC...
    # RELACION CON REGISTRO DE OBRAS Y/0 OBRAS AUTORIZADAS
    # Fianzas
    select_tipo_fianza = [('1', 'Cumplimiento'), ('2', 'Calidad/Vicios Ocultos'), ('3', 'Responsabilidad Civil'),
                          ('4', 'Ninguno')]
    tipo_fianza = fields.Selection(select_tipo_fianza, string="Tipo Fianza", default="4")
    numero_fianza_fianzas = fields.Integer(string="Numero Fianza")
    monto = fields.Float(string="Monto")
    fecha_fianza_fianzas = fields.Float(string="Fecha Fianza")
    afianzadora_fianzas = fields.Char(string="Afianzadora")
    # Deducciones
    deducciones = fields.Many2many("generales.deducciones", string="Deducciones")

    @api.multi
    @api.onchange('adjudicacion')  # if these fields are changed, call method
    def check_change(self):
        # adirecta_id = self.env['proceso.adjudicacion_directa'].browse('adjudicacion')
        ids = [1]
        self.update({
            'contrato_partida': [[0, 0, {'monto_partida': 0.0}]]
        })

    @api.one
    def nombre(self):
        self.contrato_id = self.contrato

    @api.multi
    def conveniosModificados(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Convenios Modificatorios',
            'res_model': 'proceso.convenios_modificado',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'target': 'self',
        }

    @api.multi
    def finiquitarContrato(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Finiquitar Contrato Anticipadamente',
            'res_model': 'proceso.finiquitar_anticipadamente',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'target': 'self',
        }

    @api.multi
    def AnticipoContrato(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Anticipo Contrato',
            'res_model': 'proceso.anticipo_contratos',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'target': 'current',
        }

    @api.multi
    def Seleccion(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seleccion de Obra',
            'res_model': 'proceso.elaboracion_contrato',
            'view_type': 'form',
            'target': 'new',
        }


class AnticipoContratos(models.Model):
    _name = "proceso.anticipo_contratos"

    contrato = fields.Many2one('proceso.elaboracion_contrato', string='Numero Contrato:', readonly=True)

    contrato_id = fields.Char(compute="nombre", store=True)
    fecha_anticipo = fields.Date(string="Fecha Anticipo")
    porcentaje_anticipo = fields.Float(string="Anticipo Inicio")
    total_anticipo_porcentaje = fields.Float(string="Total Anticipo")
    anticipo_material = fields.Float(string="Anticipo Material")
    importe = fields.Float(string="Importe Contratado")
    anticipo = fields.Integer(string="Anticipo")
    iva = fields.Float(string="I.V.A")
    total_anticipo = fields.Integer(string="Total Anticipo")
    numero_fianza = fields.Float(string="# Fianza")
    afianzadora = fields.Char(string="Afianzadora")
    fecha_fianza = fields.Date(string="Fecha Fianza")

    @api.one
    def nombre(self):
        self.contrato_id = self.id


# MODELO DE PARTIDAS
class ContratoPartidas(models.Model):
    _name = 'proceso.contrato_partidas'

    name = fields.Many2one('registro.programarobra')
    programaInversion = fields.Many2one('generales.programas_inversion', related="name.programaInversion")
    monto_partida = fields.Float(string="Monto", required=False, )
    iva_partida = fields.Float(string="Iva", required=False, compute="iva")
    total_partida = fields.Float(string="Total", required=False, compute="sumaPartidas")

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


class ConveniosModificados(models.Model):
    _name = "proceso.convenios_modificado"

    contrato_id = fields.Char(compute="nombre", store=True)
    contrato = fields.Many2one('proceso.elaboracion_contrato', string='Numero Contrato:', readonly=True)

    fecha_convenios = fields.Date(string="Fecha:")
    name_convenios = fields.Text(string="Obra:")
    referencia = fields.Char(string="Referencia:")
    observaciones = fields.Text(string="Observaciones:")
    fecha_dictamen = fields.Text(string="Fecha Dictamen:")

    # RADIO BUTTON
    radio = [(
        '1', "Plazo"), ('2', "Objeto"), ('3', "Monto"), ('4', "Monto/Plazo"), ]
    tipo_convenio = fields.Selection(radio, string="Tipo de Convenio:")

    # CONDICION PLAZO
    plazo_fecha_inicio = fields.Date(string="Fecha Inicio:")
    plazo_fecha_termino = fields.Date(string="Fecha Termino:")
    # CONDICION OBJETO
    objeto_nuevo_objeto = fields.Text(string="Objeto:")
    # CONDICION MONTO
    select_monto = [(
        '1', "Ampliación:"), ('2', "Reducción:")]
    tipo_monto = fields.Selection(select_monto, string="Monto:")
    monto_importe = fields.Float(string="Importe:")
    monto_iva = fields.Float(string="I.V.A:", default=0.16)
    monto_total = fields.Float(string="Total:", compute="sumaMonto")
    # CONDICION MONTO PLAZO
    monto_plazo_fecha_inicio = fields.Date(string="Fecha Inicio:")
    monto_plazo_fecha_termino = fields.Date(string="Fecha Termino:")
    select_monto_plazo = [(
        '1', "Ampliación:"), ('2', "Reducción:")]
    tipo_monto_plazo = fields.Selection(select_monto_plazo, string="Monto:")
    monto_plazo_importe = fields.Float(string="Importe:")
    monto_plazo_iva = fields.Float(string="I.V.A:", default=0.16)
    monto_plazo_total = fields.Float(string="Total:", compute="sumaMontoPlazo")
    # TERMINA CONDICIONES RADIO BUTTON

    convenio_fecha_fianza = fields.Date(string="Fecha Fianza:")
    convenio_numero_fianza = fields.Integer(string="Numero Fianza:")
    convenio_afianzadora = fields.Char(string="Afianzadora:")
    convenio_monto_afianzadora = fields.Integer(string="Afianzadora:")

    @api.one
    def nombre(self):
        self.contrato_id = self.id

    @api.depends('monto_importe', 'monto_iva')
    def sumaMonto(self):
        for rec in self:
            rec.update({
                'monto_total': (rec.monto_importe * rec.monto_iva) + rec.monto_importe
            })

    @api.depends('monto_plazo_importe', 'monto_plazo_iva')
    def sumaMontoPlazo(self):
        for rec in self:
            rec.update({
                'monto_plazo_total': (rec.monto_plazo_importe * rec.monto_plazo_iva) + rec.monto_plazo_importe
            })


class FiniquitarContratoAnticipadamente(models.Model):
    _name = "proceso.finiquitar_anticipadamente"

    @api.one
    def nombre(self):
        self.contrato_id = self.id

    contrato_id = fields.Char(compute="nombre", store=True)
    contrato = fields.Many2one('proceso.elaboracion_contrato', string='Numero Contrato:', readonly=True)

    fecha = fields.Date(string="Fecha:")
    referencia = fields.Char(string="Referencia:")
    observaciones = fields.Text(string="Observaciones:")


class categoria(models.Model):
    _name = "proceso.categoria"
    name = fields.Char()


class concepto(models.Model):
    _name = "proceso.concepto"
    name = fields.Char()


class grupo(models.Model):
    _name = "proceso.grupo"
    name = fields.Char()


class medida(models.Model):
    _name = "proceso.medida"
    name = fields.Char()


class conceptos_partidas(models.Model):
    _name = "proceso.conceptos_part"

    # name = fields.Many2one('proceso.elaboracion_contrato')
    categoria = fields.Many2one('proceso.categoria')
    concepto = fields.Many2one('proceso.concepto')
    grupo = fields.Many2one('proceso.grupo')
    medida = fields.Many2one('proceso.medida')
    precio_unitario = fields.Float()
    cantidad = fields.Integer()

    importe = fields.Float(compute="sumaCantidad")

    # importe2 = fields.Float(compute="xd")

    @api.depends('precio_unitario', 'cantidad')
    def sumaCantidad(self):
        for rec in self:
            rec.update({
                'importe': rec.cantidad * rec.precio_unitario
            })

# La vista sera de aqui
# class conceptos_model(models.Model):
#     _name = "proceso.conceptos_contratos"
#
#     contrato_partida = fields.Many2many('proceso.contrato_partidas')
#     conceptos_partidas = fields.Many2many('proceso.conceptos_part')
#     name = fields.Many2one('proceso.elaboracion_contrato', readonly=True)
#     total = fields.Float(string="Monto Total del Contrato:", readonly=True)
#     total_contrato = fields.Float(string="Monto Total del Catalogo:", readonly=True, compute="xd")
#     diferencia = fields.Float(string="Diferencia:", compute="sumaConcepto")
#     nombre_contrato = fields.Char()
#
#     # tabla = fields.Many2many("proceso.convenios_modificado", string="Tabla de Convenios Modificatorios", readonly=True)
#     # x = fields.Float(related="conceptos_partidas.importe2")
#
#     @api.multi
#     @api.onchange('name') # if these fields are changed, call method
#     def check_change(self):
#         # adirecta_id = self.env['proceso.adjudicacion_directa'].browse('adjudicacion')
#         ids = [1]
#         self.update({
#             'contrato_partida': [[0, 0, {'monto_partida': 0.0}]]
#         })
#
#     @api.depends('importe')
#     def xd(self):
#         acum = 0
#         # for i in self.env['proceso.conceptos_part'].sudo().search([('importe', 'in', self.ids)]):
#         for i in self.importe:
#             imp = i.importe
#             acum = acum + imp
#             i.update({
#                     'importe2': self.importe2 + imp
#                 })
#
#     @api.multi
#     def xd(self):
#         ids = self.env['proceso.conceptos_part'].search([('importe', '=', self.id)])
#         # r = self.env['proceso.elaboracion_contrato'].sudo().search([('adjudicacion', '=', self.id)])
#         suma = 0
#         for i in ids:
#             # imp = i.importe
#             resultado = self.env['proceso.conceptos_part'].browse(i.id).importe
#             suma = suma + resultado
#             self.total_contrato = suma
#
#     @api.onchange('x')
#     def xd(self):
#         r = self.x
#         self.total_contrato = r
#
#     @api.one
#     def sumaConcepto(self):
#         self.diferencia = 5
# fin
