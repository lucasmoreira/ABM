#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 02:06:57 2018

@author: renexavier
"""

print(__doc__)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
import matplotlib
import matplotlib.pyplot as plt

file_name = "Auto2017-BSB.xlsx"
path = "/Users/renexavier/Documents/Developer/LAMFO/Carteis/Dados/" + file_name
sheet = "BASE"
dfs = pd.read_excel(path, sheet_name = sheet)

#linhas x colunas
dfs.shape

#informações sobre as colunas
dfs.info()

#########################
#     DISTRIBUIDORAS
#########################
#somente 9 distribuidoras
dfs.distribuidora_gasolina.nunique()

#maior parte Petrobras, DPPI e Raizen
dfs.distribuidora_gasolina.describe()

dfs.distribuidora_gasolina.value_counts()

#poucas ocorrencias
dfs.distribuidora_gasolina.count()

#9,79% precisamente
dfs.distribuidora_gasolina.count()/dfs.shape[0]*100

sns.set()
sns.distplot(dfs.distribuidora_gasolina.values)
plt.show()

eventType_strenght = {'PETROBRAS DISTRIBUIDORA S.A.': 1,
                      'DPPI': 2,
                      'RAIZEN': 3,
                      'MASUT DISTRIBUIDORA': 4,
                      'ALE COMBUSTÍVEIS': 5,
                      'ZEMA': 6,
                      'TOTAL': 7,
                      'CIAPETRO': 8}


#########################
#          CNPJ
#########################
#cnpjs únicos 132
dfs.cnpj.nunique()

#desses, os com maior coleta tem entre 20 a 33 coletas no ano todo
dfs.cnpj.value_counts()

formatCnpj = lambda x: int('1' + x.translate(str.maketrans('','','./-')))
dfs['cnpj_formatado'] = dfs['cnpj'].map(formatCnpj)

#grafico não ok
sns.set()
sns.distplot(dfs.cnpj_formatado.value_counts().values)
plt.show()

#########################
#          DATAS
#########################
#temos coletas nas 52 semanas do ano
dfs.semana_inicio.nunique()

#!!!dessas semanas SEMPRE são buscados 34 postos [pensativo]
dfs.semana_inicio.value_counts()

#temos coletas nas 52 semanas do ano
dfs.semana_fim.nunique()

#!!!dessas semanas SEMPRE são buscados 34 postos [pensativo]
dfs.semana_fim.value_counts()

#########################
#          PRECOS
#########################
#informacoes sobre o preco de venda da gasolina
dfs.venda_gasolina.describe()

#preco de compra incompleto
dfs.compra_gasolina.describe()

#32.65% de preço de compra
dfs.compra_gasolina.count()/dfs.shape[0]*100

sns.set()
sns.lmplot(x='compra_gasolina', y='venda_gasolina', data=dfs)
plt.show()


#########################
#       LOCALIZAÇÃO
#########################
formatLocation = lambda x: '%.6f' % x
dfs['latitude_formatado'] = dfs.latitude.map(formatLocation)
dfs['longitude_formatado'] = dfs.longitude.map(formatLocation)


#########################
#       NOVO DF
#########################
newDf = pd.DataFrame()
newDf["semana_inicio"] = dfs["semana_inicio"]
newDf['cnpj'] = dfs.cnpj_formatado
newDf['latitude'] = dfs['latitude_formatado']
newDf['logitude'] = dfs['longitude_formatado']
newDf['venda'] = dfs.venda_gasolina

teste = pd.DataFrame()
teste['cnpj'] = dfs.cnpj_formatado
teste['venda'] = dfs.venda_gasolina
#sns.jointplot(x="semana_inicio", y="semana_fim", data=newDF);


scaler = preprocessing.Normalizer()
scaled_teste = scaler.fit_transform(teste)
scaled_teste = pd.DataFrame(scaled_teste, columns=teste.columns)


# #############################################################################
# Compute DBSCAN
#eps é a distância, quanto menor, mais próximo ele busca, maior, mais abrangente
db = DBSCAN(eps=0.1, min_samples=10).fit(teste)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
#print("Silhouette Coefficient: %0.3f"
#      % metrics.silhouette_score(X, labels))

# #############################################################################
# Plot result

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    print(col)
    print("k %i" % k)
    class_member_mask = (labels == k)

    print(labels == k)
    print(class_member_mask & core_samples_mask)
    xy = teste[class_member_mask & core_samples_mask]
    print("xy")
    print(xy)
    plt.plot(xy["cnpj"], xy["venda"], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = teste[class_member_mask & ~core_samples_mask]
    plt.plot(xy["cnpj"], xy["venda"], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()

teste["cnpj"]




# Python-matplotlib Commands
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, .25)
Y = np.arange(-5, 5, .25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
Gx, Gy = np.gradient(Z) # gradients with respect to x and y
G = (Gx**2+Gy**2)**.5  # gradient magnitude
N = G/G.max()  # normalize 0..1
surf = ax.plot_surface(
    X, Y, Z, rstride=1, cstride=1,
    facecolors=cm.jet(N),
    linewidth=0, antialiased=False, shade=False)
plt.show()

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.random.standard_normal(100)
y = np.random.standard_normal(100)
z = np.random.standard_normal(100)
c = np.random.standard_normal(100)

ax.scatter(x, y, z, c=c, cmap=plt.hot())
plt.show()





