from odoo import models, fields, api, exceptions


class Estimaciones(models.Model):
    _name = 'control.estimaciones'
    _rec_name = 'obra'

    # enlace
    estimacion_id = fields.Char(compute="nombre", store=True)
    obra = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)
    obra_id = fields.Char(compute="ConvenioEnlace", store=True)

    # AUXILIAR DE CONEXION HACIA CONTRATO
    numero_contrato = fields.Many2one(string="nc", related="obra.numero_contrato")

    # ESTIMACIONES
    radio_estimacion = [(
        '1', "Estimacion"), ('2', "Escalatoria")]
    tipo_estimacion = fields.Selection(radio_estimacion, string="")

    # estimacions_id = fields.Char(compute="estimacionId", store=True)
    numero_estimacion = fields.Integer(string="Número de Estimación:", compute="_get_increment")

    fecha_inicio_estimacion = fields.Date(string="Del:", required=False, )
    fecha_termino_estimacion = fields.Date(string="Al:", required=False, )
    fecha_presentacion = fields.Date(string="Fecha de presentación:", required=False, )
    fecha_revision = fields.Date(string="Fecha revisión Residente:", required=False, )

    radio_aplica = [(
        '1', "Estimación Finiquito"), ('2', "Amortizar Total Anticipo	")]
    si_aplica = fields.Selection(radio_aplica, string="")

    notas = fields.Text(string="Notas:", required=False, )

    # DEDUCCIONES related="obra.numero_contrato.deducciones"
    deducciones = fields.Many2many('control.deducciones', string="Deducciones:", )

    # Calculados
    estimado = fields.Float(string="Importe ejecutado estimación:", required=False, )

    amort_anticipo = fields.Float(string="Amortización de Anticipo 30%:", compute="amortizacion_anticipo", required=False, )
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
    conceptos_partidas = fields.Many2many('proceso.conceptos_part')
    total_conceptos = fields.Float(string="Total:",  required=False)

    # METODO PARA JALAR DATOS DE LAS DEDUCCIONES DEL CONTRATO
    @api.multi
    @api.onchange('conceptos_partidas')  # if these fields are changed, call method
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

    # METODO PARA AGREGAR IMPORTE A DEDUCCIONES
    @api.onchange('estimado')
    def deduc(self):
        for rec in self.deducciones:
            rec.update({
                'valor': self.estimado
            })

    # METODO PARA CALCULAR AMORTIZACION 30%
    @api.depends('estimado')
    def amortizacion_anticipo(self):
        for rec in self:
            rec.update({
                'amort_anticipo': self.estimado * 0.30
            })

    # METODO PARA INSERTAR CONCEPTOS CONTRATADOS
    @api.multi
    @api.onchange('estimacion_iva')  # if these fields are changed, call method
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

    # METODO PARA CONTAR NUMERO DE ESTIMACIONES
    @api.one
    def _get_increment(self):
        numero = self.env['control.estimaciones'].search_count([('numero_estimacion', '=', self.id)])
        self.numero_estimacion = numero

    @api.one
    def nombre(self):
        self.estimacion_id = self.id

    @api.one
    def ConvenioEnlace(self):
        self.obra_id = self.obra


class Deducciones(models.Model):
    _name = 'control.deducciones'

    name = fields.Char()
    porcentaje = fields.Float()
    valor = fields.Float()
