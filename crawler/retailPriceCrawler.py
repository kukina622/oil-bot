import requests
from bs4 import BeautifulSoup
from lxml import etree

url = r"https://www2.moeaboe.gov.tw/oil102/oil2017/A01/A0108/tablesprices.asp"


def retailPriceCrawler():
  res = requests.get(url)
  soup = BeautifulSoup(res.text, "html.parser")
  infoList = []
  dom = etree.HTML(str(soup))

  # 中油價格
  supplier = "台灣中油"
  gasoline_92 = dom.xpath('/html/body/main/section[1]/div/div/div[2]/div[2]/div/div/div[1]/ul/li[1]/div[2]/strong')[0].text
  gasoline_95 = dom.xpath('/html/body/main/section[1]/div/div/div[2]/div[2]/div/div/div[1]/ul/li[2]/div[2]/strong')[0].text
  gasoline_98 = dom.xpath('/html/body/main/section[1]/div/div/div[2]/div[2]/div/div/div[1]/ul/li[3]/div[2]/strong')[0].text

  infoList.append({
    "supplier":supplier,
    "gasoline_92":gasoline_92,
    "gasoline_95":gasoline_95,
    "gasoline_98":gasoline_98
  })

  # 台塑價格
  supplier = "台塑石化"
  gasoline_92 = dom.xpath('/html/body/main/section[1]/div/div/div[2]/div[2]/div/div/div[2]/ul/li[1]/div[2]/strong')[0].text
  gasoline_95 = dom.xpath('/html/body/main/section[1]/div/div/div[2]/div[2]/div/div/div[2]/ul/li[2]/div[2]/strong')[0].text
  gasoline_98 = dom.xpath('/html/body/main/section[1]/div/div/div[2]/div[2]/div/div/div[2]/ul/li[3]/div[2]/strong')[0].text

  infoList.append({
    "supplier":supplier,
    "gasoline_92":gasoline_92,
    "gasoline_95":gasoline_95,
    "gasoline_98":gasoline_98
  })
  
  return infoList
