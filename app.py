from flask import Flask
from flask_cors import CORS
import sqlite3
import pandas as pd

app = Flask(__name__)
CORS(app, origins=["http://localhost:5174"])


@app.route('/covid/pre-vaccination', methods=['GET'])
def get_pre_vaccination_data():
  cnx = sqlite3.connect('clusterized_covid.db')
  data = pd.read_sql_query(
    '''SELECT 
        round(AVG(c."Death Rate"), 2) as meanDeathRate, 
        round(AVG(c."New Recoveries"), 2) as meanNewRecoveries, 
        round(AVG(c."Daily Deaths"), 2) as meanDailyDeaths 
      FROM clusterized_covid c 
      WHERE c.Vaccination = 0''', cnx).to_dict(orient='records')[0]

  cnx.close()

  return data


@app.route('/covid/post-vaccination', methods=['GET'])
def get_post_vaccination_data():
  cnx = sqlite3.connect('clusterized_covid.db')
  data = pd.read_sql_query(
    '''SELECT 
        round(AVG(c."Death Rate"), 2) as meanDeathRate, 
        round(AVG(c."New Recoveries"), 2) as meanNewRecoveries, 
        round(AVG(c."Daily Deaths"), 2) as meanDailyDeaths 
      FROM clusterized_covid c 
      WHERE c.Vaccination = 1''', cnx).to_dict(orient='records')[0]

  cnx.close()

  return data


@app.route("/clusters", methods=['GET'])
def get_scatter_plot_data():
  cnx = sqlite3.connect('clusterized_covid.db')
  data = pd.read_sql_query(
    "SELECT PCA1, PCA2, Cluster FROM clusterized_covid", cnx).to_json(orient='records')

  cnx.close()

  return data


@app.route("/clusters-data", methods=['GET'])
def get_clusters_data():
  cnx = sqlite3.connect('clusterized_covid.db')
  data = pd.read_sql_query(
    '''SELECT 
        c.Cluster, 
        round(AVG(c."Death Rate"), 2) as meanDeathRate,
        round(AVG(c."New Recoveries"), 2) as meanNewRecoveries,
        round(AVG(c."Vaccination"), 2) as meanVaccination
        FROM clusterized_covid c group by c.Cluster''', cnx).to_json(orient='records')

  cnx.close()

  return data


@app.route("/covid/overall", methods=['GET'])
def get_overall_data():
  cnx = sqlite3.connect('clusterized_covid.db')
  data = pd.read_sql_query(
    '''SELECT 
        round(AVG(c."Death Rate"), 2) as meanDeathRate, 
        round(AVG(c."New Recoveries"), 2) as meanNewRecoveries, 
        round(AVG(c."Daily Deaths"), 2) as meanDailyDeaths 
      FROM clusterized_covid c''', cnx).to_dict(orient='records')[0]

  cnx.close()

  return data

if __name__ == '__main__':
  app.run(host="127.0.0.1", port=3000, debug=True)