# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ElaboracionContratos(models.Model):
    _name = "proceso.elaboracion_contrato"
    _rec_name = 'contrato'

    contrato_id = fields.Char(compute="nombre", store=True)

    obra = fields.Many2one('proceso.licitacion', string="Seleccionar obra")
    adjudicacion = fields.Many2one('proceso.adjudicacion_directa', string="Seleccionar obra")

    fecha = fields.Date(string="Fecha", required=True)

    contrato = fields.Char(string="Contrato", required=True)

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


class AnticipoContratos(models.Model):
    _name = "proceso.anticipo_contratos"

    contrato_id = fields.Char(compute="nombre", store=True)
    contrato = fields.Many2one('proceso.elaboracion_contrato', string='Numero Contrato:', readonly=True)

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