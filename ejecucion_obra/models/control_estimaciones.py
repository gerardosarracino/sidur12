from odoo import models, fields, api, exceptions


class Estimaciones(models.Model):
    _name = 'control.estimaciones'

    # ESTIMACIONES
    tipo_estimacion = fields.Char(string="", required=False, )
    fecha_inicio_estimacion = fields.Date(string="", required=False, )
    fecha_termino_estimacion = fields.Date(string="", required=False, )
    estimado = fields.Float(string="", required=False, )
    amort_anticipo = fields.Float(string="", required=False, )
    estimacion_subtotal = fields.Float(string="", required=False, )
    estimacion_iva = fields.Float(string="", required=False, )
    estimacion_facturado = fields.Float(string="", required=False, )
    estimado_deducciones = fields.Float(string="", required=False, )
    ret_dev = fields.Float(string="", required=False, )
    sancion = fields.Float(string="", required=False, )
    a_pagar = fields.Float(string="", required=False, )