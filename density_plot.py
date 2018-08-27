from mapsplotlib import mapsplot as mplt
import pandas as pd

df = pd.read_csv("postos_df_header.csv", sep = ";",encoding='latin-1')
candidatos = pd.read_csv("employee_file.csv", sep = ";",encoding='latin-1')
candidatos = candidatos["cnpj"].tolist()


df = df[df['cnpj'].isin(candidatos)]

df = df.stack().str.replace('.', '').unstack()

df["lat"] = df['lat'].astype('float64')
df["long"] = df['long'].astype('float64')


df["lat"] = df["lat"][abs(df["lat"]) > 150000000]
df["lat"] = df["lat"][abs(df["lat"]) < 160000000]

df["long"] = df["long"][abs(df["long"]) > 470000000]
df["long"] = df["long"][abs(df["long"]) < 490000000]

df = df.dropna(subset=["lat","long"])



df["lat"] = df["lat"]/10000000
df["long"] = df["long"]/10000000


mplt.register_api_key('AIzaSyA1b_95rVPHxUhuGGxaixIW4bgf8aMRndA')
mplt.density_plot(df["lat"],df["long"])
