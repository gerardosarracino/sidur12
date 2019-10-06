from odoo import models, fields, api, exceptions


from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo import tools, _
from odoo.modules.module import get_module_resource


# CLASE AUXILIAR DE PARTIDAS LICITACION
class PartidasLicitacion(models.Model):
    _name = 'partidas.licitacion'

    obra = fields.Many2one('registro.programarobra', required=True)
    programaInversion = fields.Many2one('generales.programas_inversion', required=True)
    monto_partida = fields.Float(string="Monto", required=True)
    iva_partida = fields.Float(string="Iva", compute="iva", required=True)
    total_partida = fields.Float(string="Total", compute="sumaPartidas", required=True)

    b_iva = fields.Float(string="IVA DESDE CONFIGURACION")

    # METODO BUSCAR IVA EN CONFIGURACION
    @api.multi
    @api.onchange('monto_partida')
    def BuscarIva(self):
        iva = self.env['ir.config_parameter'].sudo().get_param('generales.iva')
        self.b_iva = iva

    # METODO CALCULAR TOTAL PARTIDA
    @api.depends('monto_partida')
    def sumaPartidas(self):
        for rec in self:
            rec.update({
                'total_partida': (rec.monto_partida * self.b_iva) + rec.monto_partida
            })

    # CALCULAR EL IVA TOTAL
    @api.depends('monto_partida')
    def iva(self):
        for rec in self:
            rec.update({
                'iva_partida': (rec.monto_partida * self.b_iva)
            })


# CLASE AUXILIAR DE PARTIDAS ADJUDICACION
class PartidasAdjudicacion(models.Model):
    _name = 'partidas.adjudicacion'
    _inherit = 'res.config.settings'

    obra = fields.Many2one('registro.programarobra', required=True)
    programaInversion = fields.Many2one('generales.programas_inversion', related="")
    monto_partida = fields.Float(string="Monto", required=True)
    iva_partida = fields.Float(string="Iva", compute="iva", required=True, store=True)
    total_partida = fields.Float(string="Total", compute="sumaPartidas", required=True)

    b_iva = fields.Float(string="IVA DESDE CONFIGURACION", compute="BuscarIva" )

    # METODO BUSCAR IVA EN CONFIGURACION
    @api.one
    @api.depends('monto_partida')
    def BuscarIva(self):
        iva = self.env['ir.config_parameter'].sudo().get_param('generales.iva')
        self.b_iva = iva

    # METODO CALCULAR TOTAL PARTIDA
    @api.one
    @api.depends('monto_partida')
    def sumaPartidas(self):
        for rec in self:
            rec.update({
                'total_partida': (rec.monto_partida * self.b_iva) + rec.monto_partida
            })

    # CALCULAR EL IVA TOTAL
    @api.one
    @api.depends('monto_partida')
    def iva(self):
        for rec in self:
            rec.update({
                'iva_partida': (rec.monto_partida * self.b_iva)
            })


