import requests
from bs4 import BeautifulSoup
import copy
import re
from decimal import Decimal

datePattern = '^[0-9]{4}/[0-9]{2}/[0-9]{2}|[0-9]{1}'
url = r"https://www2.moeaboe.gov.tw/oil102/oil2017/A01/A0108/tablesprices.asp"


def retailPriceCrawler():
  res = requests.get(url)
  res.encoding = 'big5-hkscs'
  soup = BeautifulSoup(res.text, "html.parser")
  infoAry = []
  suppliers = []
  infoDict = {
      "supplier": "",
      "gasoline_98": "",
      "gasoline_95": "",
      "gasoline_92": "",
      "diesel_oil": "",
      "sales_unit": "",
      "date": ""
  }
  dataTable = soup.find_all("table")[1].find_all("tr")[1:4:]
  for row in dataTable:
    count = 0
    for cell in row.find_all("td"):
      if count == 6:  #對日期做處理
        infoDict[list(infoDict.keys())[count]] = re.match(
            datePattern, cell.text).group().replace("/", "-")  #濾出符合pattern的字段
      elif count >= 1 and count <= 4:
        infoDict[list(infoDict.keys())[count]] = Decimal(cell.text)
      else:
        infoDict[list(infoDict.keys())[count]] = cell.text
      count += 1

    # 不要把重複加入
    if infoDict["supplier"] not in suppliers:
      infoAry.append(copy.deepcopy(infoDict))
      suppliers.append(infoDict["supplier"])

  return infoAry
