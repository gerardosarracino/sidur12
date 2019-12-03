# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Eventos(models.Model):
    _name = 'proceso.eventos_licitacion'
    _rec_name = 'numerolicitacion_evento'

    licitacion_id = fields.Char(compute="nombre", store=True)

    numerolicitacion_evento = fields.Many2one('proceso.licitacion', string='Numero Licitación:', readonly=True,
                                              store=True)

    contratista_participantes = fields.Many2many('proceso.contra_participantev', store=True)
    contratista_aclaraciones = fields.Many2many('proceso.contra_aclaraciones', store=True)
    contratista_propuesta = fields.Many2many('proceso.contra_propuestas', compute="llenar_propuesta", store=True)
    contratista_fallo = fields.Many2many('proceso.contra_fallo', compute="llenar_fallo", store=True)

    aux = fields.Float(string="aux",  required=False, )

    @api.multi
    def dato_fallo(self):
        # VISTA OBJETIVO
        view = self.env.ref('proceso_contratacion.proceso_fallo_datos_form')
        # CONTADOR SI YA FUE CREADO
        count = self.env['proceso.datos_fallo'].search_count([('id', '=', self.id)])
        print(count)
        # BUSCAR VISTA
        search = self.env['proceso.datos_fallo'].search([('id', '=', self.id)])
        print(search)
        # SI YA FUE CREADA LA VISTA, ABRIR LA VISTA YA CREADA
        if count == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Fallo',
                'res_model': 'proceso.datos_fallo',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
                'res_id': search.id,
            }
        # NO A SIDO CREADA LA VISTA, CREARLA
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Fallo',
                'res_model': 'proceso.datos_fallo',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
            }

    @api.one
    def nombre(self):
        self.licitacion_id = self.id

    # METODO PARA Participantes VIsita
    @api.multi
    @api.onchange('aux')
    def llenar_evento(self):
        b_participante = self.env['proceso.participante'].search([('numerolicitacion.id', '=', self.numerolicitacion_evento.id)])
        self.update({
            'contratista_participantes': [[5]]
        })
        for i in b_participante.contratista_participantes:
            self.update({
                'contratista_participantes': [[0, 0, {'name': i.name, 'nombre_representante': i.nombre_representante,
                                                      'correo': i.correo}]]
            })

    # METODO PARA Participantes ACLARACIONES
    @api.multi
    @api.onchange('aux')
    def llenar_aclaraciones(self):
        b_participante = self.env['proceso.participante'].search(
            [('numerolicitacion.id', '=', self.numerolicitacion_evento.id)])
        self.update({
            'contratista_aclaraciones': [[5]]
        })
        for i in b_participante.contratista_participantes:
            self.update({
                'contratista_aclaraciones': [
                    [0, 0, {'name': i.name, 'nombre_representante': i.nombre_representante,
                            'correo': i.correo}]]
            })

    # METODO PARA PROPUESTA
    @api.one
    @api.depends('aux')
    def llenar_propuesta(self):
        b_participante = self.env['proceso.participante'].search(
            [('numerolicitacion.id', '=', self.numerolicitacion_evento.id)])
        self.update({
            'contratista_propuesta': [[5]]
        })
        id_lic = b_participante.numerolicitacion
        for i in b_participante.contratista_participantes:
            self.update({
                'contratista_propuesta': [
                    [0, 0, {'name': i.name, 'numerolicitacion': id_lic}]]
            })

    # METODO PARA Fallo
    @api.one
    @api.depends('aux')
    def llenar_fallo(self):
        b_participante = self.env['proceso.participante'].search(
            [('numerolicitacion.id', '=', self.numerolicitacion_evento.id)])
        self.update({
            'contratista_fallo': [[5]]
        })
        for i in b_participante.contratista_participantes:
            self.update({
                'contratista_fallo': [
                    [0, 0, {'name': i.name}]]
            })


# VISITA DE OBRA
class ContratistaParticipanteV(models.Model):
    _name = 'proceso.contra_participantev'

    name = fields.Char(string="Licitante:")
    nombre_representante = fields.Char(string="Nombre del Representante:")
    correo = fields.Char(string="Correo:")
    asiste = fields.Boolean('Asiste')


