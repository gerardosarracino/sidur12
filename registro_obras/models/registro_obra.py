from odoo import models, fields, api, exceptions
from datetime import datetime
from odoo.tools.safe_eval import safe_eval


class ejercicio(models.Model):
	_name = "registro.ejercicio"

	name = fields.Integer(string="Ejercicio", )
	ejercicio = fields.One2many("registro.obra", "ejercicio")


class unidadAdminSol(models.Model):
	_name = "registro.unidadadminsol"

	name = fields.Char(string="Descripción", )
	unidad = fields.One2many("registro.obra", "unidadadminsol")


class tipoProyecto(models.Model):
	_name = "registro.tipoproyecto"

	name = fields.Char(string="Tipo de proyecto", )
	tipoproyecto = fields.One2many("registro.obra", "tipoproyecto")


class tipoObraEtapa(models.Model):
	_name = "registro.tipoobraetapa"

	name = fields.Char(string="Tipo de proyecto", )
	tipoobraetapa = fields.One2many("registro.obra", "tipoobraetapa")


class tipoLocalidad(models.Model):
	_name = "registro.tipolocalidad"

	name = fields.Char(string="Tipo localidad", )
	tipolocalidad = fields.One2many("registro.obra", "tipolocalidad")


class unidadMedida(models.Model):
	_name = "registro.unidadm"

	name = fields.Char(string="Unidad medida", )
	unidadm = fields.One2many("registro.obra", "metaProyectoUnidad")
	unidadm1 = fields.One2many("registro.obra", "metaEjercicioUnidad")


class registro_obra(models.Model):
	_name = "registro.obra"
	_inherit = 'res.partner'

	shape_name = fields.Char(string='Shape Name')
	shape_area = fields.Float(string='Area')
	shape_radius = fields.Float(string='Radius')
	shape_description = fields.Text(string='Description')
	shape_type = fields.Selection([
		('circle', 'Circle'), ('polygon', 'Polygon'),
		('rectangle', 'Rectangle')], string='Type', default='polygon',
		required=True)
	shape_paths = fields.Text(string='Paths')

	name = fields.Char(string="Número de obra")
	ejercicio = fields.Many2one("registro.ejercicio", string="Ejercicio", required=True)
	grupoObra = fields.Boolean(string="Grupo de obra")
	origen = fields.Many2one('generales.origenes_obra', 'origen', required=True)
	monto = fields.Float(string="Monto", required=True)
	descripcion = fields.Text(string="Descripción", required=True)
	problematica = fields.Text(string="Problemática", required=True)
	unidadadminsol = fields.Many2one('registro.unidadadminsol', string="Unidad administrativa solicitante",
									 required=True)
	tipoObra = fields.Many2one('generales.tipo_obra', 'tipo_obra', required=True)
	tipoproyecto = fields.Many2one("registro.tipoproyecto", string="Tipo de proyecto", required=True)
	tipoobraetapa = fields.Many2one("registro.tipoobraetapa", string="Tipo de obra etapa", required=True)
	estado = fields.Many2one('generales.estado', 'estado')
	municipio = fields.Many2one('generales.municipios', 'municipio_delegacion', required=True)
	ubicacion = fields.Text(string="Ubicación")
	localidad = fields.Text(string="Localidad")
	cabeceraMunicipal = fields.Boolean(string="Cabecera municipal")
	tipolocalidad = fields.Many2one("registro.tipolocalidad", string="Tipo localidad", required=True)
	latitud = fields.Char(string="Latitud")
	longitud = fields.Char(string="Longitud")
	beneficiados = fields.Char(string="Beneficiados", required=True)
	metaFisicaProyecto = fields.Char(string="Meta física Proyecto", required=True)
	# metaProyectoUnidad = fields.Many2one("registro.unidadm" ,string="Meta Proyecto Unidad", )
	metaProyectoUnidad = fields.Char(string="Meta Proyecto Unidad", required=True)
	metaEjercicio = fields.Char(string="Meta ejercicio", required=True)
	# metaEjercicioUnidad = fields.Many2one("registro.unidadm", string="Meta ejercicio unidad", )
	metaEjercicioUnidad = fields.Char(string="Meta ejercicio unidad", required=True)
	justificacionTecnica = fields.Text(string="Justificación técnica", required=True)
	justificacionSocial = fields.Text(string="Justificación social", required=True)
	proyecto_ejecutivo = fields.Integer(compute='contar')
	seguimientoc = fields.Integer(compute='contar1')
	programada = fields.Integer(compute='contar2')
	# estate = fields.Selection([('planeada', 'Planeada'),('programada', 'Programada'),], default='planeada')
	estado_obra = fields.Char(compute="contar_programada")

	@api.multi
	def _compute_commercial_partner(self):
		return "hola"

	@api.multi
	def decode_shape_paths(self):
		self.ensure_one()
		return safe_eval(self.shape_paths)

	@api.one
	def contar_programada(self):
		count = self.env['registro.programarobra'].search_count([('name', '=', self.id),('estate2','!=','cancelado')])
		count2 = self.env['registro.programarobra'].search_count([('name', '=', self.id),('estate2','=','cancelado')])
		if count == 0 and count2 == 0:
			self.estado_obra = 'Planeada'
		elif count > 0 and count2==0:
			self.estado_obra = 'Programada'
		elif count > 0 and count2 > 0:
			self.estado_obra = 'Programada'
		elif count == 0 and count2 > 0:
			self.estado_obra = 'Planeada'

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
		count = self.env['registro.programarobra'].search_count([('name', '=', self.id),('estate2','!=','cancelado')])
		self.programada = count

