#
import pandas
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Plot,DataRange1d
from bokeh.models.glyphs import Line
import matplotlib.pyplot as plt


plt.style.use('seaborn-whitegrid')
import numpy as np




df = pandas.read_csv("postos_df_header.csv", sep = ";",encoding='latin-1')
print(df.info(verbose=True, null_counts=True))

lista_postos_unicos = df.drop_duplicates()
lista_postos_unicos = lista_postos_unicos["cnpj"].tolist()

for j in range(len(lista_postos_unicos)):
    temp = df[df["cnpj"] == lista_postos_unicos[j]]
    temp = temp.dropna(subset=["preo_venda_gasolina"])

    index = [i for i in range(len(temp))]
    temp["x"] = index

    venda = temp.dropna(subset=["preo_compra_gasolina"])

    if len(venda)>15 :

        #todo verificar se a diferenca de preco e maior que o minimo desejado
        temp["dif"] = [float(a.replace(",",".")) - float(b.replace(",",".")) for a in temp["preo_venda_gasolina"] for b in temp["preo_compra_gasolina"].tolist()]

        fig = plt.figure()
        ax = plt.axes()
        fig = plt.figure(figsize=(11, 8))
        ax1 = fig.add_subplot(111)
        ax1.plot(temp["x"].tolist(), temp["preo_venda_gasolina"].tolist(), label=1)
        ax1.plot(venda["x"].tolist(),venda["preo_compra_gasolina"].tolist(),label = 2)
        plt.savefig('smooth_plot.png')
        plt.show()
    print(j)