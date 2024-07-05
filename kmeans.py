import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# criar conexão com o banco de dados
cnx = sqlite3.connect('covid.db')

# abrir os dados da tabela covid
df = pd.read_sql_query("SELECT * FROM covid", cnx)

features = df[['Death Rate', 'Cases', 'Daily Cases',
               'Currently Infected', 'Deaths', 'Daily Deaths', 'New Recoveries', 'Season of the Year', 'Vaccination']]

# Padronizando os dados
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Definindo o número de clusters
num_clusters = 3

# Inicializando e ajustando o modelo KMeans
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(scaled_features)

# Adicionando os labels dos clusters ao DataFrame original
df['Cluster'] = kmeans.labels_

cluster0 = df[df['Cluster'] == 0]['Death Rate'].mean()
cluster1 = df[df['Cluster'] == 1]['Death Rate'].mean()
cluster2 = df[df['Cluster'] == 2]['Death Rate'].mean()

print('cluster0 death rate mean:', cluster0)
print('cluster1 death rate mean:', cluster1)
print('cluster2 death rate mean:', cluster2)

cluster0 = df[df['Cluster'] == 0]['New Recoveries'].mean()
cluster1 = df[df['Cluster'] == 1]['New Recoveries'].mean()
cluster2 = df[df['Cluster'] == 2]['New Recoveries'].mean()

print('cluster0 new recoveries mean:', cluster0)
print('cluster1 new recoveries mean:', cluster1)
print('cluster2 new recoveries mean:', cluster2)

cluster0 = df[df['Cluster'] == 0]['Vaccination'].mean()
cluster1 = df[df['Cluster'] == 1]['Vaccination'].mean()
cluster2 = df[df['Cluster'] == 2]['Vaccination'].mean()

print('cluster0 Vaccination mean:', cluster0)
print('cluster1 Vaccination mean:', cluster1)
print('cluster2 Vaccination mean:', cluster2)


# Reduzindo para 2D com PCA
pca = PCA(n_components=2)
principal_components = pca.fit_transform(scaled_features)
df['PCA1'] = principal_components[:, 0]
df['PCA2'] = principal_components[:, 1]

new_cnx = sqlite3.connect('clusterized_covid.db')

df.to_sql("clusterized_covid", new_cnx, if_exists="replace")

print(df.head(10))

# Plotando os clusters
# plt.figure(figsize=(10, 6))
# plt.scatter(df['PCA1'], df['PCA2'], c=df['Cluster'], cmap='viridis')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')
# plt.title('Clusters visualizados com PCA')
# plt.colorbar(label='Cluster')
# plt.show()
