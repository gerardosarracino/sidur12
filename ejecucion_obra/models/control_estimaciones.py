from odoo import models, fields, api, exceptions


class Estimaciones(models.Model):
    _name = 'control.estimaciones'
    _rec_name = 'obra'

    # enlace
    estimacion_id = fields.Char(compute="nombre", store=True)
    obra = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)
    obra_id = fields.Char(compute="ConvenioEnlace", store=True)

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

    # DEDUCCIONES
    deducciones = fields.Many2many('generales.deducciones', string="Deducciones:" )

    # Calculados
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
    conceptos_partidas = fields.Many2many('proceso.conceptos_part')

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


