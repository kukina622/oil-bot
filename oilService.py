from crawler.retailPriceCrawler import retailPriceCrawler
from crawler.priceChangeCrawler import priceChangeCrawler

from oilModel import updateRetailPrice, selectRetailPrice, selectOilst

from utils import getDistance

from copy import deepcopy

def updateRetailPriceService():
  retailPriceList = retailPriceCrawler()
  priceChange = priceChangeCrawler()
  updateRetailPrice(retailPriceList, priceChange)


def selectRetailPriceService():
  info = ""
  retailPrice = selectRetailPrice()
  priceChange = retailPrice[0][7]
  for data in retailPrice:
    info += f"{data[0]}\n98油價:{data[1]}\n95油價:{data[2]}\n92油價:{data[3]}\n超(高)級柴油:{data[4]}\n施行日期:{data[6]}\n\n"
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
    infoOfCalculation["name"] = GasStation[0]
    infoOfCalculation["counties"] = GasStation[1].strip()
    infoOfCalculation["district"] = GasStation[2].strip()
    infoOfCalculation["addr"] = GasStation[3].strip()
    infoOfCalculation["distance"] = getDistance(
        float(nowLocation["latitude"]),
        float(nowLocation["longitude"]),
        float(GasStation[5]),
        float(GasStation[4]),
    )
    infoOfCalculationList.append(deepcopy(infoOfCalculation))
  infoOfCalculationList.sort(key=lambda x:x["distance"])
  return infoOfCalculationList[:3:]