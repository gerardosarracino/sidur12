from odoo import models, fields, api, exceptions

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import tools, _
from odoo.modules.module import get_module_resource

# CLASE AUXILIAR DE PARTIDAS LICITACION
class PartidasLicitacion(models.Model):
    _name = 'partidas.licitacion'

    obra = fields.Many2one('registro.programarobra', )
    programaInversion = fields.Many2one('generales.programas_inversion', )
    monto_partida = fields.Float(string="Monto", )
    iva_partida = fields.Float(string="Iva", compute="iva")
    total_partida = fields.Float(string="Total", compute="sumaPartidas")

    # METODO CALCULAR TOTAL PARTIDA
    @api.depends('monto_partida')
    def sumaPartidas(self):
        for rec in self:
            rec.update({
                'total_partida': (rec.monto_partida * 0.16) + rec.monto_partida
            })

    # CALCULAR EL IVA TOTAL
    @api.depends('monto_partida')
    def iva(self):
        for rec in self:
            rec.update({
                'iva_partida': (rec.monto_partida * 0.16)
            })


# CLASE AUXILIAR DE PARTIDAS ADJUDICACION
class PartidasAdjudicacion(models.Model):
    _name = 'partidas.adjudicacion'

    obra = fields.Many2one('registro.programarobra', )
    programaInversion = fields.Many2one('generales.programas_inversion')
    monto_partida = fields.Float(string="Monto", )
    iva_partida = fields.Float(string="Iva", compute="iva")
    total_partida = fields.Float(string="Total", compute="sumaPartidas")

    # METODO CALCULAR TOTAL PARTIDA
    @api.depends('monto_partida')
    def sumaPartidas(self):
        for rec in self:
            rec.update({
                'total_partida': (rec.monto_partida * 0.16) + rec.monto_partida
            })

    # CALCULAR EL IVA TOTAL
    @api.depends('monto_partida')
    def iva(self):
        for rec in self:
            rec.update({
                'iva_partida': (rec.monto_partida * 0.16)
            })


