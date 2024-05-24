import flask
import json
from flask import request
from src.handler import message as handler_message
from src import config

app = flask.Blueprint("api_webhook", __name__)

def handle_page_events(request):
    body = json.loads(request.data.decode('utf-8'))
    if 'object' in body and body['object'] == 'page':
        for entry in body['entry']:
            webhookEvent = entry['messaging'][0]
            
            sender_id = webhookEvent['sender']['id']
            recipient_id = webhookEvent['recipient']['id']
            time = webhookEvent['timestamp']
            
            if 'message' in webhookEvent:
                handler_message.handle_message(sender_id, page_id = recipient_id, message = webhookEvent['message'],timestamp = time)
            return "EVENT_RECEIVED", 200
    else: 
        return 'ERROR', 403

def verify_webhook(request):
    verify_token = config.VERIFY_TOKEN
    if 'hub.mode' in request.args:
        mode = request.args.get('hub.mode')
        print(mode)
    if 'hub.verify_token' in request.args:
        token = request.args.get('hub.verify_token')
        print(token)
    if 'hub.challenge' in request.args:
        challenge = request.args.get('hub.challenge')
        print(challenge)
        
    if 'hub.mode' in request.args and 'hub.verify_token' in request.args:        
        if mode == 'subscribe' and token == verify_token:
            print("WEBHOOK VERIFIED")
            challenge = request.args.get("hub.challenge")
                    
            return challenge, 200
        else:
            return 'ERROR', 403

@app.route('/webhook', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        verify_webhook(request)
        return handle_page_events(request)
