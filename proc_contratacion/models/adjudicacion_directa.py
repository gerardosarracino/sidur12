# -*- coding: utf-8 -*-

from odoo import models, fields, api


class adjudicaciondirecta(models.Model):
	_name = "proceso.adjudicacion_directa"

	name = fields.Many2one('generales.programas_inversion', 'name')
	partidaimporte = fields.Float(string="Importe", required=True)
	partidiva = fields.Float(string="Importe IVA", required=True)
	partidatotal = fields.Float(string="Total", required=True)
	descripcionmeta = fields.Text(string="Descripción/Meta", required=True)
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