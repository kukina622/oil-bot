from crawler.retailPriceCrawler import retailPriceCrawler
from crawler.priceChangeCrawler import priceChangeCrawler

from oilMongoModel import deleteRetailPrice, updateRetailPrice, selectRetailPrice, selectOilst

from utils import getDistance

from copy import deepcopy

def updateRetailPriceService():
  retailPriceList = retailPriceCrawler()
  priceChange = priceChangeCrawler()
  deleteRetailPrice()
  updateRetailPrice(retailPriceList, priceChange)


def selectRetailPriceService():
  info = ""
  retailPrice = selectRetailPrice()
  priceChange = retailPrice[0]["expected"]
  for data in retailPrice:
    info += f"{data['supplier']}\n98油價:{data['gasoline_98']}\n95油價:{data['gasoline_95']}\n92油價:{data['gasoline_92']}\n\n"
  info += f"預計{priceChange}"
  return info


def selectOilstInfoService():
  return selectOilst()


def calcNearsetGasStationService(OilstInfoTuple, nowLocation):
  infoOfCalculationList = []
  infoOfCalculation = {
      "name": "",
      "counties": "",
      "district": "",
      "addr": "",
      "distance": 0
  }
  for GasStation in OilstInfoTuple:
    infoOfCalculation["name"] = GasStation['站名']
    infoOfCalculation["counties"] = GasStation['縣市'].strip()
    infoOfCalculation["district"] = GasStation['鄉鎮區'].strip()
    infoOfCalculation["addr"] = GasStation['地址'].strip()
    infoOfCalculation["distance"] = getDistance(
        float(nowLocation["latitude"]),
        float(nowLocation["longitude"]),
        GasStation['緯度'],
        GasStation['經度'],
    )
    infoOfCalculationList.append(deepcopy(infoOfCalculation))
  infoOfCalculationList.sort(key=lambda x:x["distance"])
  return infoOfCalculationList[:3:]