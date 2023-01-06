from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,
                            messages, LocationMessage, FlexSendMessage,
                            QuickReply, QuickReplyButton, LocationAction,
                            ImageSendMessage)

import configparser
from copy import deepcopy
import urllib.parse
# db Model
from oilModel import initConnection

# Service
from oilService import (updateRetailPriceService, selectRetailPriceService,
                        selectOilstInfoService, calcNearsetGasStationService)

# flexMessageTemplate
from flexMessageTemplate import flexMessageTemplate

app = Flask(__name__)

# 讀入設定檔
config = configparser.ConfigParser()
config.read('config.ini')

# mysql連線設定
mysql_configs = config["mysql"]
db_settings = {
    "host": mysql_configs["host"],
    "user": mysql_configs["user"],
    "password": mysql_configs["password"],
    "database": mysql_configs["database"],
    "port": int(mysql_configs["port"]),
    "charset": "utf8"
}

# 全部加油站資訊
OilstInfoTuple = None

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/callback", methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']
  body = request.get_data(as_text=True)
  app.logger.info("Request body: " + body)

  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    abort(400)

  return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handleTextMessage(event):
  content = event.message.text
  if "@油價查詢" in content:
    info = selectRetailPriceService()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=info))
  elif "@查詢附近的加油站" in content:
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="點選下方按鈕傳送位置",
            quick_reply=QuickReply(
                items=[QuickReplyButton(action=LocationAction(
                    label="傳送位置"))])))
  elif "@圖表" in content:
    line_bot_api.reply_message(event.reply_token, [
        ImageSendMessage(
            original_content_url=r"https://i.imgur.com/2GNbOrl.png",
            preview_image_url=r"https://i.imgur.com/2GNbOrl.png"),
        ImageSendMessage(
            original_content_url=r"https://i.imgur.com/29pW7lu.png",
            preview_image_url=r"https://i.imgur.com/29pW7lu.png")
    ])


@handler.add(MessageEvent, message=LocationMessage)
def handleLocationMessage(event):
  global OilstInfoTuple
  # 取得user經緯度資料
  locationInfo = {
      "latitude": event.message.latitude,
      "longitude": event.message.longitude
  }
  # 計算最近的三個加油站
  NearestGasStations = calcNearsetGasStationService(OilstInfoTuple,
                                                    locationInfo)
  print(NearestGasStations)
  FlexSendMessageList = []
  for NearestGasStation in NearestGasStations:
    fullAddr = NearestGasStation["counties"] + NearestGasStation[
        "district"] + NearestGasStation["addr"]
    # 站名
    flexMessageTemplate["body"]["contents"][0]["text"] = NearestGasStation[
        "name"]
    # 地址
    flexMessageTemplate["body"]["contents"][1]["contents"][0]["contents"][0][
        "text"] = fullAddr
    # uri
    query = urllib.parse.quote(fullAddr.encode('utf8'))
    flexMessageTemplate["footer"]["contents"][0]["action"]["uri"] = "https://www.google.com/maps?q=" + query

    FlexSendMessageList.append(
        FlexSendMessage(alt_text="附近的加油站",
                        contents=deepcopy(flexMessageTemplate)))

  line_bot_api.reply_message(event.reply_token, FlexSendMessageList)


if __name__ == '__main__':
  initConnection(db_settings)
  # 運行server就讀入所有加油站資料
  OilstInfoTuple = selectOilstInfoService()
  app.run(port=8000, debug=True)