# CLASE DE LAS PARTIDAS Y CONCEPTOS CONTRATADOS
class Partidas(models.Model):
    _name = 'partidas.partidas'
    _rec_name = "numero_contrato"
    # CONTRATO AL QUE PERTENECE LA PARTIDA
    numero_contrato = fields.Many2one(comodel_name="proceso.elaboracion_contrato", string="Numero de Contrato",
                                      compute="nombrePartida")

    # ESTIMACION ENLACE
    estimacion_id = fields.Char(compute="nombre", store=True)

    # OBRA A LA QUE PERTENECE LA PARTIDA
    obra = fields.Many2one('registro.programarobra')
    # EL OBJETO ES LA DESCRIPCION DE LA OBRA EN EL CONTRATO
    objeto = fields.Text(string="Objeto", related="numero_contrato.name")

    # PROGRAMA DE INVERSION
    programaInversion = fields.Many2one('generales.programas_inversion', string="Programa de Inversión")
    monto_partida = fields.Float(string="Monto",)
    iva_partida = fields.Float(string="Iva", compute="iva")
    total_partida = fields.Float(string="Total", compute="SumaContrato")

    # SUMA DE LAS PARTIDAS
    total_contrato = fields.Float(related="numero_contrato.impcontra")

    # NOTA CAMBIAR DESPUES LOS VALORES DE IVA A PERSONALIZADOS NO FIJOS

    # CONCEPTOS CONTRATADOS DE PARTIDAS
    conceptos_partidas = fields.Many2many('proceso.conceptos_part', required=True)

    name = fields.Many2one('proceso.elaboracion_contrato', readonly=True)
    total = fields.Float(string="Monto Total Contratado:", readonly=True, compute="totalContrato", required=True)
    total_catalogo = fields.Float(string="Monto Total del Catálogo:", compute="SumaImporte", required=True)
    diferencia = fields.Float(string="Diferencia:", compute="Diferencia", required=True)

    # ANTICIPOS
    fecha_anticipos = fields.Date(string="Fecha Anticipo", )
    porcentaje_anticipo = fields.Float(string="Anticipo Inicio", default="0.30", )
    total_anticipo_porcentaje = fields.Float(string="Total Anticipo", compute="anticipo_por")
    anticipo_material = fields.Float(string="Anticipo Material", )
    importe = fields.Float(string="Importe Contratado")
    anticipo_a = fields.Integer(string="Anticipo", compute="anticipo_inicio")
    iva_anticipo = fields.Float(string="I.V.A", compute="anticipo_iva")
    total_anticipo = fields.Integer(string="Total Anticipo", compute="anticipo_total")
    numero_fianza = fields.Integer(string="# Fianza", )
    afianzadora = fields.Char(string="Afianzadora", )
    fecha_fianza = fields.Date(string="Fecha Fianza", )
    anticipada = fields.Boolean(string="Anticipada", compute="anticipada_Sel")

    # ESTIMACIONES
    radio_estimacion = [('1', "Estimacion"), ('2', "Escalatoria")]
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

    # PROGRAMA DE OBRA JCHAIREZ AQUI
    fecha_inicio_programa = fields.Date('Fecha Inicio:', compute='fechaInicio')
    fecha_termino_programa = fields.Date('Fecha Término:', compute='fechaTermino')
    monto_programa_aux = fields.Float(compute='SumaProgramas')
    restante_programa = fields.Float(string="Restante:", compute='DiferenciaPrograma')
    programa_contrato = fields.Many2many('proceso.programa', string="Agregar Periodo:")

    # Supervicion de obra (JFernandez)
    ruta_critica = fields.Many2many('proceso.rc')
    total_ = fields.Integer(compute='suma_importe')
    # Contador de convenios por obra
    count_convenios_modif = fields.Integer(compute="contar_covenios")

    # CONTAR REGISTROS DE ESTIMACIONES
    contar_estimaciones = fields.Integer(compute='ContarEstimaciones', string="PRUEBA")

    # VISTA DE INFORMACION DE LA PARTIDA
    ejercicio = fields.Many2one("registro.ejercicio", string="Ejercicio", related="obra.name.ejercicio")
    municipio = fields.Many2one('generales.municipios', 'Municipio', related="obra.name.municipio")
    localidad = fields.Text(string="Localidad", readonly="True", related="obra.name.localidad")
    fecha = fields.Date(string="Fecha", related="numero_contrato.fecha")
    fechainicio = fields.Date(string="Fecha de Inicio", related="numero_contrato.fechainicio")
    fechatermino = fields.Date(string="Fecha de Termino", related="numero_contrato.fechatermino")
    supervisionexterna1 = fields.Many2one('proceso.elaboracion_contrato', string="Supervisión externa:",
                                          related="numero_contrato.supervisionexterna1")

    # RELACION CONTRATISTA
    contratista = fields.Many2one('contratista.contratista', related="numero_contrato.contratista")

    # NOMBRE DE LA PARTIDA = AL DEL CONTRATO
    nombre_partida = fields.Char(string="nombre partida", required=False, )
    # PENDIENTE
    nueva_partida = fields.Char(string="nombre partida", required=False, )

    # A.FIS A.FIN
    a_fis = fields.Float(string="A.FIS", default=0.0, required=False, )
    a_fin = fields.Float(string="A.FIN", default=0.0, required=False, )

    # INICIO FINIQUITO #
    fecha1 = fields.Date(string="Fecha de aviso de terminación de los trabajos")
    fecha2 = fields.Datetime(string="Fecha y hora verificación de la terminación de los trabajos")
    numero = fields.Char(string="Número bitácora del contrato")
    nota1 = fields.Text(string="Nota de bitácora aviso terminación")
    fecha3 = fields.Date(string="Fecha nota bitácora")
    fecha4 = fields.Date(string="Fecha de aviso de terminación de trabajos")
    fecha5 = fields.Date(string="Fecha de inicio Real del contrato")
    fecha6 = fields.Date(string="Fecha de termino real del contrato")
    fecha7 = fields.Datetime(string="Fecha y hora programada del acta de recepción de los trabajos")
    fecha8 = fields.Datetime(string="Fecha y hora entrega de la obra")
    fecha9 = fields.Datetime(string="Fecha y hora finiquito")
    fecha10 = fields.Datetime(string="Fecha y hora acta cierre administrativo")
    fecha11 = fields.Datetime(string="Fecha y hora acta de extinción de derechos")
    description = fields.Text(string="Descripción de los trabajos")
    creditosContra = fields.Char(string="Créditos en contra del contratista al finalizar la obra")
    # FIN FINIQUITO #

    # ID PARTIDA
    p_id = fields.Integer('ID DE LA PARTIDA')

    # RESTRICCION DEL PROGRAMA, SI NO HAY PROGRAMA NO PERMITE REGISTRAR UNA ESTIMACION
    verif_programa = fields.Boolean(string="", compute="programa_verif" )

    b_iva = fields.Float(string="IVA DESDE CONFIGURACION", compute="BuscarIva")

    # METODO BUSCAR IVA EN CONFIGURACION
    @api.one
    def BuscarIva(self):
        iva = self.env['ir.config_parameter'].sudo().get_param('generales.iva')
        self.b_iva = iva

    # METODO PARA VERIFICAR SI HAY PROGRAMAS
    @api.one
    def programa_verif(self):
        if self.fecha_inicio_programa:
            print("SI HAY PROGRAMA")
            self.verif_programa = True
        else:
            print("NO HAY PROGRAMA")
            self.verif_programa = False

    # METODO PARA VERIFICAR SI YA SE ANTICIPO UNA PARTIDA
    @api.one
    def anticipada_Sel(self):
        if self.fecha_anticipos and self.numero_fianza and self.afianzadora and self.fecha_fianza:
            self.anticipada = True
        else:
            self.anticipada = False

    # METODO PARA VERIFICAR SI HAY ANTICIPO
    @api.multi
    def VerifAnti(self, vals):
        if self.fecha_anticipos and self.fecha_fianza and self.afianzadora and self.numero_fianza and self.anticipo_material is not False:
            self.anticipada = True
        else:
            self.anticipada = False

    # METODO PARA CALCULAR EL PORCENTAJE DEL ANTICIPO
    @api.one
    @api.depends('porcentaje_anticipo')
    def anticipo_por(self):
        for rec in self:
            rec.update({
                'total_anticipo_porcentaje': rec.porcentaje_anticipo
            })

    # METODO PARA CALCULAR EL ANTICIPO DE INICIO
    @api.one
    @api.depends('total_partida', 'porcentaje_anticipo')
    def anticipo_inicio(self):
        for rec in self:
            rec.update({
                'anticipo_a': rec.total_partida * rec.total_anticipo_porcentaje
            })

    # MEOTODO PARA CALCULAR IVA DE ANTICIPO ---VER CUESTION DEL IVA
    @api.one
    @api.depends('anticipo_a')
    def anticipo_iva(self):
        for rec in self:
            rec.update({
                'iva_anticipo': rec.anticipo_a * self.b_iva
            })

    # METODO PARA CALCULAR EL TOTAL DEL ANTICIPO
    @api.one
    @api.depends('anticipo_a', 'iva_anticipo')
    def anticipo_total(self):
        for rec in self:
            rec.update({
                'total_anticipo': rec.anticipo_a + rec.iva_anticipo
            })

    # METODO PARA INSERTAR EL NUMERO DEL CONTRATO DENTRO DE LA PARTIDA PARA HACER CONEXION
    @api.one
    def nombrePartida(self):
        self.numero_contrato = self.env['proceso.elaboracion_contrato'].search([('contrato', '=', self.nombre_partida)]).id
        self.nueva_partida = self.nombre_partida

    # METODO PARA ABRIR ANTICIPOS CON BOTON
    @api.one
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
    def ContarEstimaciones(self):
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

    # Jesus Fernandez metodo para abrir ruta critica
    @api.multi
    def ruta_critica_over(self):
        view = self.env.ref('ejecucion_obra.proceso_rutac_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ruta critica',
            'res_model': 'partidas.partidas',
            'view_mode': 'form',
            'target': 'new',
            'view_id': view.id,
            'res_id': self.id,
        }

    # Jesus Fernandez metodo para abrir programa de obra
    @api.multi
    def abrir_obra(self):
        view = self.env.ref('ejecucion_obra.vista_form_programa')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Programa',
            'res_model': 'partidas.partidas',
            'view_mode': 'form',
            'target': 'new',
            'view_id': view.id,
            'res_id': self.id,
        }

    # JFernandez metodo para contar el numero de convenios que tiene cada obra
    @api.one
    def contar_covenios(self):
        count = self.env['proceso.convenios_modificado'].search_count([('referencia', '=', self.id)])
        self.count_convenios_modif = count

    # METODO PARA ASIGNAR EL TOTAL DEL CONTRATO
    @api.one
    def totalContrato(self):
        self.total = self.total_partida

    # METODO CALCULAR DIFERENCIA ENTRE PARTIDA Y CONCEPTOS
    @api.depends('total_partida', 'total_catalogo')
    def Diferencia(self):
        for rec in self:
            rec.update({
                'diferencia': self.total_partida - self.total_catalogo
            })

    # METODO CALCULAR TOTAL PARTIDA UNICA
    @api.one
    @api.depends('monto_partida')
    def SumaContrato(self):
        for rec in self:
            rec.update({
                'total_partida': (rec.monto_partida * self.b_iva) + rec.monto_partida
            })

    # CALCULAR EL IVA TOTAL
    @api.depends('monto_partida')
    def iva(self):
        for rec in self:
            rec.update({
                'iva_partida': (rec.monto_partida * self.b_iva)
            })

    # METODO PARA SUMAR LOS IMPORTES DE LOS CONCEPTOS
    @api.onchange('conceptos_partidas')
    def SumaImporte(self):
        suma = 0
        for i in self.conceptos_partidas:
            resultado = i.importe
            suma = suma + resultado
            self.total_catalogo = suma

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
    @api.depends('programa_contrato')
    def fechaInicio(self):
        for i in self.programa_contrato:
            resultado = str(i.fecha_inicio)
            print(resultado)
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

    # METODO para verificar fechas de programa
    @api.onchange('fecha_termino')
    @api.depends('fecha_termino', 'fecha_inicio')
    def validar_fecha_programa(self):
        if str(self.fecha_termino) < str(self.fecha_inicio):
            raise exceptions.Warning('No se puede seleccionar una Fecha anterior a la fecha de inicio, '
                                     'por favor seleccione una fecha posterior')
        else:
            return False

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


