import pymongo

db = None

def initConnection(db_settings):
  """連接資料庫"""
  global db
  user = db_settings["user"]
  password = db_settings["password"]
  host = db_settings["host"]

  client = pymongo.MongoClient(f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority")
  db = client["oilBot"]

def updateRetailPrice(retailPrice,priceChange):
  """更新零售價格"""
  collection = db["domestic_retail_price"]  
  retailPrice[0]["expected"] = priceChange
  retailPrice[1]["expected"] = priceChange
  collection.insert_many(retailPrice)

def deleteRetailPrice():
  """刪除所有近期零售價格"""
  collection = db["domestic_retail_price"]
  collection.delete_many({})

def selectRetailPrice():
  """查詢所有近期零售價格"""
  collection = db["domestic_retail_price"]
  return collection.find({})

def selectOilst():
  """查詢所有加油站資料"""
  collection = db["Oilst"]
  return collection.find({})