#	@api.multi
#	def proyectoEjecutivo(self):
#		context = {
#		'default_name': self.id
#		}
#		return {
#		'type': 'ir.actions.act_window',
#		'name': 'Proyecto ejecutivo',
#		'res_model': 'registro.proyectoejecutivo',
#		'view_mode': 'tree,form',
#		'context': context,
#		'target': 'new',
#		}


class ProyectoEjecutivo(models.TransientModel):
	_name = 'registro.proyectoejecutivo'

	name1 = fields.Many2one('generales.apartados_proyectos', required=True)
	name = fields.Many2one('registro.obra', readonly=True)
	documento = fields.Binary(string="Documento", required=True)
	nombre = fields.Char(string="Nombre", required=True)
	observaciones = fields.Text(string="Observaciones", required=True)


class SeguimientoObra(models.TransientModel):
	_name = 'registro.seguimientoobra'

	name = fields.Many2one('registro.obra', readonly=True)
	seguimiento = fields.Html(string="Seguimiento", required=True)


class ProgramarObra(models.Model):
	_name = 'registro.programarobra'
	_rec_name = 'descripcion'

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
	estate2 = fields.Selection([('activo', 'Activo'),('cancelado', 'Cancelado'),], default='activo')
	tipo = fields.Char(related="name.tipoObra.tipo_obra")

	descripcion = fields.Text(related="name.descripcion")

	estado = fields.Char(related="name.estado.estado")
	municipio = fields.Char(related="name.municipio.municipio_delegacion")
	ubicacion = fields.Text(related="name.ubicacion")
	monto = fields.Float(related="name.monto")
	estruc_finan = fields.Integer(compute='contar3')

	# BUSCAR SI LA OBRA ESTA ADJUDICADA
	adjudicacion_cont = fields.Integer(compute="adjudicacion_contar")
	licitacion_cont = fields.Integer(compute="licitacion_contar")
	contrato_cont = fields.Integer(compute="contrato_contar")
	# INICA METODOS PARA CONTAR ADJUDICADA, LICITADA O CONTRATADA
	@api.one
	def adjudicacion_contar(self):
		count = self.env['partidas.adjudicacion'].search_count([('obra', '=', self.descripcion)])
		self.adjudicacion_cont = count

	@api.one
	def licitacion_contar(self):
		count = self.env['partidas.licitacion'].search_count([('obra', '=', self.descripcion)])
		self.licitacion_cont = count

	@api.one
	def contrato_contar(self):
		count = self.env['partidas.partidas'].search_count([('obra', '=', self.descripcion)])
		self.contrato_cont = count

	# TERMINA METODOS PARA CONTAR ADJUDICADA, LICITADA O CONTRATADA

	@api.multi
	def borrador_progressbar_respuesta(self):
		for rec in self:
			rec.write({
				'estate2': 'cancelado',
				})

	@api.constrains('name')
	def contar2(self):
		count = self.env['registro.programarobra'].search_count([('name', '=', self.name.id),('estate2','!=','cancelado')])
		if count>1:
			raise exceptions.ValidationError("La obra ya fue programada con anterioridad. Por favor verifique su información.")

	@api.one
	def contar3(self):
		count = self.env['registro.estructurafinanciera'].search_count([('name', '=', self.id)])
		self.estruc_finan = count


