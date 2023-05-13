import os
import requests
from bs4 import BeautifulSoup
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

url = "https://www.cnn.com/2023/05/11/africa/south-africa-russia-vessel-us-ambo-intl-afr/index.html"
response = requests.get(url)

if response.ok:
	soup = BeautifulSoup(response.text, "html.parser")
	content = soup.find(class_="article__content")

	#content = content.replace("<title>", "")
	#content = content.replace("</title>", "")
	print("The CNN content is : " + str(content))

os.system("pause")