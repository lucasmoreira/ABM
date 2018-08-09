import requests
import csv
import pandas

with open("postos_df_header.csv", 'r', newline='',encoding='latin-1') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    header_row = next(csvreader)

    for i in range(len(header_row)):
        print(i, header_row[i], '\n')

    for row in csvreader:
        CNPJ = row[5]
        #print(CNPJ)

r = requests.get('https://www.receitaws.com.br/v1/cnpj/27865757000102')
print(r.text)
df = pandas.DataFrame(r.text)

