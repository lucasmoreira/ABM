
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 20:05:23 2018

@author: lucasgomes
"""
import psycopg2
import csv
from geopy.geocoders import GoogleV3
import time


con = psycopg2.connect(host='localhost', database='abm')
cur = con.cursor()

repetidos = 0
error = 0
count = 0
files = ["Auto2012.csv","Auto2013.csv","Auto2014.csv","Auto2015.csv","Auto2016.csv","Auto2017.csv"]
ano = 2012

for file in files:
    with open(file,'r',newline = '') as csvfile:
        csvreader = csv.reader(csvfile,delimiter=';')
        header_row = next(csvreader)

        for i in range(len(header_row)):
            print (i , header_row[i],'\n')

        for row in csvreader:
            nome = row[3]
            preco = row[12]
            estado = row[10]
            text = ""
            end = "BRAZIL " + str(row[10]) + " " + str(row[9]) + " " + str(row[4]) + " " + str(row[6]) + " " + str(
                row[7]) + " " + str(row[8])

            #if row [10] == "DISTRITO FEDERAL":

            for i in range(1, 33):
                text += ",'" + str(row[i]) +"'"
            try:
                # verifica se o nome do posto ja esta no BD
                sql = "select count(*) from public.postos where postos.razÃo_social like '%" + str(row[3])+"%'"
                cur.execute(sql)
                recset = cur.fetchall()
                con.commit()

                sql = "select count(*) from public.postos where postos.razÃo_social like '%" + str(
                    row[3]) + "%' and data_da_coleta like '%" + str(row[32]) + "%'"
                cur.execute(sql)
                recset2 = cur.fetchall()
            except Exception as e:
                print(e)
            con.commit()


            #caso o nome seja novo, roda-se o bloco
            if recset[0][0] == 0:
                try:

                    geolocator = GoogleV3(api_key= "AIzaSyA1b_95rVPHxUhuGGxaixIW4bgf8aMRndA")
                    location = geolocator.geocode(end)

                    sql = "insert into public.postos values (" + str(ano) + ",'"+ str(location.latitude)+"','" + str(location.longitude) +"','"+ row[0] +"'"+ text +" )"
                    cur.execute(sql)

                except Exception as e:
                    print(e)
                    error += 1
                con.commit()



            elif (recset2[0][0] == 0):
                repetidos += 1
                #print ("end repetido")

                try:
                    sql = "select lat, long from public.postos where postos.razÃo_social like '%" + str(row[3]) + "%'"
                    cur.execute(sql)
                    recset = cur.fetchall()
                    con.commit()

                    sql = "insert into public.postos values (" + str(ano) +",'"+ str(recset[0][0])+"','" + str(recset[0][1]) +"','"+ row[0] +"'"+ text +" )"
                    cur.execute(sql)
                    con.commit()
                    print("end copy")

                except Exception as e:
                    print(e)
                    error += 1
                con.commit()
            else:
                print("info repetida")
            con.commit()

            count += 1
            print("estamos no ano de "+str(ano)+ " com downloads: " + str(count))

        ano += 1
    csvfile.close()
print ("foram baixados "+str(count)+" enderecos com "+str(error)+ " erros e " +str(repetidos)+ " postos repetidos. ")

