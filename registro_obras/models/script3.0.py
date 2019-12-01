import odoorpc, csv

usuario = 'admin'
password = 'admin'
odoo = odoorpc.ODOO('sidur.galartec.com', port=80)
odoo.login('sidur2', usuario, password)
programarObra = odoo.env['registro.programarobra']

x = programarObra.search([("obra_planeada","=",False)])
print(len(x))
total = len(x)
for i in x:
    obraprog= programarObra.browse(i)
    if obraprog.obra_planeada.id == None:
        with open('obras_programadas_script.csv') as csvfile:
            #print(3)
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print(4)
                #print("id_programada : "+row['id_programada'])
                #print("obraprog.Id_obraprogramada : "+str(obraprog.Id_obraprogramada))
                if row['id_programada'] == str(obraprog.Id_obraprogramada):
                #    print(5)
                    registro = odoo.env['registro.obra'].search([("id_sideop","=",row['id_planeada'])])
                    for xd in registro:
                        idd = odoo.env['registro.obra'].browse(xd)
                        print(xd)
                        total = total - 1
                        print("faltan: "+ str(total))
                        obraprog.write({
                                'obra_planeada': str(idd.id)
                            })

            #csv_id = row['idsideop']