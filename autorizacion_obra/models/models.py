from odoo import models, fields, api
from datetime import datetime

class AutorizacionDeObra(models.Model):
    _name = 'autorizacion_obra.oficios_de_autorizacion'
    name = fields.Char(string='Número de oficio', required=True)
    fecha_actual = fields.Date(string='Fecha',default=fields.Date.today(), required=True)
    fecha_de_recibido = fields.Date(string='Fecha de recibido', required=True)
    fecha_de_vencimiento = fields.Date(string='Fecha de vencimiento', required=True)
    importe = fields.Float(string='Importe', required=True)
    anexo_tec = fields.Integer(compute='contar')
    total_at = fields.Float(compute='suma_total_anexos')
    anexos = fields.One2many('autorizacion_obra.anexo_tecnico', 'name')
    total_atcancel = fields.Float(string='Importe anexos', compute='suma_total_cancel')

    @api.one
    def suma_total_anexos(self):
        ids = self.env['autorizacion_obra.anexo_tecnico'].search([('name', '=', self.id)])
        suma = 0
        for i in ids:
            resultado = self.env['autorizacion_obra.anexo_tecnico'].browse(i.id).total
            suma += float(resultado)
        self.total_at = suma

    @api.one
    def suma_total_cancel(self):
        ids1 = self.env['autorizacion_obra.anexo_tecnico'].search([('name', '=', self.id)])
        suma1 = 0
        for i in ids1:
            resultado1 = self.env['autorizacion_obra.anexo_tecnico'].browse(i.id).total1
            suma1 += float(resultado1)
        self.total_atcancel = suma1

    @api.one
    def contar(self):
        count = self.env['autorizacion_obra.anexo_tecnico'].search_count([('name', '=', self.id)])
        self.anexo_tec = count

class AnexoTecnico(models.Model):
    _name = 'autorizacion_obra.anexo_tecnico'
    _rec_name = 'id'
    name = fields.Many2one('autorizacion_obra.oficios_de_autorizacion', readonly=True)
    claveobra = fields.Char(string='Clave de obra', required=True)
    clave_presupuestal = fields.Char(string='Clave presupuestal', required=True)
    concepto = fields.Many2one('registro.programarobra', )
    federal = fields.Float(string='Federal')
    estatal = fields.Float(string='Estatal')
    municipal = fields.Float(string='Municipal')
    otros = fields.Float(string='Otros')
    total = fields.Float(compute="_total", store=True)
    cancelados = fields.Integer(compute='contar')
    total_ca = fields.Float(string='Cancelado',compute='suma_total_cancelado')
    total1 = fields.Float(string="Total", compute="_total1")
    cancelado = fields.One2many('autorizacion_obra.cancelarrecurso', 'name')

    @api.depends('federal','estatal','municipal','otros')
    def _total(self):
        for r in self:
            r.total = r.federal + r.estatal + r.municipal + r.otros

    @api.depends('total','total_ca')
    def _total1(self):
        for r in self:
            r.total1 = r.total - r.total_ca

    @api.one
    def suma_total_cancelado(self):
        ids = self.env['autorizacion_obra.cancelarrecurso'].search([('name', '=', self.id)])
        suma = 0
        for i in ids:
            resultado = self.env['autorizacion_obra.cancelarrecurso'].browse(i.id).totalc
            suma += float(resultado)
        self.total_ca = suma

    @api.one
    def contar(self):
        count = self.env['autorizacion_obra.cancelarrecurso'].search_count([('name', '=', self.id)])
        self.cancelados = count

class CancelacionRecursos(models.Model):
    _name = 'autorizacion_obra.cancelarrecurso'
    name = fields.Many2one('autorizacion_obra.anexo_tecnico', 'id', readonly=True)
    nooficio = fields.Char(string="No. Oficio", required=True)
    fecha = fields.Date(string="Fecha", required=True)
    federalc = fields.Float(string='Federal')
    estatalc = fields.Float(string='Estatal')
    municipalc = fields.Float(string='Municipal')
    otrosc = fields.Float(string='Otros')
    totalc = fields.Float(compute="_totalc", store=True)

    @api.depends('federalc','estatalc','municipalc','otrosc')
    def _totalc(self):
        for c in self:
            c.totalc = c.federalc + c.estatalc + c.municipalc + c.otrosc