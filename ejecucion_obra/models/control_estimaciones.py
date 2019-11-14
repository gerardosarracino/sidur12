from odoo import models, fields, api, exceptions
from datetime import date
from datetime import datetime


class Estimaciones(models.Model):
    _name = 'control.estimaciones'
    _rec_name = 'obra'

    ide_estimacion = fields.Char(string="ID", compute="estid")
    # VER SI UTILIZAR
    estimacion_id = fields.Char()

    obra = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)
    obra_id = fields.Char(compute="obra_enlace", store=True)

    # ver si utilizar
    p_id = fields.Integer("ID PARTIDA", related="obra.p_id")

    # AUXILIAR DE CONEXION HACIA CONTRATO
    numero_contrato = fields.Many2one(string="nc", related="obra.numero_contrato")

    # ESTIMACIONES
    radio_estimacion = [(
        '1', "Estimacion"), ('2', "Escalatoria")]
    tipo_estimacion = fields.Selection(radio_estimacion, string="")

    # estimacions_id = fields.Char(compute="estimacionId", store=True)
    numero_estimacion = fields.Char(string="Número de Estimación:")

    fecha_inicio_estimacion = fields.Date(string="Del:", required=True, )
    fecha_termino_estimacion = fields.Date(string="Al:", required=True, )
    fecha_presentacion = fields.Date(string="Fecha de presentación:", required=True, )
    fecha_revision = fields.Date(string="Fecha revisión Residente:", required=True, )

    radio_aplica = [(
        '1', "Estimación Finiquito"), ('2', "Amortizar Total Anticipo	")]
    si_aplica = fields.Selection(radio_aplica, string="")

    notas = fields.Text(string="Notas:", required=False, )

    # DEDUCCIONES
    deducciones = fields.Many2many('control.deducciones', string="Deducciones:", )

    # Calculados
    estimado = fields.Float(string="Importe ejecutado estimación:", required=False )

    amort_anticipo = fields.Float(string="Amortización de Anticipo:", compute="amortizacion_anticipo")
    amort_anticipo_partida = fields.Float(related="obra.numero_contrato.contrato_partida_adjudicacion.porcentaje_anticipo")

    estimacion_subtotal = fields.Float(string="Neto Estimación sin IVA:", compute="Estimacion_sinIva")
    estimacion_iva = fields.Float(string="I.V.A. 16%", compute="Estimacion_Iva")
    estimacion_facturado = fields.Float(string="Neto Estimación con IVA:", compute="Estimacion_conIva")
    estimado_deducciones = fields.Float(string="Menos Suma Deducciones:", required=False, )
    ret_dev = fields.Float(string="Retención/Devolución:", required=False, )
    sancion = fields.Float(string="Sanción por Incump. de plazo:", required=False, )
    a_pagar = fields.Float(string="Importe liquido:", required=False, )

    # PENAS CONVENCIONALES
    menos_clau_retraso = fields.Float(string="Menos Clausula Retraso:", required=False, )
    sancion_incump_plazo = fields.Integer(string="Sanción por Incump. de plazo:", required=False, )

    # CONCEPTOS EJECUTADOS
    conceptos_partidas = fields.Many2many('proceso.conceptos_part')
    total_conceptos = fields.Float(string="Total:",  required=False)

    # ID DE LA ESTIMACION
    estimacion_ids = fields.Char(string="ID")

    b_iva = fields.Float(string="IVA DESDE CONFIGURACION", compute="BuscarIva")

    idobra = fields.Char(string="Numero de Estimacion:")

    # DATOS DEL CONTRATO PARA REPORTE
    fecha_contrato = fields.Date(string="", related="obra.fecha", )
    monto_contrato = fields.Float(string="", related="obra.total_partida", )
    anticipo_contrato = fields.Float(string="", related="obra.total_anticipo", )
    fechainicio_contrato = fields.Date(string="", related="obra.fechainicio", )
    fechatermino_contrato = fields.Date(string="", related="obra.fechatermino", )
    municipio_contrato = fields.Many2one(string="", related="obra.municipio", )
    tipobra_contrato = fields.Many2one(string="", related="obra.obra.name.tipoObra", )
    contratista_contrato = fields.Many2one(string="", related="obra.contratista", )
    programa = fields.Many2one(string="", related="obra.programaInversion", )
    subdirector_contrato = fields.Char(string="", compute="BuscarDirector")
    # DATOS Y CAMPOS CALCULADOS PARA REPORTE DE RETENCION
    fecha_inicio_programa = fields.Date(compute="B_fi_programa")
    fecha_termino_programa = fields.Date(compute="B_ff_programa")
    dias_transcurridos = fields.Integer(compute="DiasTrans")
    # MONTO PROGRAMADO PARA ESTA ESTIMACION
    monto_programado_est = fields.Float(compute="MontoProgramadoESt")
    porcentaje_est = fields.Float(compute="MontoProgramadoESt")

    _url = fields.Char(compute="_calc_url", string="Vista de impresión")

    xd = fields.Float(compute="computeSeccion")

    @api.multi
    @api.onchange('fecha_termino_estimacion', 'fecha_inicio_estimacion')
    def VerifFechaEst(self):
        if str(self.fecha_termino_estimacion) < str(self.fecha_inicio_estimacion):
            raise exceptions.Warning('No se puede seleccionar una Fecha anterior a la actual, '
                                     'por favor seleccione una fecha actual o posterior')
        else:
            return False

    @api.multi
    @api.onchange('fecha_presentacion', 'fecha_revision')
    def VerifFechaEst2(self):
        if str(self.fecha_revision) < str(self.fecha_presentacion):
            raise exceptions.Warning('No se puede seleccionar una Fecha anterior a la actual, '
                                     'por favor seleccione una fecha actual o posterior')
        else:
            return False

    @api.multi
    def computeSeccion(self):
        for i in self.conceptos_partidas:
            # print(i.nivel.complete_name)
            # print(i.nivel.parent_id.name)
            if i.categoria.name is i.categoria.parent_id.name:
                self.xd = 1
            else:
                self.xd = 1
        self.xd = 1

    @api.one
    def _calc_url(self):
        original_url = "/registro_obras/registro_obras/?id="
        self._url = original_url + str(self.id)

    @api.multi
    def imprimir_accion(self):
        return {
            "type": "ir.actions.act_url",
            "url": self._url,
            "target": "new",
        }

    # NOTA VERIFICAR M_ESTIMADO, DIAS IGUALES NO RETORNA EL VALOR COMPLETO DEL MONTO
    @api.multi
    def MontoProgramadoESt(self):
        f_estimacion_inicio = self.fecha_inicio_estimacion
        f_estimacion_termino = self.fecha_termino_estimacion
        b_programa = self.env['programa.programa_obra'].search([('obra.id', '=', self.obra.id)])
        acum = 0
        for i in b_programa.programa_contratos:
            fechatermino = i.fecha_termino
            fechainicio = i.fecha_inicio
            if f_estimacion_termino > fechatermino:
                acum = acum + i.monto
            elif f_estimacion_termino.month == fechatermino.month:
                # DIAS
                date_format = "%Y-%m-%d"
                if f_estimacion_inicio == f_estimacion_termino:
                    ultimo_monto = i.monto
                    m_estimado = ultimo_monto + acum
                    self.monto_programado_est = m_estimado
                else:
                    f1 = datetime.strptime(str(f_estimacion_inicio), date_format)
                    f2 = datetime.strptime(str(fechainicio), date_format)
                    r = f1 - f2
                    dias = r.days
                    f3 = datetime.strptime(str(fechainicio), date_format)
                    f4 = datetime.strptime(str(fechatermino), date_format)
                    r2 = f4 - f3
                    total_dias_periodo = r2.days
                    ultimo_monto = i.monto
                    monto_final = (ultimo_monto / total_dias_periodo) * dias
                    m_estimado = monto_final + acum
                    por = ultimo_monto + acum
                    self.monto_programado_est = m_estimado
                    self.porcentaje_est = (m_estimado / por) * 100
            else:
                print('xd')
        # self.monto_programado_est = m_estimado

    @api.one
    def DiasTrans(self):
        fe1 = self.fecha_inicio_programa
        fe2 = self.fecha_termino_programa
        date_format = "%Y-%m-%d"
        f1 = datetime.strptime(str(fe1), date_format)
        f2 = datetime.strptime(str(fe2), date_format)
        r = f2 - f1
        self.dias_transcurridos = r.days

    @api.one
    def B_fi_programa(self):
        b_fecha = self.env['programa.programa_obra'].search([('obra.id', '=', self.obra.id)])
        self.fecha_inicio_programa = str(b_fecha.fecha_inicio_programa)

    @api.one
    def B_ff_programa(self):
        b_fecha = self.env['programa.programa_obra'].search([('obra.id', '=', self.obra.id)])
        self.fecha_termino_programa = str(b_fecha.fecha_termino_programa)

    # METODO BUSCAR DIRECTOR DE OBRAS CONFIGURACION
    @api.one
    def BuscarDirector(self):
        b_director = self.env['ir.config_parameter'].sudo().get_param('firmas_logos.nombre_subdirector_obra')
        print(b_director)
        self.subdirector_contrato = b_director

    @api.one
    def estid(self):
        numero = 100000 + self.id
        self.ide_estimacion = str(numero)

    # COMPUTE CONTAR ESTIMACIONES
    '''@api.one
    @api.depends('obra')
    def ido(self):
        self.idobra = str(self.env['control.estimaciones'].search_count([('obra', '=', self.obra.id)]))'''

    # METODO BUSCAR IVA EN CONFIGURACION
    @api.one
    def BuscarIva(self):
        iva = self.env['ir.config_parameter'].sudo().get_param('generales.iva')
        self.b_iva = iva

    @api.model
    def create(self, values):
        num = int(values['estimacion_ids'])
        num = num + 1
        print(num)
        values['idobra'] = str(num)
        return super(Estimaciones, self).create(values)

    '''# METODO PARA EL CONTADOR DE ESTIMACIONES
    @api.model
    def create(self, values):
        count = self.env['partidas.partidas'].search_count([('id', '=', self.obra.id)])
        print(count)
        count = count + 1
        values['numero_estimacion'] = count
        return super(Estimaciones, self).create(values)'''

    # METODO CREATE PARA CREAR LA ID DE ESTIMACION
    @api.multi
    @api.onchange('obra')
    def IdEstimacion(self):
        self.estimacion_ids = str(self.env['control.estimaciones'].search_count([('obra', '=', self.obra.id)]))

    # METODO PARA JALAR DATOS DE LAS DEDUCCIONES DEL CONTRATO
    @api.multi
    @api.onchange('p_id')  # if these fields are changed, call method
    def deduccion(self):
        adirecta_id = self.env['proceso.elaboracion_contrato'].browse(self.numero_contrato.id)
        self.update({
            'deducciones': [[5]]
        })
        for deducciones in adirecta_id.deducciones:
            self.update({
                'deducciones': [[0, 0, {'name': deducciones.name, 'porcentaje': deducciones.porcentaje}]]
            })

    # METODO PARA JALAR IMPORTE DE LOS CONCEPTOS DE PARTIDA
    @api.onchange('conceptos_partidas')
    def suma_conceptos(self):
        suma = 0
        for i in self.conceptos_partidas:
            resultado = i.importe_ejecutado
            suma = suma + resultado
            self.estimado = suma

    # METODO PARA CALCULAR ESTIMACION NETA SIN IVA
    @api.one
    @api.depends('estimado')
    def Estimacion_sinIva(self):
        for rec in self:
            rec.update({
                'estimacion_subtotal': (self.estimado - self.amort_anticipo) - (self.estimado * self.b_iva)
            })

    # METODO PARA CALCULAR ESTIMACION IVA.
    @api.one
    @api.depends('estimado')
    def Estimacion_Iva(self):
        for rec in self:
            rec.update({
                'estimacion_iva': (self.estimado - self.amort_anticipo) * self.b_iva
            })

    # METODO PARA CALCULAR ESTIMACION + IVA
    @api.one
    @api.depends('estimacion_iva')
    def Estimacion_conIva(self):
        for rec in self:
            rec.update({
                'estimacion_facturado': self.estimacion_subtotal + self.estimacion_iva
            })

    # METODO PARA SUMAR DEDUCCIONES
    @api.multi
    @api.onchange('estimacion_facturado')
    def SumaDeducciones(self):
        suma = 0
        for i in self.deducciones:
            resultado = i.valor
            suma = suma + resultado
            self.estimado_deducciones = suma

    # METODO PARA CALCULAR AMORTIZACION 30%
    @api.one
    @api.depends('estimado')
    def amortizacion_anticipo(self):
        for rec in self:
            rec.update({
                'amort_anticipo': self.estimado * self.amort_anticipo_partida
            })

    # METODO PARA AGREGAR IMPORTE A DEDUCCIONES
    @api.multi
    @api.onchange('estimado')
    def deduc(self):
        for rec in self.deducciones:
            rec.update({
                'valor': self.estimado * rec.porcentaje
            })

    # METODO PARA INSERTAR CONCEPTOS CONTRATADOS     ---------------VERIFICAR COMO CORRER EL METODO AL ENTRAR
    '''@api.multi
    @api.onchange('p_id')  # if these fields are changed, call method
    def conceptosEjecutados(self):
        adirecta_id = self.env['partidas.partidas'].browse(self.obra.id)
        self.update({
            'conceptos_partidas': [[5]]
        })
        for conceptos in adirecta_id.conceptos_partidas:
            self.update({
                'conceptos_partidas': [[0, 0, {'categoria': conceptos.categoria,
                                               'clave_linea': conceptos.clave_linea, 'concepto': conceptos.concepto,
                                               'medida': conceptos.medida,
                                               'precio_unitario': conceptos.precio_unitario,
                                               'cantidad': conceptos.cantidad}]]
            })'''


    @api.one
    def Estimacion(self):
        self.estimacion_id = self.id

    @api.one
    def obra_enlace(self):
        self.obra_id = self.obra


class Deducciones(models.Model):
    _name = 'control.deducciones'

    name = fields.Char()
    porcentaje = fields.Float()
    valor = fields.Float()
