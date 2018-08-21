#
import pandas
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, Plot,DataRange1d
from bokeh.models.glyphs import Line

df = pandas.read_csv("postos_df_header.csv", sep = ";",encoding='latin-1')
print(df.info(verbose=True, null_counts=True))

lista_postos_unicos = df.drop_duplicates()
lista_postos_unicos = lista_postos_unicos["cnpj"].tolist()

for j in range(len(lista_postos_unicos)):
    temp = df[df["cnpj"] == lista_postos_unicos[j]]
    index = [i for i in range(len(temp))]
    temp["x"] = index
    if j == 3:
        break

source = ColumnDataSource(temp)

xdr = DataRange1d()
ydr = DataRange1d()
plot = Plot(
    title=None, x_range=xdr, y_range=ydr)

glyph = Line(x="x", y="preo_venda_gasolina", line_color="#f46d43", line_width=6, line_alpha=0.6)
plot.add_glyph(source, glyph)
show(plot)