from src.handler import processor as generator_message
from src.service import call_facebook_api as fb_api
from src.service import queue as queue_handler
from src.handler import GPT
import threading
import queue

message_queue = queue.Queue()
user_queue = queue.Queue()
bot_queue = queue.Queue()

def handleSendMessage(senderPsid, pagePsid, response):
    fb_api.reply(senderPsid, pagePsid, response)
        
def handleMessage(senderPsid, pagePsid, receiveMessage):
    if 'text' in receiveMessage:
        thequestion = receiveMessage['text']
        try:
            txt = GPT.chatbot_response(thequestion)
        except:
            txt = generator_message.chatbot_response(thequestion)
        response = {
            "text": txt
        }
        
        user_thread = threading.Thread(target = handleSendMessage, args=(senderPsid, pagePsid, response))
        user_thread.daemon = True
        user_thread.start()
        
        Db_thread = threading.Thread(target = queue_handler.handleSaveToDb, args=(senderPsid, receiveMessage, pagePsid, response, message_queue, user_queue, bot_queue))
        Db_thread.start()
        
        return "oke", 200
    else:
        response = {
            "text": 'This chatbot only accecpts text message'
        }
        fb_api.reply(senderPsid, pagePsid, response)