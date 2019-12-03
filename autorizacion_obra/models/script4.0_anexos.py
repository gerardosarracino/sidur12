import odoorpc, csv

usuario = 'admin'
password = 'admin'
odoo = odoorpc.ODOO('sidur.galartec.com', port=80)
odoo.login('sidur2', usuario, password)
anexos = odoo.env['autorizacion_obra.anexo_tecnico']

x = anexos.search([('name','=',False)])
print(len(x))
contador = 0
for i in x:
    anexo_actual = anexos.browse(i)
    busqueda_oficio = odoo.env['autorizacion_obra.oficios_de_autorizacion'].search([('id_sideop','=',anexo_actual.id_oficio_sideop)])[0]
    try:
        anexo_actual.write({
        'name': busqueda_oficio
        })
    except:
        print("Fallo")
    contador = contador + 1
    print(contador)