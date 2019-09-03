# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class ElaboracionContratos(models.Model):
    _name = "proceso.elaboracion_contrato"
    _rec_name = 'contrato'

    contrato_partida_licitacion = fields.Many2many('partidas.partidas', ondelete="cascade")

    # contrato_partida_adjudicacion = fields.Many2many('partidas.partidas')
    contrato_partida_adjudicacion = fields.Many2many('partidas.partidas', ondelete="cascade")

    contrato_id = fields.Char(compute="nombre", store=True)

    # LICITACION
    obra = fields.Many2one('proceso.licitacion', string="Seleccionar obra")

    # ADJUDICACION
    adjudicacion = fields.Many2one('proceso.adjudicacion_directa', string="Nombre de Adjudicacion")

    fecha = fields.Date(string="Fecha", required=True)
    contrato = fields.Char(string="Contrato", required=True)

    name = fields.Text(string="Descripción/Meta", required=True)
    descripciontrabajos = fields.Text(string="Descripción trabajos:", required=True)
    unidadresponsableejecucion = fields.Char(string="Unidad responsable de su ejecución", required=True)
    supervisionexterna = fields.Text(string="Supervisión externa")
    supervisionexterna1 = fields.Many2one('proceso.elaboracion_contrato', string="Supervisión externa:")

    # VER SI SON NECESARIOS
    importe_contrato = fields.Float(string="Importe:")
    iva_contrato = fields.Float(string="IVA:")
    portentaje_iva_contrato = fields.Float(string="% IVA:")
    total_contrato = fields.Float(string="Total:")
    total = fields.Float(string="Total", readonly=True)
    # ///
    # VINCULO CON ADJUDICACION TRAER DATOS PENDIENTE
    contratista = fields.Char(string="Contratista", readonly=True, default="POR ASIGNAR")
    fechainicio = fields.Date(string="Fecha de Inicio", required=True)
    fechatermino = fields.Date(string="Fecha de Termino", required=True)

    select = [('1', 'Diario'), ('2', 'Mensual'), ('3', 'Ninguno')]
    periodicidadretencion = fields.Selection(select, string="Periodicidad Retención", required=True, default="3")
    retencion = fields.Float(string="% Retencion")

    # Fianzas
    fianzas = fields.Many2many('proceso.fianza', string="Fianzas:")

    # Deducciones
    deducciones = fields.Many2many("generales.deducciones", string="Deducciones")
    # ANTICIPOS
    anticipos = fields.Many2many('proceso.anticipo_contratos', string="Anticipos:")

    @api.multi
    @api.onchange('adjudicacion')  # if these fields are changed, call method
    def check_change_adjudicacion(self):
        adirecta_id = self.env['proceso.adjudicacion_directa'].browse(self.adjudicacion.id)
        self.update({
            'contrato_partida_adjudicacion': [[5]]
        })
        for partidas in adirecta_id.programar_obra_adjudicacion:
            self.update({
                'contrato_partida_adjudicacion': [[0, 0, {'obra': partidas.obra,
                                                          'programaInversion': partidas.programaInversion,
                                                          'monto_partida': partidas.monto_partida,
                                                          'iva_partida': partidas.iva_partida,
                                                          'total_partida': partidas.total_partida}]]
                     })





    @api.model
    def create(self, values):
        self.write({
            'contrato_partida_adjudicacion': [(0, 0, {'numero_contrato': self.contrato})]
        })
        return super(ElaboracionContratos, self).create(values)






    @api.multi
    @api.onchange('obra')  # if these fields are changed, call method
    def check_change_licitacion(self):
        adirecta_id = self.env['proceso.licitacion'].browse(self.obra.id)
        self.update({
            'contrato_partida_licitacion': [[5]]
        })
        for partidas in adirecta_id.programar_obra_licitacion:
            self.update({
                'contrato_partida_licitacion': [[0, 0, {'obra': partidas.obra,
                                                          'programaInversion': partidas.programaInversion,
                                                          'monto_partida': partidas.monto_partida,
                                                          'iva_partida': partidas.iva_partida,
                                                          'total_partida': partidas.total_partida}]]
            })

    @api.one
    def nombre(self):
        self.contrato_id = self.contrato

    # CONVENIOS MODIFICATORIOS
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

    # FINIQUITAR CONTRATO
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

    #
    @api.multi
    def Seleccion(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seleccion de Obra',
            'res_model': 'proceso.elaboracion_contrato',
            'view_type': 'form',
            'target': 'new',
        }