# JUNTA ACLARACIONES
class JuntaAclaraciones(models.Model):
    _name = 'proceso.contra_aclaraciones'

    name = fields.Char(string="Licitante:")
    nombre_representante = fields.Char(string="Nombre del Representante:")
    correo = fields.Char(string="Correo:")
    asiste = fields.Boolean('Asiste')
    # preguntas
    pregunta = fields.Char(string="Pregunta:", required=False, )
    respuesta = fields.Text(string="Respuesta:", required=False, )

    # METODO PARA INGRESAR A RECURSOS BOTON
    @api.multi
    def aclaraciones(self):
        # VISTA OBJETIVO
        view = self.env.ref('proceso_contratacion.proceso_aclaraciones_form')
        # CONTADOR SI YA FUE CREADO
        count = self.env['proceso.contra_aclaraciones'].search_count([('id', '=', self.id)])
        # BUSCAR VISTA
        search = self.env['proceso.contra_aclaraciones'].search([('id', '=', self.id)])
        # SI YA FUE CREADA LA VISTA, ABRIR LA VISTA YA CREADA
        if count == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Preguntas',
                'res_model': 'proceso.contra_aclaraciones',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
                'res_id': search.id,
            }
        # NO A SIDO CREADA LA VISTA, CREARLA
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Preguntas',
                'res_model': 'proceso.contra_aclaraciones',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
            }


# Apertura de Propuestas
class AperturaPropuestas(models.Model):
    _name = 'proceso.contra_propuestas'

    numerolicitacion = fields.Many2one('proceso.licitacion', string='Numero Licitación:')

    name = fields.Char(string="Licitante:")
    monto = fields.Float(string="Monto:", readonly=True)
    asiste = fields.Boolean('Asiste')
    completa = fields.Boolean('Completa')
    revision = fields.Boolean('Para revisión')
    puntos_tecnicos = fields.Float('Puntos Tecnicos')
    puntos_economicos = fields.Float('Puntos Economicos')
    paso = fields.Boolean('Pasó')
    posicion = fields.Char('Posición', default="---")
    programar_obra_licitacion2 = fields.Many2many("proceso.propuesta_lic", string="Partida(s):", store=True)

    observaciones = fields.Text(string="Observaciones:", required=False, )

    aux = fields.Float(string="")

    @api.multi
    @api.onchange('programar_obra_licitacion2')
    def sumMonto(self):
        sum = 0
        for i in self.programar_obra_licitacion2:
            sum = sum + i.monto_partida
            self.monto = sum

    # METODO PARA Participantes VIsita
    @api.multi
    @api.onchange('aux')
    def llenar_licitacion(self):
        b_lic = self.env['proceso.licitacion'].search(
            [('id', '=', self.numerolicitacion.id)])
        print(b_lic)
        self.update({
            'programar_obra_licitacion2': [[5]]
        })
        for i in b_lic.programar_obra_licitacion:
            self.update({
                'programar_obra_licitacion2': [[0, 0, {'recursos': i.recursos}]]
            })

    # METODO PARA INGRESAR A PROPUESTAS BOTON
    @api.multi
    def propuestas(self):
        # VISTA OBJETIVO
        view = self.env.ref('proceso_contratacion.proceso_propuesta_form')
        # CONTADOR SI YA FUE CREADO
        count = self.env['proceso.contra_propuestas'].search_count([('id', '=', self.id)])
        # BUSCAR VISTA
        search = self.env['proceso.contra_propuestas'].search([('id', '=', self.id)])
        # SI YA FUE CREADA LA VISTA, ABRIR LA VISTA YA CREADA
        if count == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Propuesta',
                'res_model': 'proceso.contra_propuestas',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
                'res_id': search.id,
            }
        # NO A SIDO CREADA LA VISTA, CREARLA
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Propuesta',
                'res_model': 'proceso.contra_propuestas',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
            }


