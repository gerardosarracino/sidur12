# -*- coding: utf-8 -*-

from odoo import models, fields, api


class licitacion(models.Model):
	_name = "proceso.licitacion"

	name = fields.Many2one('generales.programas_inversion', 'name')
	objetolicitacion = fields.Text(string="Programa de Inversión", required=True)
	select = [('1', 'Licitación publica'), ('2', 'Licitación simplificada/Por invitación')]
	tipolicitacion = fields.Selection(select, string="Tipo de Licitación", default="1", required=True)
	numerolicitacion = fields.Char(string="Número de Licitación", required=True)
	convocatoria = fields.Char(string="Convocatoria",required=True)
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
	costobasesdependencia = fields.Float(string="Costo de Bases Dependencia", required=True)
	costocompranetbanco = fields.Float(string="Costo CompraNET/Banco", required=True)
	fechaestimadainicio = fields.Date(string="Fecha Estimada de Inicio", required=True)
	fechaestimadatermino = fields.Date(string="Fecha Estimada de Termino", required=True)
	plazodias = fields.Integer(string="Plazo de Días", required=True)
	capitalcontable = fields.Float(string="Capital Contable", required=True)
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

	@api.multi
	def participantes(self):
		return {
			'type': 'ir.actions.act_window',
			'name': 'Licitantes participantes',
			'res_model': 'proceso.participantes_contratistas',
			'view_mode': 'tree,form',
			'view_type': 'form',
			'target': 'self',
		}


class Participantes(models.Model):
	_name = "proceso.participantes_contratistas"

	contratista_participante = fields.Many2one('contratista.contratista', 'name')



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