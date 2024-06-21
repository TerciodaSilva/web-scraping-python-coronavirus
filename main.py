import re
import json
import requests
from bs4 import BeautifulSoup

url = "https://www.worldometers.info/coronavirus/country/brazil/"

response = requests.request(url=url, method="GET")
html = response.content

soup = BeautifulSoup(html, features="html.parser")

numbers = soup.findAll(class_="maincounter-number")
results = [span.find("span").get_text().strip() for span in numbers]

contents = [content.get_text().strip() for content in soup.findAll("script")]

for content in contents:
    # print(BeautifulSoup(content, features="html.parser").prettify())
    name = re.search(r"name:\s*'([^']*)'", content)
    yaxis = re.search(r"data:\s*(\[[^\]]*\])", content)
    xaxis = re.search(r"categories:\s*(\[[^\]]*\])", content)
    if yaxis:
        print(name.groups()[0])
        print(json.loads(yaxis.groups()[0]))
        print(json.loads(xaxis.groups()[0]))