# Fallo
class Fallo(models.Model):
    _name = 'proceso.contra_fallo'

    name = fields.Char(string="Licitante:")
    monto = fields.Float(string="Monto Fallado A/I.V.A:")
    asiste = fields.Boolean('Asistió')
    ganador = fields.Boolean('Ganador')
    puntos_tecnicos = fields.Float('Puntos Tecnicos')
    puntos_economicos = fields.Float('Puntos Economicos')
    posicion = fields.Char('Posición', default="---")
    observaciones = fields.Text(string="Observaciones")

    # METODO PARA INGRESAR A PROPUESTAS BOTON
    @api.multi
    def fallo(self):
        # VISTA OBJETIVO
        view = self.env.ref('proceso_contratacion.proceso_fallo_form')
        # CONTADOR SI YA FUE CREADO
        count = self.env['proceso.contra_fallo'].search_count([('id', '=', self.id)])
        # BUSCAR VISTA
        search = self.env['proceso.contra_fallo'].search([('id', '=', self.id)])
        # SI YA FUE CREADA LA VISTA, ABRIR LA VISTA YA CREADA
        if count == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Fallo',
                'res_model': 'proceso.contra_fallo',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
                'res_id': search.id,
            }
        # NO A SIDO CREADA LA VISTA, CREARLA
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Fallo',
                'res_model': 'proceso.contra_fallo',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
            }


class DatosFallo(models.Model):
    _name = 'proceso.datos_fallo'

    numerolicitacion = fields.Many2one('proceso.licitacion', string='Numero Licitación:', readonly=True, store=True)
    id_eventos = fields.Many2one('proceso.eventos_licitacion')

    ganador = fields.Char(string="Ganador:", )
    fecha_fallo = fields.Date(string="Fecha Fallo:")
    hora_inicio_f = fields.Datetime(string="Hora de Inicio Fallo:")
    hora_termino_f = fields.Datetime('Hora Termino Fallo:')
    hora_inicio_o = fields.Date('Fecha Inicio Obra:')
    hora_termino_o = fields.Date('Fecha Termino Obra:')
    plazo = fields.Integer('Plazo')
    hora_antes_firma = fields.Datetime('Hora Antes Firma Contrato:')
    fecha_fcontrato = fields.Date('Fecha firma contrato:')

    importe_ganador = fields.Float('Importe Ganador:')
    iva = fields.Float('I.V.A')
    total_contratado = fields.Float('Total Contratado:	')

    recursos = fields.Many2many('partidas.licitacion')


class PropuestaLic(models.Model):
    _name = 'proceso.propuesta_lic'

    recursos = fields.Many2one('autorizacion_obra.anexo_tecnico', 'Recursos')
    monto_partida = fields.Float(string="" )


