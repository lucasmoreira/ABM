#
import pandas
import csv
import numpy as np



#importa dados referentes ao DF
df = pandas.read_csv("postos_df_header.csv", sep = ";",encoding='latin-1')
print(df.info(verbose=True, null_counts=True))

#cria lista contendo apenas cnjpjs distintos do DF
lista_postos_unicos = df.drop_duplicates(subset=['cnpj'])
lista_postos_unicos = lista_postos_unicos["cnpj"].tolist()
candidatos = []

with open('employee_file.csv', mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    employee_writer.writerow(["cnpj"])

    for j in range(len(lista_postos_unicos)):

        #extrai informações referentes ao posto j e armazena temporariamente em temp
        temp = df[df["cnpj"] == lista_postos_unicos[j]]

        #armazena df com apenas linhas que contenham valor de venda
        venda = temp.dropna(subset=["preo_venda_gasolina"])


        if not len(venda) > 10:
            continue

        venda = venda.stack().str.replace(',', '.').unstack()
        venda['preo_venda_gasolina'] = venda['preo_venda_gasolina'].astype('float64')


        #calcula média de preço de venda
        media_venda = venda["preo_venda_gasolina"].mean()


        #adiciona index para temp
        index = [i for i in range(len(temp))]
        temp["x"] = index

        #armazena df com apenas linhas que contenham valor de compra
        compra = temp.dropna(subset=["preo_compra_gasolina"])

        if not len(compra) > 10:
            continue

        compra = compra.stack().str.replace(',', '.').unstack()
        compra["preo_compra_gasolina"] = compra['preo_compra_gasolina'].astype('float64')

        #calcula média de preço de compra da gasolina
        media_compra = compra["preo_compra_gasolina"].mean()
        diferenca = media_venda - media_compra

        if (diferenca > 0.3):
            print("append",lista_postos_unicos[j]," ",j)

            employee_writer.writerow([lista_postos_unicos[j]])

