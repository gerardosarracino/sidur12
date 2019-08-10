# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime


class ejercicio(models.Model):
	_name = "registro.ejercicio"

	name = fields.Integer(string="Ejercicio", required=True)
	#ejercicio = fields.One2many("registro.obra", "ejercicio")


class unidadAdminSol(models.Model):
	_name = "registro.unidadadminsol"

	name = fields.Char(string="Descripción", required=True)
	unidad = fields.One2many("registro.obra", "unidadadminsol")


class tipoProyecto(models.Model):
	_name = "registro.tipoproyecto"

	name = fields.Char(string="Tipo de proyecto", required=True)
	tipoproyecto = fields.One2many("registro.obra", "tipoproyecto")


class tipoObraEtapa(models.Model):
	_name = "registro.tipoobraetapa"

	name = fields.Char(string="Tipo de proyecto", required=True)
	tipoobraetapa = fields.One2many("registro.obra", "tipoobraetapa")


class tipoLocalidad(models.Model):
	_name = "registro.tipolocalidad"

	name = fields.Char(string="Tipo localidad", required=True)
	tipolocalidad = fields.One2many("registro.obra", "tipolocalidad")


class unidadMedida(models.Model):
	_name = "registro.unidadm"

	name = fields.Char(string="Unidad medida", required=True)
	unidadm = fields.One2many("registro.obra", "metaProyectoUnidad")
	unidadm1 = fields.One2many("registro.obra", "metaEjercicioUnidad")


class registro_obra(models.Model):
	_name = "registro.obra"

	name = fields.Char(string="Número de obra", required=True)
	ejercicio = fields.Many2one("registro.ejercicio", string="Ejercicio", required=True)
	grupoObra = fields.Boolean(string="Grupo de obra")
	origen = fields.Many2one('generales.origenes_obra', 'name', required=True)
	monto = fields.Float(string="Monto", required=True)
	descripcion = fields.Text(string="Descripción", required=True)
	problematica = fields.Text(string="Problemática", required=True)
	unidadadminsol = fields.Many2one('registro.unidadadminsol', string="Unidad administrativa solicitante", required=True)
	tipoObra = fields.Many2one('generales.tipo_obra', 'name', required=True)
	tipoproyecto = fields.Many2one("registro.tipoproyecto", string="Tipo de proyecto", required=True)
	tipoobraetapa = fields.Many2one("registro.tipoobraetapa", string="Tipo de obra etapa", required=True)
	estado = fields.Many2one('generales.estado', 'name', required=True)
	municipio = fields.Many2one('generales.municipios', 'municipio_delegacion', required=True)
	ubicacion = fields.Text(string="Ubicación", required=True)
	localidad = fields.Text(string="Localidad", required=True)
	cabeceraMunicipal = fields.Boolean(string="Cabecera municipal")
	tipolocalidad = fields.Many2one("registro.tipolocalidad", string="Tipo localidad", required=True)
	latitud = fields.Char(string="Latitud")
	longitud = fields.Char(string="Longitud")
	beneficiados = fields.Char(string="Beneficiados", required=True)
	metaFisicaProyecto = fields.Char(string="Meta física Proyecto", required=True)
	metaProyectoUnidad = fields.Many2one("registro.unidadm" ,string="Meta Proyecto Unidad", required=True)
	metaEjercicio = fields.Char(string="Meta ejercicio", required=True)
	metaEjercicioUnidad = fields.Many2one("registro.unidadm", string="Meta ejercicio unidad", required=True)
	justificacionTecnica = fields.Text(string="Justificación técnica", required=True)
	justificacionSocial = fields.Text(string="Justificación social", required=True)
	proyecto_ejecutivo = fields.Integer(compute='contar')
	seguimientoc = fields.Integer(compute='contar1')
	programada = fields.Integer(compute='contar2')
	
	@api.one
	def contar(self):
		count = self.env['registro.proyectoejecutivo'].search_count([('name', '=', self.id)])
		self.proyecto_ejecutivo = count

	@api.one
	def contar1(self):
		count = self.env['registro.seguimientoobra'].search_count([('name', '=', self.id)])
		self.seguimientoc = count

	@api.one
	def contar2(self):
		count = self.env['registro.programarobra'].search_count([('name', '=', self.id)])
		self.programada = count
	
	@api.one
	def nombre(self):
		self.name = self.name

	@api.multi
	def proyectoEjecutivo(self):
		context = {
		'default_name': self.id
		}
		return {
		'type': 'ir.actions.act_window',
		'name': 'Proyecto ejecutivo',
		'res_model': 'registro.proyectoejecutivo',
		'view_mode': 'tree,form',
		'context': context,
		'target': 'new',
		}


class ProyectoEjecutivo(models.Model):
	_name = 'registro.proyectoejecutivo'

	name1 = fields.Many2one('generales.apartados_proyectos', required=True)
	name = fields.Many2one('registro.obra', readonly=True)
	documento = fields.Binary(string="Documento", required=True)
	nombre = fields.Char(string="Nombre", required=True)
	observaciones = fields.Text(string="Observaciones", required=True)


class SeguimientoObra(models.Model):
	_name = 'registro.seguimientoobra'

	name = fields.Many2one('registro.obra', readonly=True)
	seguimiento = fields.Html(string="Seguimiento", required=True)


class ProgramarObra(models.Model):
	_name = 'registro.programarobra'
	
	name = fields.Many2one('registro.obra', readonly=True)
	programaInversion = fields.Many2one('generales.programas_inversion', required=True)
	categoriaProgramatica = fields.Many2one('generales.modalidades', required=True)
	fechaProbInicio = fields.Date(string="Fecha probable de inicio", required=True)
	fechaProbTermino = fields.Date(string="Fecha Probable de termino", required=True)
	descripTotalObra = fields.Text(string="Descripción de la totalidad de la obra")
	conceptoEjecutar = fields.Text(string="Conceptos a ejecutar")
	select = [('1', 'Contrato'), ('2', 'Administracion directa'), ('3', 'Mixta')]
	modalidadEjecucion = fields.Selection(select, string="Modalidad de la ejecución", default="1", required=True)
	avanceFisicoActual = fields.Float(string="Avance físico actual")
	avanceProgCierreEjerci = fields.Float(string="Avance programado al cierre del ejercicio")
	imagen1 = fields.Binary(string="Imagen uno")
	imagen2 = fields.Binary(string="Imagen dos")
	imagen3 = fields.Binary(string="Imagen tres")
	imagen4 = fields.Binary(string="Imagen cuatro")

	@api.constrains('name')
	def contar2(self):
		count = self.env['registro.programarobra'].search_count([('name', '=', self.name.id)])
		if count>1:
			raise exceptions.ValidationError("La obra ya fue programada con anterioridad. Por favor verifique su información.")

