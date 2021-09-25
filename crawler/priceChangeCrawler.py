import requests
from bs4 import BeautifulSoup

url = r"https://gas.goodlife.tw/"

def priceChangeCrawler():
  res = requests.get(url)
  res.encoding = "utf-8"
  soup = BeautifulSoup(res.text, "html.parser")
  node = soup.find('li', attrs={"class": "main"})
  priceChange = node.h2.text.strip()
  return priceChange

