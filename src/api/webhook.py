import flask
import json
from flask import request
from src.handler import message as handler_message
from src import config

app = flask.Blueprint("api_webhook", __name__)

@app.route('/webhook', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        VERIFY_TOKEN = config.VERIFY_TOKEN
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            
        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("WEBHOOK VERIFIED")
                
                challenge = request.args.get("hub.challenge")
                
                return challenge, 200
            else:
                return 'ERROR', 403
        return "NOTHING", 200
    
    if request.method == 'POST':
        VERIFY_TOKEN = config.VERIFY_TOKEN
        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            
        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("WEBHOOK VERIFIED")
                
                challenge = request.args.get("hub.challenge")
                
                return challenge, 200
            else:
                return 'ERROR', 403
        
        data = request.data
        body = json.loads(data.decode('utf-8'))
        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                
                senderPsid = webhookEvent['sender']['id']
                pagePsid = webhookEvent['recipient']['id']
                time = webhookEvent['timestamp']
                
                if 'message' in webhookEvent:
                    handler_message.handleMessage(senderPsid, pagePsid, webhookEvent['message'], time)
                
                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404