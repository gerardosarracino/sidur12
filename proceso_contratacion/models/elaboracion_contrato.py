# -*- coding: utf-8 -*-

from odoo import exceptions
from odoo import api, fields, models, _


class ElaboracionContratos(models.Model):
    _name = "proceso.elaboracion_contrato"
    _rec_name = 'contrato'

    contrato_partida_licitacion = fields.Many2many('partidas.partidas', ondelete="cascade")
    contrato_partida_adjudicacion = fields.Many2many('partidas.partidas', ondelete="cascade")

    # RELATED CON LA OBRA DE LA PARTIDA PARA RELACIONARLA CON EL ANEXO TECNICO
    obra_partida = fields.Many2one(string="obra partida", related="contrato_partida_adjudicacion.obra")

    contrato_id = fields.Char(compute="nombre", store=True)

    # LICITACION
    obra = fields.Many2one('proceso.licitacion', string="Seleccionar obra")
    # ADJUDICACION
    adjudicacion = fields.Many2one('proceso.adjudicacion_directa', string="Nombre de Adjudicacion")

    # CONTAR REGISTROS DE FINIQUITO
    contar_finiquito = fields.Integer(compute='contar', string="PRUEBA")
    # CONTAR REGISTROS DE CONVENIO
    contar_convenio = fields.Integer(compute='contar2', string="PRUEBA")

    fecha = fields.Date(string="Fecha", required=True, default=fields.Date.today())

    contrato = fields.Char(string="Contrato", required=True)

    name = fields.Text(string="Descripción/Meta", required=True)

    descripciontrabajos = fields.Text(string="Descripción trabajos:", required=True)
    unidadresponsableejecucion = fields.Many2one('proceso.unidad_responsable', string="Unidad responsable de su ejecución", required=True)
    supervisionexterna = fields.Text(string="Supervisión externa")
    supervisionexterna1 = fields.Many2one('proceso.elaboracion_contrato', string="Supervisión externa:")

    # IMPORTE DEL CONTRATO LICITACION Y ADJUDICACION
    importe_contrato = fields.Float(string="Importe:", store=True)

    contratista = fields.Many2one('contratista.contratista', related="adjudicacion.contratista")
    fechainicio = fields.Date(string="Fecha de Inicio", required=True)

    fechatermino = fields.Date(string="Fecha de Termino", required=True)

    select = [('1', 'Diario'), ('2', 'Mensual'), ('3', 'Ninguno')]
    periodicidadretencion = fields.Selection(select, string="Periodicidad Retención", required=True, default="3")
    retencion = fields.Float(string="% Retencion")

    # Fianzas
    fianzas = fields.Many2many('proceso.fianza', string="Fianzas:")

    # Deducciones
    deducciones = fields.Many2many("generales.deducciones", string="Deducciones")

    # RECURSOS ANEXOS
    anexos = fields.Many2many('proceso.anexos', string="Anexos:")
    enlace_oficio = fields.Many2one('autorizacion_obra.oficios_de_autorizacion', string="Enlace a Oficio",)
    # related="anexos.name"
    recurso_autorizado = fields.Float(string='Recursos Autorizados:', related="anexos.name.total_at")
    importe_cancelado = fields.Float(string='Recursos Cancelados:', related="anexos.total_ca")
    total_recurso_aut = fields.Float(string='Total de Recursos Autorizados:', compute="recurso_total")
    # contratado_original = fields.Float(string="Contratado Original:	", related="contrato_partida_adjudicacion.total_partida")
    convenios_escalatorias = fields.Float(string="Convenios y Escalatorias:", readonly="True")
    total_contratado = fields.Float(string="Total Contratado:", compute="contratado_total")
    saldo = fields.Float(string="Saldo:", compute="saldo_total")

    # METODO PARA CALCULAR EL IMPORTE DEL CONTRATO
    @api.onchange('contrato_partida_adjudicacion')
    def importe_total(self):
        suma = 0
        for i in self.contrato_partida_adjudicacion and self.contrato_partida_licitacion:
            resultado = i.total_partida
            suma += resultado
            self.importe_contrato = suma

    # VALIDACIONES DE FECHAS
    @api.onchange('fechatermino')
    @api.depends('fechatermino', 'fechainicio')
    def onchange_fechatermino(self):
        if str(self.fechatermino) < str(self.fechainicio):
            raise exceptions.Warning('No se puede seleccionar una Fecha anterior a la fecha de inicio, '
                                     'por favor seleccione una fecha posterior')
        else:
            return False

    @api.onchange('fechainicio')
    @api.depends('fechatermino', 'fechainicio')
    def onchange_fechainicio(self):
        if str(self.fechatermino) < str(self.fechainicio):
            raise exceptions.Warning('No se puede seleccionar una Fecha posterior a la de termino, '
                                     'por favor seleccione una fecha anterior')
        else:
            return False

    # METODO PARA INYECTAR ANEXOS
    @api.multi
    @api.onchange('contrato_partida_adjudicacion')  # if these fields are changed, call method
    def llenar_anexo(self):
        adirecta_id = self.env['autorizacion_obra.anexo_tecnico'].search([('concepto', '=', self.obra_partida.id)])
        self.update({
            'anexos': [[5]]
        })
        for anexos_b in adirecta_id:
            self.update({
                'anexos': [[0, 0, {'name': anexos_b.name, 'claveobra': anexos_b.claveobra,
                                   'clave_presupuestal': anexos_b.clave_presupuestal,
                                   'federal': anexos_b.federal,
                                   'concepto': anexos_b.concepto,
                                   'estatal': anexos_b.estatal,
                                   'municipal': anexos_b.municipal, 'otros': anexos_b.otros,
                                   'ferderalin': anexos_b.federalin, 'estatalin': anexos_b.estatalin,
                                   'municipalin': anexos_b.municipalin, 'otrosin': anexos_b.otrosin,
                                   'total': anexos_b.total, 'cancelados': anexos_b.cancelados,
                                   'total_ca': anexos_b.total_ca,
                                   'total1': anexos_b.total1, 'totalin': anexos_b.totalin,
                                   'total_at': anexos_b.total_at,
                                      }]]
            })

    '''@api.one
    def contar_convenios(self):
        count = self.env['proceso.convenios_modificado'].search_count([('contrato', '=', self.contrato)])
        self.contador_convenios = count'''

    @api.depends('total_recurso_aut', 'total_contratado')
    def saldo_total(self):
        for rec in self:
            rec.update({
                'saldo': rec.total_recurso_aut - rec.total_contratado
            })

    @api.depends('importe_contrato', 'convenios_escalatorias')
    def contratado_total(self):
        for rec in self:
            rec.update({
                'total_contratado': rec.importe_contrato + rec.convenios_escalatorias
            })

    @api.depends('recurso_autorizado', 'importe_cancelado')
    def recurso_total(self):
        for rec in self:
            rec.update({
                'total_recurso_aut': rec.recurso_autorizado - rec.importe_cancelado
            })

    # METODO DE LAS PARTIDAS ADJUDICACION
    @api.multi
    @api.onchange('adjudicacion')  # if these fields are changed, call method
    def check_change_adjudicacion(self):
        adirecta_id = self.env['proceso.adjudicacion_directa'].browse(self.adjudicacion.id)
        self.update({
            'contrato_partida_adjudicacion': [[5]]
        })
        for partidas in adirecta_id.programar_obra_adjudicacion:
            self.update({
                'contrato_partida_adjudicacion': [[0, 0, {'obra': partidas.obra,
                                                          'programaInversion': partidas.programaInversion,
                                                          'monto_partida': partidas.monto_partida,
                                                          'iva_partida': partidas.iva_partida,
                                                          'total_partida': partidas.total_partida,
                                                          'nombre_partida': self.contrato
                                                          }]]
                     })

    @api.model
    def create(self, values):
        self.write({
            'contrato_partida_adjudicacion': [(0, 0, {'numero_contrato': self.contrato})]
        })
        return super(ElaboracionContratos, self).create(values)

    # METODO DE LAS PARTIDAS LICITACION
    @api.multi
    @api.onchange('obra')  # if these fields are changed, call method
    def check_change_licitacion(self):
        adirecta_id = self.env['proceso.licitacion'].browse(self.obra.id)
        self.update({
            'contrato_partida_licitacion': [[5]]
        })
        for partidas in adirecta_id.programar_obra_licitacion:
            self.update({
                'contrato_partida_licitacion': [[0, 0, {'obra': partidas.obra,
                                                          'programaInversion': partidas.programaInversion,
                                                          'monto_partida': partidas.monto_partida,
                                                          'iva_partida': partidas.iva_partida,
                                                          'total_partida': partidas.total_partida}]]
            })

    # METODO DE CONTAR REGISTROS DE FINIQUITOS PARA ABRIR VISTA EN MODO NEW O TREE VIEW
    @api.one
    def contar(self):
        count = self.env['proceso.finiquitar_anticipadamente'].search_count([('contrato', '=', self.id)])
        self.contar_finiquito = count

    # METODO DE CONTAR REGISTROS DE FINIQUITOS PARA ABRIR VISTA EN MODO NEW O TREE VIEW
    @api.one
    def contar2(self):
        count = self.env['proceso.convenios_modificado'].search_count([('contrato', '=', self.id)])
        self.contar_convenio = count

    # METODO DE ENLACE
    @api.one
    def nombre(self):
        self.contrato_id = self.contrato

    # CONVENIOS MODIFICATORIOS METODOS DE ABRIR VENTANA EN MODO NEW Y EN TREE VIEW
    @api.multi
    def conveniosModificados1(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Convenios Modificatorios',
            'res_model': 'proceso.convenios_modificado',
            'view_mode': 'form,tree',
            'target': 'new',
        }

    @api.multi
    def conveniosModificados2(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Convenios Modificatorios',
            'res_model': 'proceso.convenios_modificado',
            'view_mode': 'tree,form',
        }

    # FINIQUITAR CONTRATO METODOS DE ABRIR VENTANA EN MODO NEW Y EN TREE VIEW
    @api.multi
    def finiquitarContrato1(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Finiquitar Contrato Anticipadamente',
            'res_model': 'proceso.finiquitar_anticipadamente',
            'view_mode': 'form,tree',
            'target': 'new',
        }

    @api.multi
    def finiquitarContrato2(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Finiquitar Contrato Anticipadamente',
            'res_model': 'proceso.finiquitar_anticipadamente',
            'view_mode': 'tree,form',
        }

    #
    @api.multi
    def Seleccion(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seleccion de Obra',
            'res_model': 'proceso.elaboracion_contrato',
            'view_type': 'form',
            'target': 'new',
        }


