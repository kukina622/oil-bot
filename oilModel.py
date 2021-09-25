import pymysql

db = None


def initConnection(db_settings):
  global db
  db = pymysql.connect(**db_settings, autocommit=True)


def updateRetailPrice(retailPrice,priceChange):
  with db.cursor() as cursor:
    cursor.execute("DELETE FROM `domestic_retail_price`")
    sql = '''INSERT INTO `domestic_retail_price` (supplier,gasoline_98,gasoline_95,gasoline_92,diesel_oil,sales_unit,date,expected) 
    values (%s,%s,%s,%s,%s,%s,%s,%s);'''
    updateData = [list(eachData.values())
                  for eachData in retailPrice]  #整理成可被update的格式
    updateData[0].append(priceChange)
    updateData[1].append(priceChange)
    cursor.executemany(sql, updateData)

def selectRetailPrice():
  with db.cursor() as cursor:
    sql="SELECT * FROM `domestic_retail_price`"
    cursor.execute(sql)
    return cursor.fetchall()

def selectOilst():
  with db.cursor() as cursor:
    sql="SELECT * FROM `Oilst`"
    cursor.execute(sql)
    return cursor.fetchall()