# -*- coding: utf-8 -*-

from odoo import api, fields, models


class conceptos_partidas(models.Model):
    _name = "proceso.conceptos_part"
    _rec_name = 'name'


    # clave
    name = fields.Many2one('catalogo.categoria', 'Nivel Padre')
    descripcion = fields.Text('Nivel', )
    # name = fields.Char()

    sequence = fields.Integer()
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="")

    clave_linea = fields.Char('Clave', required=True)

    # prueba
    obra = fields.Many2one('partidas.partidas', string='Obra:', )

    categoria = fields.Char()
    concepto = fields.Text(required=True)

    nivel = fields.Many2one('catalogo.categoria', 'Nivel', required=True)

    medida = fields.Char(required=True)
    precio_unitario = fields.Float(required=True)
    cantidad = fields.Integer(required=True)

    # MODIFICACIONES
    fecha_modificacion = fields.Date('Fecha de la Modificación')
    justificacion = fields.Text('Justificación de Modificación')

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

    @api.depends('precio_unitario', 'cantidad')
    def sumaCantidad(self):
        for rec in self:
            rec.update({
                'importe': rec.cantidad * rec.precio_unitario
            })


class ConceptosModificados(models.Model):
    _name = "proceso.conceptos_modificados"

    obra = fields.Many2one('partidas.partidas', string='Obra:', )

    justificacion = fields.Text('Justificación de Modificación')
    select_tipo = [('1', 'Monto'), ('2', 'Plazo'), ('3', 'Ambos')]
    tipo = fields.Selection(select_tipo, string="Tipo:")


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









