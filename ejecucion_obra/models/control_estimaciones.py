from odoo import models, fields, api, exceptions


class Estimaciones(models.Model):
    _name = 'control.estimaciones'
    _rec_name = 'obra'

    ide_estimacion = fields.Char(string="ID", compute="estid")
    # VER SI UTILIZAR
    estimacion_id = fields.Char()

    obra = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)
    obra_id = fields.Char(compute="ConvenioEnlace", store=True)

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

    fecha_inicio_estimacion = fields.Date(string="Del:", required=False, )
    fecha_termino_estimacion = fields.Date(string="Al:", required=False, )
    fecha_presentacion = fields.Date(string="Fecha de presentación:", required=False, )
    fecha_revision = fields.Date(string="Fecha revisión Residente:", required=False, )

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
    @api.multi
    @api.onchange('p_id')  # if these fields are changed, call method
    def conceptosEjecutados(self):
        adirecta_id = self.env['partidas.partidas'].browse(self.obra.id)
        self.update({
            'conceptos_partidas': [[5]]
        })
        for conceptos in adirecta_id.conceptos_partidas:
            self.update({
                'conceptos_partidas': [[0, 0, {'name': conceptos.name, 'sequence': conceptos.sequence,
                                               'display_type': conceptos.display_type,
                                               'categoria': conceptos.categoria, 'concepto': conceptos.concepto,
                                               'grupo': conceptos.grupo,
                                               'medida': conceptos.medida,
                                               'precio_unitario': conceptos.precio_unitario,
                                               'cantidad': conceptos.cantidad}]]
            })

    @api.one
    def Estimacion(self):
        self.estimacion_id = self.id

    @api.one
    def ConvenioEnlace(self):
        self.obra_id = self.obra


class Deducciones(models.Model):
    _name = 'control.deducciones'

    name = fields.Char()
    porcentaje = fields.Float()
    valor = fields.Float()
