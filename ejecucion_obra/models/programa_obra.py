from odoo import models, fields, api, exceptions


class ProgramaObra(models.Model):
    _name = 'programa.programa_obra'
    _rec_name = 'obra'

    obra = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)
    obra_id = fields.Char(compute="partidaEnlace", store=True)

    fecha_inicio_programa = fields.Date('Fecha Inicio:', related="programa_contratos.fecha_inicio")
    fecha_termino_programa = fields.Date('Fecha Término:', compute="fechaTermino")
    monto_programa_aux = fields.Float(compute='SumaProgramas')
    restante_programa = fields.Float(string="Restante:", compute='DiferenciaPrograma')
    programa_contratos = fields.Many2many('proceso.programa', string="Agregar Periodo:")

    razon = fields.Text(string="Versión:", required=False, default="")

    total_partida = fields.Float(string="Total", related="obra.total_partida")

    select_tipo = [('1', 'Monto'), ('2', 'Plazo'), ('3', 'Ambos')]
    tipo = fields.Selection(select_tipo, string="Tipo:")

    @api.multi
    def write(self, values):
        if len(values['tipo']) == 0:
            raise exceptions.Warning('2')

        if values['razon'] is False:
            raise exceptions.Warning('2')

        version = self.env['programa.programa_version']
        id_programa = self.id
        datos = {'comentario': values['razon'], 'programa': id_programa, 'tipo': values['tipo']}
        nueva_version = version.create(datos)
        values['razon'] = ""
        values['tipo'] = ""
        return super(ProgramaObra, self).write(values)

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


# CLASE NUEVA
class ProgramaVersion(models.Model):
    _name = 'programa.programa_version'
    _rec_name = 'programa'

    select_tipo = [('1', 'Monto'), ('2', 'Plazo'), ('3', 'Ambos')]
    tipo = fields.Selection(select_tipo, string="Tipo:")
    fecha = fields.Date('Fecha:', default=fields.Date.today())
    programa = fields.Many2one('programa.programa_obra', string="Programa:")
    comentario = fields.Text(string="Comentario:", required=False, )


# CLASE VIEJA
class ProgramaObraVersion(models.Model):
    _name = 'programa.programa_obra_version'
    _rec_name = 'obra'

    fecha_version = fields.Date('Fecha de la Versión:')
    razon = fields.Text(string="Versión:", required=False, )

    programa_ids = fields.Char(string="ID")
    programa_id = fields.Char(string="Numero de Version del Programa:")
    obra = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)
    obra_id = fields.Char(compute="partidaEnlace", store=True)

    fecha_inicio_programa = fields.Date('Fecha Inicio:', related="programa_contrato_version.fecha_inicio")
    fecha_termino_programa = fields.Date('Fecha Término:', compute="fechaTermino")
    monto_programa_aux = fields.Float(compute='SumaProgramasVersion')
    restante_programa = fields.Float(string="Restante:", compute='DiferenciaProgramaVersion')
    programa_contrato_version = fields.Many2many('programa.tabla', string="Agregar Periodo:")

    total_partida = fields.Float(string="Total", related="obra.total_partida")
    auxiliar = fields.Float(string="auxiliar", )

    @api.model
    def create(self, values):
        num = int(values['programa_ids'])
        num = num + 1
        print(num)
        values['programa_id'] = str(num)
        return super(ProgramaObraVersion, self).create(values)

    # METODO CREATE PARA CREAR LA ID DE ESTIMACION
    @api.multi
    @api.onchange('obra')
    def idPrograma(self):
        self.programa_ids = str(self.env['programa.programa_obra_version'].search_count([('obra.id', '=', self.obra.id)]))

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