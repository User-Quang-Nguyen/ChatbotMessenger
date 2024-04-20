from src import config
import requests

def getUserInfor(psid):
    PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN
    fields = "id,first_name,last_name,profile_pic,gender,locale"

    url = "https://graph.facebook.com/{}?fields={}&access_token={}".format(psid, fields, PAGE_ACCESS_TOKEN)
    result = requests.get(url)
    if result.status_code == 200:
        userData = result.json()
        return userData
    else:
        return None
    
def getBotInfor(pageid):
    PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN
    fields = "name,category"
    
    url = "https://graph.facebook.com/{}?fields={}&access_token={}".format(pageid, fields, PAGE_ACCESS_TOKEN)
    result = requests.get(url)
    if result.status_code == 200:
        botData = result.json()
        return botData
    else:
        return None

    
def reply(senderPsid, pagePsid, response):
    PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN
    
    payload = {
        "recipient": {
            "id": senderPsid
        },
        "message": response
    }
    
    headers = {'content-type': 'application/json'}
    
    url = "https://graph.facebook.com/v14.0/me/messages?access_token={}".format(PAGE_ACCESS_TOKEN)
    r = requests.post(url = url, json=payload, headers=headers)
    return "oke", 200