class AnexosAuxiliar(models.Model):
    _name = 'proceso.anexos'

    name = fields.Many2one('autorizacion_obra.oficios_de_autorizacion')
    concepto = fields.Many2one('registro.programarobra')
    claveobra = fields.Char(string='Clave de obra')
    clave_presupuestal = fields.Char(string='Clave presupuestal')
    federal = fields.Float(string='Federal')
    estatal = fields.Float(string='Estatal')
    municipal = fields.Float(string='Municipal')
    otros = fields.Float(string='Otros')
    federalin = fields.Float(string='Federal')
    estatalin = fields.Float(string='Estatal')
    municipalin = fields.Float(string='Municipal')
    otrosin = fields.Float(string='Otros')
    total = fields.Float()
    cancelados = fields.Integer()
    total_ca = fields.Float(string='Cancelado')
    total1 = fields.Float(string="Total")
    totalin = fields.Float(string="Indirectos")

    total_at = fields.Float()


class UnidadResponsableEjecucion(models.Model):
    _name = 'proceso.unidad_responsable'

    name = fields.Char('Descripción:')


class Fianza(models.Model):
    _name = 'proceso.fianza'

    select_tipo_fianza = [('1', 'Cumplimiento'), ('2', 'Calidad/Vicios Ocultos'), ('3', 'Responsabilidad Civil'),
                          ('4', 'Ninguno')]
    tipo_fianza = fields.Selection(select_tipo_fianza, string="Tipo Fianza", default="4", required=True)
    numero_fianza_fianzas = fields.Integer(string="Numero Fianza", required=True)
    monto = fields.Float(string="Monto", required=True)
    fecha_fianza_fianzas = fields.Float(string="Fecha Fianza", required=True)
    afianzadora_fianzas = fields.Char(string="Afianzadora", required=True)


