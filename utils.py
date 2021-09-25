import math

# 計算距離
def getDistance(latA, lonA, latB, lonB):
  ra = 6378140  # 赤道半徑
  rb = 6356755  # 極半徑
  flatten = (ra - rb) / ra  # Partial rate of the earth
  # change angle to radians
  radLatA = math.radians(latA)
  radLonA = math.radians(lonA)
  radLatB = math.radians(latB)
  radLonB = math.radians(lonB)

  pA = math.atan(rb / ra * math.tan(radLatA))
  pB = math.atan(rb / ra * math.tan(radLatB))
  x = math.acos(
      math.sin(pA) * math.sin(pB) +
      math.cos(pA) * math.cos(pB) * math.cos(radLonA - radLonB))
  c1 = (math.sin(x) - x) * (math.sin(pA) + math.sin(pB))**2 / math.cos(
      x / 2)**2
  c2 = (math.sin(x) + x) * (math.sin(pA) - math.sin(pB))**2 / math.sin(
      x / 2)**2
  dr = flatten / 8 * (c1 - c2)
  distance = ra * (x + dr)
  distance = round(distance / 1000, 4)
  return distance
