from src.handler import processor as generator_message
from src.handler import database
from src.handler import call_facebook_api as fb_api
import json
import threading
import queue

message_queue = queue.Queue()
user_queue = queue.Queue()
bot_queue = queue.Queue()

def handleSendMessage(senderPsid, pagePsid, response):
    fb_api.reply(senderPsid, pagePsid, response)
    
def handleSaveToDb(senderPsid, receiveMmessage, pagePsid, response):
    message_req = {"senderid": senderPsid, "content": receiveMmessage['text']}
    message_res = {"senderid": pagePsid, "content": response['text']}
    message_queue.put(message_req)
    message_queue.put(message_res)
    print("Tin nhắn đã được lưu vào trong hàng đợi.")
    if message_queue.qsize() >= 10:
        database.addHistoryData(message_queue)
        
    user = fb_api.getUserInfor(senderPsid)
    user_queue.put(user)
    print("Người dùng đã được lưu vào trong hàng đợi.")
    if user_queue.qsize() >= 1:
        database.addUserInfors(user_queue)
        
    bot = fb_api.getBotInfor(pagePsid)
    bot_queue.put(bot)
    print("Bot đã được lưu vào trong hàng đợi.")
    if bot_queue.qsize() >= 1:
        database.addBotInfors(bot_queue)

        
def handleMessage(senderPsid, pagePsid, receiveMessage):
    if 'text' in receiveMessage:
        thequestion = receiveMessage['text']
        
        txt = generator_message.chatbot_response(thequestion)
        response = {
            "text": txt
        }
        
        user_thread = threading.Thread(target = handleSendMessage, args=(senderPsid, pagePsid, response))
        user_thread.daemon = True
        user_thread.start()
        
        Db_thread = threading.Thread(target = handleSaveToDb, args=(senderPsid, receiveMessage, pagePsid, response))
        Db_thread.start()
        
        return "oke", 200
    else:
        response = {
            "text": 'This chatbot only accecpts text message'
        }
        fb_api.reply(senderPsid, pagePsid, response)