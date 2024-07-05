import re
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# create a connection to the database
cnx = sqlite3.connect('covid.db')

# set the URL to scrape data
url = "https://www.worldometers.info/coronavirus/country/brazil/"

# get the HTML content
response = requests.request(url=url, method="GET")
html = response.content

# parse the HTML content
soup = BeautifulSoup(html, features="html.parser")

# get the numbers of cases, deaths and recoveries
numbers = soup.findAll(class_="maincounter-number")
results = [span.find("span").get_text().strip() for span in numbers]

contents = [content.get_text().strip() for content in soup.findAll("script")]

df = pd.DataFrame()

for content in contents:
  # print(BeautifulSoup(content, features="html.parser").prettify())
  name = re.search(r"name:\s*'([^']*)'", content)
  yaxis = re.search(r"data:\s*(\[[^\]]*\])", content)
  xaxis = re.search(r"categories:\s*(\[[^\]]*\])", content)
  if yaxis:
    nameData = name.groups()[0]
    yAxisData = json.loads(yaxis.groups()[0])
    xAxisData = json.loads(xaxis.groups()[0])
    df[nameData] = yAxisData

# create the date column
df["Date"] = xAxisData
df["Date"] = df["Date"].apply(pd.to_datetime)

# mapping dates into seasons
# 1: Summer, 2: Autumn, 3: Winter, 4: Spring
seasons = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 1]
month_to_season = dict(zip(range(1, 13), seasons))
df["Season of the Year"] = df["Date"].dt.month.map(month_to_season)

# treating empty data
df["Death Rate"] = df["Death Rate"].apply(
  lambda x: 0 if isinstance(x, str) and x == "nan" else x)
df["Daily Cases"].fillna(0, inplace=True)
df["Daily Deaths"].fillna(0, inplace=True)
df["New Recoveries"].fillna(0, inplace=True)

df["Vaccination"] = df["Date"].apply(
  lambda x: 0 if x < pd.to_datetime("2021-01-17") else 1)

# set the date as the index
df.set_index("Date", inplace=True)

print(df.head(10))

# convert the data into a sqlite table
df.to_sql("covid", cnx, if_exists="replace")