# CLASE DE LAS PARTIDAS Y CONCEPTOS CONTRATADOS
class Partidas(models.Model):
    _name = 'partidas.partidas'
    _rec_name = "numero_contrato"

    numero_contrato = fields.Many2one(comodel_name="proceso.elaboracion_contrato", string="Numero de Contrato", compute="nombrePartida" )
    # enlace estimacion
    estimacion_id = fields.Char(compute="nombre", store=True)
    obra = fields.Many2one('registro.programarobra', )

    # PROGRAMA DE INVERSION
    programaInversion = fields.Many2one('generales.programas_inversion',)
    monto_partida = fields.Float(string="Monto",)
    iva_partida = fields.Float(string="Iva",   compute="iva")
    total_partida = fields.Float(string="Total",   compute="sumaPartidas")

    # NOTA CAMBIAR DESPUES LOS VALORES DE IVA A PERSONALIZADOS NO FIJOS
    # METODOS DE SUMA DEL MANY2MANY 'programar_obra'

    # CONCEPTOS CONTRATADOS DE PARTIDAS
    conceptos_partidas = fields.Many2many('proceso.conceptos_part')

    name = fields.Many2one('proceso.elaboracion_contrato', readonly=True)
    total = fields.Float(string="Monto Total Contratado:", readonly=True, compute="totalContrato")
    total_contrato = fields.Float(string="Monto Total del Catálogo:", readonly=True, compute="SumaImporte")
    diferencia = fields.Float(string="Diferencia:", compute="Diferencia")

    # ESTIMACIONES ---------
    radio_estimacion = [(
        '1', "Estimacion"), ('2', "Escalatoria")]
    tipo_estimacion = fields.Selection(radio_estimacion, string="")
    # estimacions_id = fields.Char(compute="estimacionId", store=True)
    numero_estimacion = fields.Integer(string="Número de Estimación:", required=False, )
    fecha_inicio_estimacion = fields.Date(string="Del:", required=False, )
    fecha_termino_estimacion = fields.Date(string="Al:", required=False, )
    fecha_presentacion = fields.Date(string="Fecha de presentación:", required=False, )
    fecha_revision = fields.Date(string="Fecha revisión Residente:", required=False, )
    radio_aplica = [(
        '1', "Estimación Finiquito"), ('2', "Amortizar Total Anticipo	")]
    si_aplica = fields.Selection(radio_aplica, string="")
    notas = fields.Text(string="Notas:", required=False, )

    # DEDUCCIONES
    deducciones = fields.Many2many('generales.deducciones', string="Deducciones:")

    # CALCULADOS DE ESTIMACIONES
    estimado = fields.Float(string="Importe ejecutado estimación:", required=False, )
    amort_anticipo = fields.Float(string="Amortización de Anticipo 30%:", required=False, )
    estimacion_subtotal = fields.Float(string="Neto Estimación sin IVA:", required=False, )
    estimacion_iva = fields.Float(string="I.V.A. 16%", required=False, )
    estimacion_facturado = fields.Float(string="Neto Estimación con IVA:", required=False, )
    estimado_deducciones = fields.Float(string="Menos Suma Deducciones:", required=False, )
    ret_dev = fields.Float(string="Retención/Devolución:", required=False, )
    sancion = fields.Float(string="Sanción por Incump. de plazo:", required=False, )
    a_pagar = fields.Float(string="Importe liquido:", required=False, )

    # PENAS CONVENCIONALES
    menos_clau_retraso = fields.Float(string="Menos Clausula Retraso:", required=False, )
    sancion_incump_plazo = fields.Integer(string="Sanción por Incump. de plazo:", required=False, )

    # CONCEPTOS EJECUTADOS
    # conceptos_partidas = fields.Many2many('proceso.conceptos_part')

    # CONVENIOS MODIFICATORIOS
    convenios_modificatorios = fields.Many2many('proceso.convenios', string="Conv. Modificatorios")

    # RESIDENCIA
    residente_obra = fields.Many2one(
        comodel_name='res.users',
        string='Residente obra:',
        default=lambda self: self.env.user.id,)
    supervision_externa = fields.Many2one('proceso.elaboracion_contrato', string="Supervisión externa:")
    director_obras = fields.Char('Director de obras:')
    puesto_director_obras = fields.Text('Puesto director de obras:')

    # PROGRAMA
    fecha_inicio_programa = fields.Date('Fecha Inicio:', compute='fechaInicio')
    fecha_termino_programa = fields.Date('Fecha Término:', compute='fechaTermino')
    monto_programa_aux = fields.Float(compute='SumaProgramas')
    restante_programa = fields.Float(string="Restante:", compute='DiferenciaPrograma')
    programa_contrato = fields.Many2many('proceso.programa', string="Agregar Periodo:")

    # Supervicion de obra (JFernandez)
    ruta_critica = fields.Many2many('proceso.rc')
    total_ = fields.Integer(compute='suma_importe')

    # ANTICIPOS
    # anticipos = fields.Many2many('proceso.anticipo_contratos', string="Anticipos:")
    # new_field = fields.Float(string="")

    # CONTAR REGISTROS DE ESTIMACIONES
    contar_estimaciones = fields.Integer(compute='contarEstimaciones', string="PRUEBA")

    # ANTICIPOS
    fecha_anticipos = fields.Date(string="Fecha Anticipo")
    porcentaje_anticipo = fields.Float(string="Anticipo Inicio", default="0.30")
    total_anticipo_porcentaje = fields.Float(string="Total Anticipo", compute="anticipo_por")
    anticipo_material = fields.Float(string="Anticipo Material")
    importe = fields.Float(string="Importe Contratado")
    anticipo_a = fields.Integer(string="Anticipo", compute="anticipo_inicio")
    iva_anticipo = fields.Float(string="I.V.A", compute="anticipo_iva")
    total_anticipo = fields.Integer(string="Total Anticipo", compute="anticipo_total")
    numero_fianza = fields.Integer(string="# Fianza")
    afianzadora = fields.Char(string="Afianzadora")
    fecha_fianza = fields.Date(string="Fecha Fianza")

    # PRUEBA DE VISTA
    ejercicio = fields.Many2one("registro.ejercicio", string="Ejercicio", related="obra.name.ejercicio")
    municipio = fields.Many2one('generales.municipios', 'municipio_delegacion', related="obra.name.municipio")
    localidad = fields.Text(string="Localidad", readonly="True", related="obra.name.localidad")
    # fecha_anticipo = fields.Date(string="Fecha Anticipo", related="obra.name.ejercicio")
    fecha = fields.Date(string="Fecha", related="numero_contrato.fecha")
    fechainicio = fields.Date(string="Fecha de Inicio", related="numero_contrato.fechainicio")
    fechatermino = fields.Date(string="Fecha de Termino", related="numero_contrato.fechatermino")
    supervisionexterna1 = fields.Many2one('proceso.elaboracion_contrato', string="Supervisión externa:",
                                          related="numero_contrato.supervisionexterna1")

    # RELACION CONTRATISTA
    contratista = fields.Many2one('contratista.contratista', related="numero_contrato.contratista")

    nombre_partida = fields.Char(string="nombre partida", required=False, )
    # PENDIENTE
    nueva_partida = fields.Char(string="nombre partida", required=False, )

    @api.one
    @api.depends('porcentaje_anticipo')
    def anticipo_por(self):
        for rec in self:
            rec.update({
                'total_anticipo_porcentaje': rec.porcentaje_anticipo
            })

    @api.one
    @api.depends('total_partida', 'porcentaje_anticipo')
    def anticipo_inicio(self):
        for rec in self:
            rec.update({
                'anticipo_a': rec.total_partida * rec.total_anticipo_porcentaje
            })

    # VER CUESTION DEL IVA
    @api.one
    @api.depends('anticipo_a')
    def anticipo_iva(self):
        for rec in self:
            rec.update({
                'iva_anticipo': rec.anticipo_a * 0.16
            })

    @api.one
    @api.depends('anticipo_a', 'iva_anticipo')
    def anticipo_total(self):
        for rec in self:
            rec.update({
                'total_anticipo': rec.anticipo_a + rec.iva_anticipo
            })

    @api.one
    def nombrePartida(self):
        self.numero_contrato = self.env['proceso.elaboracion_contrato'].search([('contrato', '=', self.nombre_partida)]).id
        self.nueva_partida = self.nombre_partida

    # METODO PARA ABRIR ANTICIPOS CON BOTON
    @api.multi
    def anticipo(self):
        view = self.env.ref('proceso_contratacion.partidas_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'anticipo',
            'res_model': 'partidas.partidas',
            'view_mode': 'form',
            'target': 'new',
            'view_id': view.id,
            'res_id': self.id,
        }



    # METODO DE CONTAR REGISTROS DE FINIQUITOS PARA ABRIR VISTA EN MODO NEW O TREE VIEW
    @api.one
    def contarEstimaciones(self):
        count = self.env['control.estimaciones'].search_count([('obra', '=', self.id)])
        self.contar_estimaciones = count

    # METODO DE JCHAIRZ
    @api.onchange('ruta_critica')
    def suma_importe(self):
        suma = 0
        for i in self.ruta_critica:
            resultado = i.porcentaje_est
            suma += resultado
            self.total_ = suma
    # JCHAIREZ
    @api.onchange('total_')
    def validar_total_importe(self):
        if self.total_ > 100:
            raise ValidationError("Ups! el porcentaje no puede ser mayor a 100 %")

    @api.one
    def totalContrato(self):
        self.total = self.total_partida

    # METODO CALCULAR DIFERENCIA ENTRE PARTIDA Y CONCEPTOS
    @api.one
    def Diferencia(self):
        self.diferencia = self.total - self.total_contrato

    # METODO CALCULAR TOTAL PARTIDA
    @api.depends('monto_partida')
    def sumaPartidas(self):
        for rec in self:
            rec.update({
                'total_partida': (rec.monto_partida * 0.16) + rec.monto_partida
            })

    # CALCULAR EL IVA TOTAL
    @api.depends('monto_partida')
    def iva(self):
        for rec in self:
            rec.update({
                'iva_partida': (rec.monto_partida * 0.16)
            })

    # METODO PARA SUMAR LOS IMPORTES DE LOS CONCEPTOS
    @api.onchange('conceptos_partidas')
    def SumaImporte(self):
        suma = 0
        for i in self.conceptos_partidas:
            resultado = i.importe
            suma = suma + resultado
            self.total_contrato = suma

    # METODO PARA SUMAR LOS IMPORTES DE LOS PROGRAMAS ---
    @api.onchange('programa_contrato')
    def SumaProgramas(self):
        suma = 0
        for i in self.programa_contrato:
            resultado = i.monto
            suma = suma + resultado
            self.monto_programa_aux = suma

    # METODO PARA SACAR LA FECHA DEL M2M
    @api.one
    def fechaInicio(self):
        for i in self.programa_contrato:
            resultado = str(i.fecha_inicio)
            self.fecha_inicio_programa = str(resultado)

    # METODO PARA SACAR LA FECHA DEL M2M
    @api.one
    def fechaTermino(self):
        for i in self.programa_contrato:
            resultado = str(i.fecha_termino)
            self.fecha_termino_programa = str(resultado)

    # METODO CALCULAR DIFERENCIA ENTRE PROGRAMAS Y TOTAL DEL CONTRATO
    @api.one
    def DiferenciaPrograma(self):
        self.restante_programa = self.total_partida - self.monto_programa_aux

    # METODO DE ENLACE A ESTIMACIONES
    @api.one
    def nombre(self):
        self.estimacion_id = self.obra

    '''@api.multi
        def create_customer_invoice(self):
            """
            Method to open create customer invoice form
            """
            # Get the client id from transport form
            obra = self.obra

            # Initialize required parameters for opening the form view of invoice
            # Get the view ref. by paasing module & name of the required form
            view_ref = self.env['ir.model.data'].get_object_reference('proceso_contratacion', 'partidas_form')
            view_id = view_ref[1] if view_ref else False

            # Let's prepare a dictionary with all necessary info to open create invoice form with
            # customer/client pre-selected
            res = {
                'type': 'ir.actions.act_window',
                'name': _('prueba'),
                'res_model': 'partidas.partidas',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'new',
                'context': {'default_obra': obra}
            }

            return res'''

    '''@api.multi
    @api.onchange('new_field')  # if these fields are changed, call method
    def check_change_anticipo(self):
        adirecta_id = self.env['proceso.elaboracion_contrato'].browse(self.obra.id)
        self.update({
            'anticipos': [[5]]
        })
        for partidas in adirecta_id.anticipos:
            self.update({
                'anticipos': [[0, 0, {'obra': partidas.obra,
                                      'fecha_anticipo': partidas.fecha_anticipo,
                                      'porcentaje_anticipo': partidas.porcentaje_anticipo,
                                      'total_anticipo_porcentaje': partidas.total_anticipo_porcentaje,
                                      'anticipo_material': partidas.anticipo_material,
                                      'importe': partidas.importe,
                                      'anticipo': partidas.anticipo,
                                      'iva': partidas.iva,
                                      'total_anticipo': partidas.total_anticipo,
                                      'numero_fianza': partidas.numero_fianza,
                                      'afianzadora': partidas.total_anticipo,
                                      'fecha_fianza': partidas.numero_fianza,
                                      }]]
            })'''

    '''@api.multi
    @api.onchange('new_field')  # if these fields are changed, call method
    def prueba(self):
        adirecta_id = self.env['registro.obra'].browse(self.obra.id)
        self.update({
            'ejercicio': [[5]]
        })
        for ejercicio in adirecta_id.ejercicio:
            self.update({
                'ejercicio': [[0, 0, {'ejercicio': ejercicio.ejercicio
                                      }]]
            })'''


