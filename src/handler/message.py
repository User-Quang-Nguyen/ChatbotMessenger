from src.handler import processor as generator_message
from src.service import call_facebook_api as fb_api
from src.service import queue as queue_handler
from src.service import database
from src.handler import pre_process
from src.handler import GPT
import threading
import queue

message_queue = queue.Queue()
user_queue = queue.Queue()
bot_queue = queue.Queue()

def handleSendMessage(senderPsid, pagePsid, response):
    fb_api.reply(senderPsid, pagePsid, response)
        
def handleMessage(senderPsid, pagePsid, receiveMessage, time):
    if 'text' in receiveMessage:
        thequestion = receiveMessage['text']
        
        is_suitable = pre_process.check_text(thequestion)
        if not is_suitable:
            txt = "Sorry, you used an invalid keyword"
            response = {
                "text": txt
            }
        else:
            try:
                txt = GPT.AI(thequestion)
            except:
                txt = generator_message.chatbot_response(thequestion)
                txt = "You send:" + receiveMessage['text']
            response = {
                "text": txt
            }
        
        user_thread = threading.Thread(target = handleSendMessage, args=(senderPsid, pagePsid, response))
        user_thread.daemon = True
        user_thread.start()
        
        Db_thread = threading.Thread(target = queue_handler.handleSaveToDb, args=(senderPsid, receiveMessage, pagePsid, response, message_queue, user_queue, bot_queue, time))
        Db_thread.start()
        
        user_thread.join()
        Db_thread.join()
        return "oke", 200
    else:
        response = {
            "text": 'This chatbot only accecpts text message'
        }
        user_thread = threading.Thread(target = handleSendMessage, args=(senderPsid, pagePsid, response))
        user_thread.daemon = True
        user_thread.start()
        
        Db_thread = threading.Thread(target = queue_handler.handleSaveToDb, args=(senderPsid, receiveMessage, pagePsid, response, message_queue, user_queue, bot_queue, time))
        Db_thread.start()
        return "oke", 200
    
def getMessage(senderid, receiveid, page):
    result = database.getMessageSenderIdForPageid(senderid, receiveid, page)
    return result