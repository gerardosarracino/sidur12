from odoo import models, fields, api, exceptions


class ProgramaObra(models.Model):
    _name = 'programa.programa_obra'
    _rec_name = 'obra'

    obra = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)

    obraid = fields.Many2one('partidas.partidas', string='Obra:', readonly=True)
    obra_id = fields.Char(compute="partidaEnlace", store=True)
    obra_id2 = fields.Char(compute="partidaEnlaceId", store=True)

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

    @api.one
    def partidaEnlaceId(self):
        self.obra_id2 = self.obraid

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


class TablaPrograma(models.Model):
    _name = 'programa.tabla'

    fecha_inicio = fields.Date()
    fecha_termino = fields.Date()
    monto = fields.Float()