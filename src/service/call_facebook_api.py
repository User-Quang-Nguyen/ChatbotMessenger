from src import config
import requests

def fetch_user_info(user_id):
    access_token = config.PAGE_ACCESS_TOKEN
    fields = "id,first_name,last_name,profile_pic,gender,locale"

    url = f"https://graph.facebook.com/{user_id}?fields={fields}&access_token={access_token}"
    response = requests.get(url)

    if response.status_code == 200:
        user_data = response.json()
        return user_data
    return None
    
def get_bot_info(page_id):
    access_token = config.PAGE_ACCESS_TOKEN
    fields = "name,category"
    
    url = f"https://graph.facebook.com/{page_id}?fields={fields}&access_token={access_token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        bot_data = response.json()
        return bot_data
    
    return None

    
def send_message(sender_id, page_id, message):
    access_token = config.PAGE_ACCESS_TOKEN
    payload = {
        "recipient": {
            "id": sender_id
        },
        "message": message
    }
    headers = {'content-type': 'application/json'}
    url = f"https://graph.facebook.com/v14.0/me/messages?access_token={access_token}"
    response = requests.post(url, json=payload, headers=headers)
    return "ok", response.status_code