class ruta_critica_avance(models.Model):
    _name = 'proceso.rc_a'

    numero_contrato = fields.Many2one('partidas.partidas')
    actividad = fields.Char(string="ACTIVIDADES PRINCIPALES")
    porcentaje_est = fields.Float(string="P.R.C")
    name = fields.Char(string="FRENTE")
    sequence = fields.Integer()
    avance_fisico = fields.Integer(string="% AVANCE")
    obra = fields.Many2one('registro.programarobra')
    r = fields.Many2one('proceso.iavance')
    avance_fisico_ponderado = fields.Float(string="% FISICO PONDERADO", compute='avance_fisico_pon')

    @api.depends('avance_fisico')
    def avance_fisico_pon(self):
        for rec in self:
            rec.update({
                'avance_fisico_ponderado': (rec.porcentaje_est * rec.avance_fisico) / 100
            })

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False)


    @api.model
    def create(self, values):
        if values.get('display_type', self.default_get(['display_type'])['display_type']):
            values.update(actividad=False, porcentaje_est=0)
        line = super(ruta_critica_avance, self).create(values)
        return line

    @api.multi
    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(
                "You cannot change the type of a sale order line. Instead you should delete the current line and create a new line of the proper type.")
        result = super(ruta_critica_avance, self).write(values)
        return result


