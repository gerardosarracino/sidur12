from odoo import models, fields, api, exceptions

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


# CLASE AUXILIAR DE PARTIDAS LICITACION
class PartidasLicitacion(models.Model):
    _name = 'partidas.licitacion'

    obra = fields.Many2one('registro.programarobra', required=True)
    programaInversion = fields.Many2one('generales.programas_inversion')
    monto_partida = fields.Float(string="Monto", required=True)
    iva_partida = fields.Float(string="Iva", compute="iva")
    total_partida = fields.Float(string="Total", compute="sumaPartidas")

    b_iva = fields.Float(string="IVA DESDE CONFIGURACION", compute="BuscarIva")

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


# CLASE AUXILIAR DE PARTIDAS ADJUDICACION
class PartidasAdjudicacion(models.Model):
    _name = 'partidas.adjudicacion'
    # _inherit = 'res.config.settings'

    obra = fields.Many2one('registro.programarobra', required=True)
    programaInversion = fields.Many2one('generales.programas_inversion')
    monto_partida = fields.Float(string="Monto", required=True)
    iva_partida = fields.Float(string="Iva", compute="iva")
    total_partida = fields.Float(string="Total", compute="sumaPartidas")

    b_iva = fields.Float(string="IVA DESDE CONFIGURACION", compute="BuscarIva")

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
    monto_partida = fields.Float(string="Monto", )
    iva_partida = fields.Float(string="Iva", compute="iva", store=True)
    total_partida = fields.Float(string="Total", compute="SumaContrato")

    # SUMA DE LAS PARTIDAS
    total_contrato = fields.Float(related="numero_contrato.impcontra")

    # NOTA CAMBIAR DESPUES LOS VALORES DE IVA A PERSONALIZADOS NO FIJOS

    # CONCEPTOS CONTRATADOS DE PARTIDAS
    conceptos_partidas = fields.Many2many('proceso.conceptos_part', required=True)
    conceptos_modificados = fields.Many2many('proceso.conceptos_modificados', required=True)
    justificacion = fields.Text('Justificación de Modificación')
    select_tipo = [('1', 'Monto'), ('2', 'Plazo'), ('3', 'Ambos')]
    tipo = fields.Selection(select_tipo, string="Tipo:")

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
    total_anticipo = fields.Float(string="Total Anticipo", compute="anticipo_total")
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
        default=lambda self: self.env.user.id, )
    supervision_externa = fields.Many2one('proceso.elaboracion_contrato', string="Supervisión externa:")
    director_obras = fields.Char('Director de obras:')
    puesto_director_obras = fields.Text('Puesto director de obras:')

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
    localidad = fields.Char(string="Localidad", readonly="True", related="obra.name.city")
    # localidad = fields.Text(string="Localidad", readonly="True", related="obra.name.localidad")
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
    verif_programa = fields.Boolean(string="", compute="programa_verif")

    b_iva = fields.Float(string="IVA DESDE CONFIGURACION", compute="BuscarIva")

    @api.multi
    def CategoriasForm(self):
        view = self.env.ref('proceso_contratacion.categoria_seccion_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Categorias',
            'res_model': 'catalogo.categoria',
            'view_mode': 'form',
            'target': 'new',
            'view_id': view.id,
        }

    @api.multi
    def write(self, values):
        if self.fecha_anticipos and self.fecha_fianza and self.afianzadora and self.numero_fianza and \
                self.anticipo_material:
            return super(Partidas, self).write(values)
        elif self.ruta_critica is not False:
            return super(Partidas, self).write(values)
        elif self.conceptos_partidas:
            version = self.env['proceso.conceptos_modificados']
            id_partida = self.id
            datos = {'justificacion': values['justificacion'], 'obra': id_partida, 'tipo': values['tipo']}
            nueva_version = version.create(datos)
            values['tipo'] = ""
            values['justificacion'] = ""
            return super(Partidas, self).write(values)
        else:
            return super(Partidas, self).write(values)

    # METODO PARA INGRESAR A RECURSOS BOTON
    @api.multi
    def programas(self):
        view = self.env.ref('ejecucion_obra.vista_form_programa')
        count = self.env['programa.programa_obra'].search_count([('obra.id', '=', self.id)])
        search = self.env['programa.programa_obra'].search([('obra.id', '=', self.id)])
        if count == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Programa',
                'res_model': 'programa.programa_obra',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
                'res_id': search.id,
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Programa',
                'res_model': 'programa.programa_obra',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
            }

    @api.one
    def FechaAnticipo(self):
        search = self.env['anticipo.anticipo'].search([('obra.id', '=', self.id)])
        self.fecha_anticipos = search.fecha_anticipos

    @api.one
    def PorcentajeAnticipo(self):
        search = self.env['anticipo.anticipo'].search([('obra.id', '=', self.id)])
        self.porcentaje_anticipo = search.porcentaje_anticipo

    @api.one
    def TotalAnticipo(self):
        search = self.env['anticipo.anticipo'].search([('obra.id', '=', self.id)])
        self.total_anticipo = search.total_anticipo

    # METODO PARA ABRIR ANTICIPOS CON BOTON
    @api.multi
    def anticipoBoton(self):
        view = self.env.ref('proceso_contratacion.partidas_form')
        return {
            'type': 'ir.actions.act_window',
            'name': 'anticipos',
            'res_model': 'partidas.partidas',
            'view_mode': 'form',
            'target': 'new',
            'view_id': view.id,
            'res_id': self.id,
        }

    # METODO BUSCAR IVA EN CONFIGURACION
    @api.one
    def BuscarIva(self):
        iva = self.env['ir.config_parameter'].sudo().get_param('generales.iva')
        self.b_iva = iva

    # METODO PARA VERIFICAR SI HAY PROGRAMAS
    @api.one
    def programa_verif(self):
        busqueda = self.env['programa.programa_obra'].search([('obra.id', '=', self.id)])
        if busqueda.fecha_inicio_programa:
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
        self.numero_contrato = self.env['proceso.elaboracion_contrato'].search(
            [('contrato', '=', self.nombre_partida)]).id
        self.nueva_partida = self.nombre_partida

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
    @api.one
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

    # METODO DE ENLACE A ESTIMACIONES
    @api.one
    def nombre(self):
        self.estimacion_id = self.obra


class ConveniosM(models.Model):
    _name = 'proceso.convenios'

    fecha_convenios = fields.Date("Fecha:")
    referencia_convenios = fields.Char("Referencia:")
    observaciones_convenios = fields.Char("Observaciones:")
    tipo_convenio = fields.Char("Tipo de Convenio:", default="Escalatorio", readonly="True")
    importe_convenios = fields.Float('Importe:')
    iva_convenios = fields.Float('I.V.A:')
    total_convenios = fields.Float('Total:')


# CONTENIDO DE LA TABLA DE PROGRAMA DE OBRA
class ProgramaContrato(models.Model):
    _name = 'proceso.programa'

    fecha_inicio = fields.Date('Fecha Inicio:', default=fields.Date.today(), required=True)
    fecha_termino = fields.Date('Fecha Término:', required=True)
    monto = fields.Float('Monto:', required=True)

    # METODO para verificar fechas de programa
    @api.multi
    @api.onchange('fecha_termino')
    def validar_fecha_programa(self):
        if str(self.fecha_termino) < str(self.fecha_inicio):
            raise exceptions.Warning('No se puede seleccionar una Fecha anterior a la fecha de inicio, '
                                     'por favor seleccione una fecha posterior')
        else:
            return False