class ConveniosModificados(models.Model):
    _name = "proceso.convenios_modificado"

    contrato_id = fields.Char(compute="nombre", store=True)
    contrato = fields.Many2one('proceso.elaboracion_contrato', string='Numero Contrato:', readonly=True)

    fecha_convenios = fields.Date(string="Fecha:")
    name_convenios = fields.Text(string="Obra:")
    referencia = fields.Char(string="Referencia:")
    observaciones = fields.Text(string="Observaciones:")
    fecha_dictamen = fields.Text(string="Fecha Dictamen:")

    # RADIO BUTTON
    radio = [(
        '1', "Plazo"), ('2', "Objeto"), ('3', "Monto"), ('4', "Monto/Plazo"), ]
    tipo_convenio = fields.Selection(radio, string="Tipo de Convenio:")

    # CONDICION PLAZO
    plazo_fecha_inicio = fields.Date(string="Fecha Inicio:")
    plazo_fecha_termino = fields.Date(string="Fecha Termino:")
    # CONDICION OBJETO
    objeto_nuevo_objeto = fields.Text(string="Objeto:")
    # CONDICION MONTO
    select_monto = [(
        '1', "Ampliación:"), ('2', "Reducción:")]
    tipo_monto = fields.Selection(select_monto, string="Monto:")
    monto_importe = fields.Float(string="Importe:")
    monto_iva = fields.Float(string="I.V.A:", default=0.16)
    monto_total = fields.Float(string="Total:", compute="sumaMonto")
    # CONDICION MONTO PLAZO
    monto_plazo_fecha_inicio = fields.Date(string="Fecha Inicio:")
    monto_plazo_fecha_termino = fields.Date(string="Fecha Termino:")
    select_monto_plazo = [(
        '1', "Ampliación:"), ('2', "Reducción:")]
    tipo_monto_plazo = fields.Selection(select_monto_plazo, string="Monto:")
    monto_plazo_importe = fields.Float(string="Importe:")
    monto_plazo_iva = fields.Float(string="I.V.A:", default=0.16)
    monto_plazo_total = fields.Float(string="Total:", compute="sumaMontoPlazo")
    # TERMINA CONDICIONES RADIO BUTTON

    convenio_fecha_fianza = fields.Date(string="Fecha Fianza:")
    convenio_numero_fianza = fields.Integer(string="Numero Fianza:")
    convenio_afianzadora = fields.Char(string="Afianzadora:")
    convenio_monto_afianzadora = fields.Integer(string="Afianzadora:")

    @api.one
    def nombre(self):
        self.contrato_id = self.id

    @api.depends('monto_importe', 'monto_iva')
    def sumaMonto(self):
        for rec in self:
            rec.update({
                'monto_total': (rec.monto_importe * rec.monto_iva) + rec.monto_importe
            })

    @api.depends('monto_plazo_importe', 'monto_plazo_iva')
    def sumaMontoPlazo(self):
        for rec in self:
            rec.update({
                'monto_plazo_total': (rec.monto_plazo_importe * rec.monto_plazo_iva) + rec.monto_plazo_importe
            })