class Licitacion(models.Model):
    _name = "proceso.licitacion"
    _rec_name = 'numerolicitacion'

    licitacion_id = fields.Char(compute="nombre", store=True)

    programa_inversion_licitacion = fields.Many2one('generales.programas_inversion', 'Programa de Inversión')

    programar_obra_licitacion = fields.Many2many("partidas.licitacion", string="Partida(s):", ondelete="cascade")

    name = fields.Text(string="Objeto De La Licitación", )
    select = [('1', 'Licitación publica'), ('2', 'Licitación simplificada/Por invitación')]
    tipolicitacion = fields.Selection(select, string="Tipo de Licitación", default="1", )

    numerolicitacion = fields.Char(string="Número de Licitación", )

    estado_obra_desierta = fields.Integer(compute='estadoObraDesierta')
    estado_obra_cancelar = fields.Integer(compute='estadoObraCancelar')

    convocatoria = fields.Char(string="Convocatoria", )
    fechaconinv = fields.Date(string="Fecha Con/Inv", )
    select1 = [('1', 'Estatal'), ('2', 'Nacional'), ('3', 'Internacional')]
    caracter = fields.Selection(select1, string="Carácter", default="1", )
    select2 = [('1', 'Federal'), ('2', 'Estatal')]
    normatividad = fields.Selection(select2, string="Normatividad", required=True )
    funcionariopresideactos = fields.Char(string="Funcionario que preside actos", )
    puesto = fields.Text(string="Puesto", )
    numerooficio = fields.Char(string="Numero oficio", )
    fechaoficio = fields.Date(string="Fecha oficio", )
    oficioinvitacioncontraloria = fields.Char(string="Oficio invitación contraloría", )
    fechaoficio2 = fields.Date(string="Fecha oficio", )
    notariopublico = fields.Text(string="Notario publico", )
    fechalimiteentregabases = fields.Date(string="Fecha Límite para la entrega de Bases", )
    fecharegistrocompranet = fields.Date(string="Fecha Registro CompraNet", )
    costobasesdependencia = fields.Float(string="Costo de Bases Dependencia", )
    costocompranetbanco = fields.Float(string="Costo CompraNET/Banco",)
    fechaestimadainicio = fields.Date(string="Fecha Estimada de Inicio", )
    fechaestimadatermino = fields.Date(string="Fecha Estimada de Termino", )
    plazodias = fields.Integer(string="Plazo de Días", )
    capitalcontable = fields.Float(string="Capital Contable",)
    anticipomaterial = fields.Float(string="Anticipo Material %")
    anticipoinicio = fields.Float(string="Anticipo Inicio %")
    puntosminimospropuestatecnica = fields.Char(string="Puntos mínimos propuesta técnica")
    visitafechahora = fields.Datetime(string="Fecha/Hora")
    visitalugar = fields.Text(string="Lugar")
    juntafechahora = fields.Datetime(string="Fecha/Hora")
    juntalugar = fields.Text(string="Lugar")
    aperturafechahora = fields.Datetime(string="Fecha/Hora")
    aperturalugar = fields.Text(string="Lugar")
    fallofechahora = fields.Datetime(string="Fecha/Hora")
    fallolugar = fields.Text(string="Lugar")

    select3 = [('1', 'EN PROCESO, RECIEN CREADA'), ('2', 'Apertura de preposiciones'), ('3', 'Junta de aclaraciones'),
               ('4', 'Licitación enviada para su contratación')]
    estatus = fields.Selection(select3, string="Estatus de Licitación", default="1", compute="estatus_licitaciones")

    @api.one
    def estatus_licitaciones(self):
        b_eventos = self.env['proceso.eventos_licitacion'].search([('numerolicitacion_evento.id', '=', self.id)])
        b_participantes = self.env['proceso.participante'].search_count([('numerolicitacion.id', '=', self.id)])
        if b_participantes >= 1:
            print('asies')
        for i in b_eventos.contratista_aclaraciones:
            if i.asiste:
                self.estatus = '3'
            else:
                self.estatus = '1'

    variable_count = fields.Integer(compute='contar')

    estatus_licitacion = fields.Selection(
        [('borrador', 'Borrador'), ('confirmado', 'Confirmado'), ('validado', 'Validado'), ],
        default='borrador')

    # METODO PARA INGRESAR A RECURSOS BOTON
    @api.multi
    def VentanaEventos(self):
        # VISTA OBJETIVO
        view = self.env.ref('proceso_contratacion.proceso_eventos_form')
        # CONTADOR SI YA FUE CREADO
        count = self.env['proceso.eventos_licitacion'].search_count([('numerolicitacion_evento.id', '=', self.id)])
        # BUSCAR VISTA
        search = self.env['proceso.eventos_licitacion'].search([('numerolicitacion_evento.id', '=', self.id)])
        # SI YA FUE CREADA LA VISTA, ABRIR LA VISTA YA CREADA
        if count == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Eventos',
                'res_model': 'proceso.eventos_licitacion',
                'view_mode': 'form',
                'target': 'self',
                'view_id': view.id,
                'res_id': search.id,
            }
        # NO A SIDO CREADA LA VISTA, CREARLA
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Eventos',
                'res_model': 'proceso.eventos_licitacion',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
            }

        # METODO PARA INGRESAR A RECURSOS BOTON

    @api.multi
    def VentanaParticipantes(self):
        # VISTA OBJETIVO
        view = self.env.ref('proceso_contratacion.proceso_participantes_form')
        # CONTADOR SI YA FUE CREADO
        count = self.env['proceso.participante'].search_count([('numerolicitacion.id', '=', self.id)])
        # BUSCAR VISTA
        search = self.env['proceso.participante'].search([('numerolicitacion.id', '=', self.id)])
        # SI YA FUE CREADA LA VISTA, ABRIR LA VISTA YA CREADA
        if count == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Participantes',
                'res_model': 'proceso.participante',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
                'res_id': search.id,
            }
        # NO A SIDO CREADA LA VISTA, CREARLA
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Participantes',
                'res_model': 'proceso.participante',
                'view_mode': 'form',
                'target': 'new',
                'view_id': view.id,
            }

    @api.one
    def borrador_progressbar(self):
        self.write({'estatus_licitacion': 'borrador', })

    @api.one
    def confirmado_progressbar(self):
        self.write({'estatus_licitacion': 'confirmado'})

    @api.one
    def validado_progressbar(self):
        self.write({'estatus_licitacion': 'validado'})

    @api.multi
    @api.onchange('programas_inversion_adjudicacion')
    def BorrarTabla(self):
        self.update({
            'programar_obra_adjudicacion': [[5]]
        })

    # METODO CONTADOR DE PARTICIPANTES
    @api.one
    def contar(self):
        count = self.env['proceso.participante'].search_count([('numerolicitacion', '=', self.id)])
        self.variable_count = count

    # METODO DE OBRA DESIERTA
    @api.one
    def estadoObraDesierta(self):
        resultado = self.env['proceso.estado_obra_desierta'].search_count([('numerolicitacion', '=', self.id)])
        self.estado_obra_desierta = resultado

    # METODO DE OBRA CANCELADA
    @api.one
    def estadoObraCancelar(self):
        resultado = self.env['proceso.estado_obra_cancelar'].search_count([('numerolicitacion', '=', self.id)])
        self.estado_obra_cancelar = resultado

    # ENLACE CON LA LICITACION
    @api.one
    def nombre(self):
        self.licitacion_id = self.numerolicitacion