class informe_avance(models.Model):
    _name = 'proceso.iavance'

    ruta_critica = fields.Many2many('proceso.rc_a')
    total_ = fields.Integer(compute='suma_importe')
    avance = fields.Integer(string="AVANCE %")
    fisico_ponderado = fields.Float(string="FISICO PONDERADO")
    obra = fields.Many2one('registro.programarobra')
    numero_contrato = fields.Many2one('partidas.partidas')

    porcentaje_e = fields.Float()
    porcentaje_estimado = fields.Float(compute='porcest', store=True)
    fecha_actual = fields.Date(string='Fecha', default=fields.Date.today(), required=True)
    comentarios_generales = fields.Text(string='Comentarios generales')
    situacion_contrato = fields.Selection([
        ('bien', "1- Bien"),
        ('satisfactorio', "2- Satisfactorio"),
        ('regular', "3- Regular"),
        ('deficiente', "4- Deficiente"),
        ('mal', "5- Mal")], default='bien',string="Situación del contrato")

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

    @api.multi
    @api.onchange('numero_contrato')
    def informe_de_avance_field(self):
        adirecta_id = self.env['partidas.partidas'].search([('id', '=', self.numero_contrato.id)])


        self.update({
            'ruta_critica': [[5]]
        })

        for rt in adirecta_id.ruta_critica:
            self.update({
                'ruta_critica': [[0, 0, {'name': rt.name, 'secuence': rt.sequence,
                                         'display_type': rt.display_type, 'obra': rt.obra,
                                         'actividad': rt.actividad, 'porcentaje_est': rt.porcentaje_est}]]
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