class FiniquitarContratoAnticipadamente(models.Model):
    _name = "proceso.finiquitar_anticipadamente"

    @api.one
    def nombre(self):
        self.contrato_id = self.id

    contrato_id = fields.Char(compute="nombre", store=True)
    contrato = fields.Many2one('proceso.elaboracion_contrato', string='Numero Contrato:', readonly=True)

    fecha = fields.Date(string="Fecha:")
    referencia = fields.Char(string="Referencia:")
    observaciones = fields.Text(string="Observaciones:")


class categoria(models.Model):
    _name = "proceso.categoria"
    name = fields.Char()


class concepto(models.Model):
    _name = "proceso.concepto"
    name = fields.Char()


class grupo(models.Model):
    _name = "proceso.grupo"
    name = fields.Char()


class medida(models.Model):
    _name = "proceso.medida"
    name = fields.Char()


class conceptos_partidas(models.Model):
    _name = "proceso.conceptos_part"

    name = fields.Char()
    sequence = fields.Integer()
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="")
    # prueba
    obra = fields.Many2one('partidas.partidas', string='Obra:', )

    categoria = fields.Many2one('proceso.categoria')
    concepto = fields.Many2one('proceso.concepto')
    grupo = fields.Many2one('proceso.grupo')
    medida = fields.Many2one('proceso.medida')
    precio_unitario = fields.Float()
    cantidad = fields.Integer()

    # CONCEPTOS EJECUTADOS EN EL PERIODO
    # contratada = fields.Float(string="Contratada",  required=False, compute="test")
    est_ant = fields.Integer(string="Est. Ant",  required=False, compute="sumaEst")
    pendiente = fields.Integer(string="Pendiente",  required=False, compute="Pendiente")
    estimacion = fields.Integer(string="Estimacion",  required=False, )
    importe_ejecutado = fields.Float(string="Importe",  required=False, compute="importeEjec")

    importe = fields.Float(compute="sumaCantidad")

    @api.depends('cantidad', 'estimacion')
    def sumaEst(self):
        for rec in self:
            rec.update({
                'est_ant': rec.cantidad - rec.estimacion
            })

    # VER COMO PROGRAMAREMOS EL ESTIMADO ANTERIOR DE OTRA ESTIMACION DE LA MISMA PROCEDENCIA
    @api.depends('cantidad', 'estimacion')
    def Pendiente(self):
        for rec in self:
            rec.update({
                'pendiente': rec.cantidad - rec.estimacion
            })

    @api.depends('precio_unitario', 'estimacion')
    def importeEjec(self):
        for rec in self:
            rec.update({
                'importe_ejecutado': rec.estimacion * rec.precio_unitario
            })

    @api.one
    def test(self):
        return 0

    @api.depends('precio_unitario', 'cantidad')
    def sumaCantidad(self):
        for rec in self:
            rec.update({
                'importe': rec.cantidad * rec.precio_unitario
            })