class Fianza(models.Model):
    _name = 'proceso.fianza'

    select_tipo_fianza = [('1', 'Cumplimiento'), ('2', 'Calidad/Vicios Ocultos'), ('3', 'Responsabilidad Civil'),
                          ('4', 'Ninguno')]
    tipo_fianza = fields.Selection(select_tipo_fianza, string="Tipo Fianza", default="4")
    numero_fianza_fianzas = fields.Integer(string="Numero Fianza")
    monto = fields.Float(string="Monto")
    fecha_fianza_fianzas = fields.Float(string="Fecha Fianza")
    afianzadora_fianzas = fields.Char(string="Afianzadora")


class AnticipoContratos(models.Model):
    _name = "proceso.anticipo_contratos"

    obra = fields.Many2one('partidas.partidas', string="Obra:")

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

    name = fields.Char()
    sequence = fields.Integer()
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="")
    # prueba
    obra = fields.Many2one('partidas.partidas', string='Obra:', )

    categoria = fields.Many2one('proceso.categoria')
    concepto = fields.Many2one('proceso.concepto')
    grupo = fields.Many2one('proceso.grupo')
    medida = fields.Many2one('proceso.medida')
    precio_unitario = fields.Float()
    cantidad = fields.Integer()

    # CONCEPTOS EJECUTADOS EN EL PERIODO
    # contratada = fields.Float(string="Contratada",  required=False, compute="test")
    est_ant = fields.Integer(string="Est. Ant",  required=False, compute="sumaEst")
    pendiente = fields.Integer(string="Pendiente",  required=False, compute="Pendiente")
    estimacion = fields.Integer(string="Estimacion",  required=False, )
    importe_ejecutado = fields.Float(string="Importe",  required=False, compute="importeEjec")

    importe = fields.Float(compute="sumaCantidad")

    @api.depends('cantidad', 'estimacion')
    def sumaEst(self):
        for rec in self:
            rec.update({
                'est_ant': rec.cantidad - rec.estimacion
            })

    # VER COMO PROGRAMAREMOS EL ESTIMADO ANTERIOR DE OTRA ESTIMACION DE LA MISMA PROCEDENCIA
    @api.depends('cantidad', 'estimacion')
    def Pendiente(self):
        for rec in self:
            rec.update({
                'pendiente': rec.cantidad - rec.estimacion
            })

    @api.depends('precio_unitario', 'estimacion')
    def importeEjec(self):
        for rec in self:
            rec.update({
                'importe_ejecutado': rec.estimacion * rec.precio_unitario
            })

    @api.one
    def test(self):
        return 0

    @api.depends('precio_unitario', 'cantidad')
    def sumaCantidad(self):
        for rec in self:
            rec.update({
                'importe': rec.cantidad * rec.precio_unitario
            })

    '''@api.model
    def create(self, values):
        if values.get('display_type', self.default_get(['display_type'])['display_type']):
            values.update(categoria=False, concepto=False, grupo=False, medida=0, precio_unitario=0, cantidad=0, importe=0)
        line = super(conceptos_partidas, self).create(values)
        return line

    @api.multi
    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(
                "You cannot change the type of a sale order line. Instead you should delete the current line and create a new line of the proper type.")
        result = super(conceptos_partidas, self).write(values)
        return result'''




