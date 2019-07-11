# -*- coding: utf-8 -*-

from odoo import models, fields, api


class elaboracioncontratos(models.Model):
	_name = "proceso.elaboracion_contratos"

	name = fields.Char(string="Seleccionar obra", required=True)
	fecha = fields.Date(string="Fecha", required=True)
	contrato = fields.Char(string="Contrato", required=True)
	descripcionmeta = fields.Text(string="Descripción/Meta", required=True)
	descripciontrabajos = fields.Text(string="Descripción trabajos:", required=True)
	unidadresponsableejecucion = fields.Char(string="Unidad responsable de su ejecución", required=True)
	supervisionexterna = fields.Text(string="Supervisión externa")
	supervisionexterna1 = fields.Char(string="Supervisión externa1")
	total = fields.Float(string="Total", required=True)
	contratista = fields.Char(string="Contratista", required=True)
	fechainicio = fields.Date(string="Fecha de Inicio", required=True)
	fechatermino = fields.Date(string="Fecha de Termino", required=True)
	select = [('1', 'Diario'), ('2', 'Mensual')]
	periodicidadretencion = fields.Selection(select, string="Periodicidad Retención", required=True)
	retencion = fields.Float(string="% Retencion")

	# Anticipo
	fecha_anticipo = fields.Date(string="Fecha Anticipo")
	obra = fields.Text(string="Obra")
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

	# Fianzas
	select_tipo_fianza = [('1', 'Cumplimiento'), ('2', 'Calidad/Vicios Ocultos'), ('3', 'Responsabilidad Civil')]
	tipo_fianza = fields.Selection(select_tipo_fianza, string="Tipo Fianza", default="1")
	numero_fianza_fianzas = fields.Integer(string="Numero Fianza")
	monto = fields.Float(string="Monto")
	fecha_fianza_fianzas = fields.Float(string="Fecha Fianza")
	afianzadora_fianzas = fields.Float(string="Afianzadora")

	# Deducciones
	deducciones = fields.Many2one("generales.deducciones", string="Deducciones")


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