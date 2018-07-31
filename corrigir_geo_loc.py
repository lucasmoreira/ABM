
import csv

with open(file, 'r', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    header_row = next(csvreader)

    for i in range(len(header_row)):
        print(i, header_row[i], '\n')

    for row in csvreader:
        nome = row[3]
        preco = row[12]
        estado = row[10]