class ConveniosM(models.Model):
    _name = 'proceso.convenios'

    fecha_convenios = fields.Date("Fecha:")
    referencia_convenios = fields.Char("Referencia:")
    observaciones_convenios = fields.Char("Observaciones:")
    tipo_convenio = fields.Char("Tipo de Convenio:", default="Escalatorio", readonly="True")
    importe_convenios = fields.Float('Importe:')
    iva_convenios = fields.Float('I.V.A:')
    total_convenios = fields.Float('Total:')


class ProgramaContrato(models.Model):
    _name = 'proceso.programa'

    fecha_inicio = fields.Date('Fecha Inicio:')
    fecha_termino = fields.Date('Fecha Término:')
    monto = fields.Float('Monto:')


class ruta_critica(models.Model):
    _name = 'proceso.rc'

    obra = fields.Many2one('registro.programarobra')
    actividad = fields.Char(string="ACTIVIDADES PRINCIPALES")
    porcentaje_est = fields.Integer(string="P.R.C")
    name = fields.Char(string="FRENTE")
    sequence = fields.Integer()
    avance_fisico = fields.Integer(string="% Avance")

    xd = fields.Char(string="xd", required=False, )

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False)

    @api.model
    def create(self, values):
        if values.get('display_type', self.default_get(['display_type'])['display_type']):
            values.update(actividad=False, porcentaje_est=0)
        line = super(ruta_critica, self).create(values)
        return line

    @api.multi
    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(
                "You cannot change the type of a sale order line. Instead you should delete the current line and create a new line of the proper type.")
        result = super(ruta_critica, self).write(values)
        return result


