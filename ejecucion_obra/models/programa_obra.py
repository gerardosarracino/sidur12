from odoo import models, fields, api


class ProgramaObra(models.Model):
    _name = 'programa.programa_obra'

    obra = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)
    obra_id = fields.Char(compute="partidaEnlace", store=True)

    fecha_inicio_programa = fields.Date('Fecha Inicio:', related="programa_contratos.fecha_inicio")
    fecha_termino_programa = fields.Date('Fecha Término:', compute="fechaTermino")
    monto_programa_aux = fields.Float(compute='SumaProgramas')
    restante_programa = fields.Float(string="Restante:", compute='DiferenciaPrograma')
    programa_contratos = fields.Many2many('proceso.programa', string="Agregar Periodo:")

    total_partida = fields.Float(string="Total", related="obra.total_partida")

    @api.one
    def partidaEnlace(self):
        self.obra_id = self.obra

    @api.multi
    @api.onchange('programa_contratos')
    def SumaProgramas(self):
        suma = 0
        for i in self.programa_contratos:
            resultado = i.monto
            suma = suma + resultado
            self.monto_programa_aux = suma

    # METODO PARA SACAR LA FECHA DEL M2M
    @api.one
    @api.depends('programa_contratos')
    def fechaTermino(self):
        for i in self.programa_contratos:
            resultado = str(i.fecha_termino)
            self.fecha_termino_programa = str(resultado)

    @api.one
    def DiferenciaPrograma(self):
        self.restante_programa = self.total_partida - self.monto_programa_aux


class ProgramaObraVersion(models.Model):
    _name = 'programa.programa_obra_version'
    _rec_name = 'obra'

    razon = fields.Text(string="Versión:", required=False, )

    obra = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)
    obra_id = fields.Char(compute="partidaEnlace", store=True)

    fecha_inicio_programa = fields.Date('Fecha Inicio:', related="programa_contrato_version.fecha_inicio")
    fecha_termino_programa = fields.Date('Fecha Término:', compute="fechaTermino")
    monto_programa_aux = fields.Float(compute='SumaProgramasVersion')
    restante_programa = fields.Float(string="Restante:", compute='DiferenciaProgramaVersion')
    programa_contrato_version = fields.Many2many('programa.tabla', string="Agregar Periodo:")

    total_partida = fields.Float(string="Total", related="obra.total_partida")
    auxiliar = fields.Float(string="auxiliar", )

    # METODO INSERTAR PROGRAMA
    @api.multi
    @api.onchange('auxiliar')  # if these fields are changed, call method
    def insetarPrograma(self):
        b_programa = self.env['programa.programa_obra'].search([('obra.id', '=', self.obra.id)])
        self.update({
            'programa_contrato_version': [[5]]
        })
        for programa in b_programa.programa_contratos:
            self.update({
                'programa_contrato_version': [[0, 0, {'fecha_inicio': programa.fecha_inicio,
                                                      'fecha_termino': programa.fecha_termino,
                                                      'monto': programa.monto}]]
            })

    @api.one
    def partidaEnlace(self):
        self.obra_id = self.obra

    @api.one
    @api.depends('programa_contrato_version')
    def SumaProgramasVersion(self):
        suma = 0
        for i in self.programa_contrato_version:
            resultado = i.monto
            suma = suma + resultado
            self.monto_programa_aux = suma

    # METODO PARA SACAR LA FECHA DEL M2M
    @api.one
    @api.depends('programa_contrato_version')
    def fechaTermino(self):
        for i in self.programa_contrato_version:
            resultado = str(i.fecha_termino)
            self.fecha_termino_programa = str(resultado)

    @api.one
    @api.depends('programa_contrato_version')
    def DiferenciaProgramaVersion(self):
        self.restante_programa = self.total_partida - self.monto_programa_aux


class TablaPrograma(models.Model):
    _name = 'programa.tabla'

    fecha_inicio = fields.Date()
    fecha_termino = fields.Date()
    monto = fields.Float()