class EstructuraFinanciera(models.Model):
	_name = "registro.estructurafinanciera"

	name = fields.Many2one('registro.programarobra', readonly=True)
	descripcion = fields.Text(related="name.descripcion")
	monto = fields.Float(related="name.monto")
	iaoeFederal = fields.Float(string="Federal")
	iaoeEstatal = fields.Float(string="Estatal")
	iaoeMunicipal = fields.Float(string="Municipal")
	iaoeInstitucional = fields.Float(string="Institucional")
	iaoeOtros = fields.Float(string="Otros")
	sumaIaoe = fields.Float(string="Total", compute="_sumaiaoe", store=True)
	ideFederal = fields.Float(string="Federal")
	ideEstatal = fields.Float(string="Estatal")
	ideMunicipal = fields.Float(string="Municipal")
	ideInstitucional = fields.Float(string="Institucional")
	ideOtros = fields.Float(string="Otros")
	sumaIde = fields.Float(string="Total", compute="_sumaide", store=True)
	iarFederal = fields.Float(string="Federal")
	iarEstatal = fields.Float(string="Estatal")
	iarMunicipal = fields.Float(string="Municipal")
	iarInstitucional = fields.Float(string="Institucional")
	iarOtros = fields.Float(string="Otros")
	sumaIar = fields.Float(string="Total", compute="_sumaiar", store=True)
	Total = fields.Float(compute="_total", store=True)

	@api.depends('iaoeFederal','iaoeEstatal','iaoeMunicipal','iaoeInstitucional','iaoeOtros')
	def _sumaiaoe(self):
		for r in self:
			r.sumaIaoe = r.iaoeFederal + r.iaoeEstatal + r.iaoeMunicipal + r.iaoeInstitucional + r.iaoeOtros

	@api.depends('ideFederal','ideEstatal','ideMunicipal','ideInstitucional','ideOtros')
	def _sumaide(self):
		for r in self:
			r.sumaIde = r.ideFederal + r.ideEstatal + r.ideMunicipal + r.ideInstitucional + r.ideOtros

	@api.depends('iarFederal','iarEstatal','iarMunicipal','iarInstitucional','iarOtros')
	def _sumaiar(self):
		for r in self:
			r.sumaIar = r.iarFederal + r.iarEstatal + r.iarMunicipal + r.iarInstitucional + r.iarOtros

	@api.depends('sumaIaoe','sumaIde','sumaIar')
	def _total(self):
		for r in self:
			r.Total = r.sumaIaoe + r.sumaIde + r.sumaIar


class GoogleMapsDrawingShapeMixin(models.AbstractModel):
	_name = 'google_maps.drawing.shape.mixin'
	_description = 'Google Maps Shape Mixin'
	_rec_name = 'shape_name'

	shape_name = fields.Char(string='Name')
	shape_area = fields.Float(string='Area')
	shape_radius = fields.Float(string='Radius')
	shape_description = fields.Text(string='Description')
	shape_type = fields.Selection([
		('circle', 'Circle'), ('polygon', 'Polygon'),
		('rectangle', 'Rectangle')], string='Type', default='polygon',
		required=True)
	shape_paths = fields.Text(string='Paths')

	@api.multi
	def decode_shape_paths(self):
		self.ensure_one()
		return safe_eval(self.shape_paths)