class Participante(models.Model):
    _name = 'proceso.participante'

    licitacion_id = fields.Char(compute="nombre", store=True)
    numerolicitacion = fields.Many2one('proceso.licitacion', string='Numero Licitación:',
                                       readonly=True)
    contratista_participantes = fields.Many2many('contratista.contratista')

    @api.one
    def nombre(self):
        self.licitacion_id = self.id


class EstadoObraDesierta(models.Model):
    _name = 'proceso.estado_obra_desierta'
    _rec_name = 'estado_obra_desierta'

    obra_id_desierta = fields.Char(compute="estadoObra", store=True)
    licitacion_id = fields.Char(compute="nombre", store=True)
    estado_obra_desierta = fields.Char(string="estado obra", default="Desierta", readonly=True)
    numerolicitacion = fields.Many2one('proceso.licitacion', string='Numero Licitación:',
                                       readonly=True)
    fecha_desierta = fields.Date(string="Fecha de Desierta:")
    observaciones_desierta = fields.Text(string="Observaciones:")

    @api.one
    def estadoObra(self):
        self.obra_id_desierta = self.estado_obra_desierta

    @api.one
    def nombre(self):
        self.licitacion_id = self.id


class EstadoObraCancelar(models.Model):
    _name = 'proceso.estado_obra_cancelar'

    obra_id_cancelar = fields.Char(compute="estadoObra", store=True)
    licitacion_id = fields.Char(compute="nombre", store=True)
    estado_obra_cancelar = fields.Char(string="estado obra", default="Cancelada", readonly=True)
    numerolicitacion = fields.Many2one('proceso.licitacion', string='Numero Licitación:',
                                       readonly=True)
    fecha_cancelado = fields.Date(string="Fecha de Cancelacion:")
    observaciones_cancelado = fields.Text(string="Observaciones:")

    @api.one
    def estadoObraCancelar(self):
        self.obra_id_cancelar = self.estado_obra_cancelar

    @api.one
    def nombre(self):
        self.licitacion_id = self.id