class informe_avance(models.Model):
    _name = 'proceso.iavance'

    ruta_critica = fields.Many2many('proceso.rc')
    total_ = fields.Integer(compute='suma_importe')
    avance = fields.Integer(string="AVANCE %")
    fisico_ponderado = fields.Float(string="FISICO PONDERADO")
    obra = fields.Many2one('registro.programarobra')
    numero_contrato = fields.Integer(compute='numero_con')

    porcentaje_e = fields.Float()
    porcentaje_estimado = fields.Float(compute='porcest')
    comentarios_generales = fields.Text(string='Comentarios generales')
    situacion_contrato = fields.Selection([
        ('bien', "1- Bien"),
        ('satisfactorio', "2- Satisfactorio"),
        ('regular', "3- Regular"),
        ('deficiente', "4- Deficiente"),
        ('mal', "5- Mal")], default='bien', string="Situación del contrato")

    com_avance_obra = fields.Text()

    @api.one
    def nombre(self):
        self.contrato_id = self.contrato

    @api.onchange('ruta_critica')
    def suma_importe(self):
        suma = 0
        for i in self.ruta_critica:
            resultado = i.porcentaje_est
            suma += resultado
            self.total_ = suma

    @api.one
    def numero_con(self):
        c = self.env['partidas.partidas'].search([])
        a = self.env['proceso.adjudicacion_directa'].browse(1).numero_contrato.contrato

        self.numero_contrato = a

    @api.onchange('obra')
    def check_change_licitacion(self):
        adirecta_id = self.env['proceso.rc'].search([('obra', '=', self.obra.id)])
        self.update({
            'ruta_critica': [[5]]
        })

        for rt in adirecta_id:
            self.update({
                'ruta_critica': [
                    [0, 0, {'name': rt.name, 'obra': rt.obra, 'actividad': rt.actividad,
                            'porcentaje_est': rt.porcentaje_est, }]]
            })

    @api.onchange('ruta_critica')
    def porcest(self):
        r_porcentaje_est = 0
        r_avance_fisico = 0
        for i in self.ruta_critica:
            porcentaje_est = i.porcentaje_est
            r_porcentaje_est += porcentaje_est

            avance_fisico = i.avance_fisico
            r_avance_fisico += avance_fisico

            resultado = (r_porcentaje_est * r_avance_fisico) / 100

            self.porcentaje_estimado = resultado