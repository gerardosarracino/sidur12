from odoo import models, fields, api, exceptions

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class ruta_critica(models.Model):
    _name = 'proceso.rc'

    obra = fields.Many2one('registro.programarobra')
    name = fields.Char(string="ACTIVIDADES PRINCIPALES")
    porcentaje_est = fields.Integer(string="P.R.C")
    sequence = fields.Integer()
    avance_fisico = fields.Integer(string="% Avance")
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False)

    @api.model
    def create(self, values):
        if values.get('display_type', self.default_get(['display_type'])['display_type']):
            values.update(name=False, porcentaje_est=0)
        line = super(ruta_critica, self).create(values)
        return line

    @api.multi
    def write(self, values):
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError("You cannot change the type of a sale order line. Instead you should delete the current "
                            "line and create a new line of the proper type.")
        result = super(ruta_critica, self).write(values)
        return result


class ruta_critica_avance(models.Model):
    _name = 'proceso.rc_a'

    numero_contrato = fields.Many2one('partidas.partidas')
    # actividad = fields.Char(string="ACTIVIDADES PRINCIPALES")
    porcentaje_est = fields.Float(string="P.R.C")
    name = fields.Char(string="ACTIVIDADES PRINCIPALES")
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
            values.update(name=False, porcentaje_est=0)
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
