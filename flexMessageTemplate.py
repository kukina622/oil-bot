flexMessageTemplate = {
    "type": "bubble",
    "body": {
        "type":
        "box",
        "layout":
        "vertical",
        "contents": [
        {
            "type": "text",
            "text": "Brown Cafe",
            "weight": "bold",
            "size": "xl"
        }, 
        {
            "type":
            "box",
            "layout":
            "vertical",
            "margin":
            "lg",
            "spacing":
            "sm",
            "contents": [{
                "type":"box",
                "layout":"baseline",
                "spacing":"sm",
                "contents": [{
                    "type": "text",
                    "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5
                }]
            }]
        }]
    },
    "footer": {
        "type":"box",
        "layout":"vertical",
        "spacing":"sm",
        "contents": [
            {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                    "type": "uri",
                    "label": "查看",
                    "uri": "http://linecorp.com/"
                },
            },
        ],
    }
}