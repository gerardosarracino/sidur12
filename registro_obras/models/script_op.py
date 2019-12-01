import odoorpc, csv


usuario = 'admin'
password = 'admin'
odoo = odoorpc.ODOO('sidur.galartec.com', port=80)
odoo.login('sidur2', usuario, password)
proveedores = odoo.env['res.partner']

with open('obras_planeadas.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['idsideop'])
        csv_id = row['idsideop']
        csv_registro = row['numeroobra']
        b = odoo.env['registro.obra'].search([('id_sideop', '=', csv_id)])
        for i in b:
            registro = odoo.env['registro.obra'].browse(i)
            registro.write({
                'name': csv_registro
            })
            print(registro)


# print "hecho"