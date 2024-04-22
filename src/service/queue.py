from src.service import call_facebook_api as fb_api
from src.service import database

def handleSendMessage(senderPsid, pagePsid, response):
    fb_api.reply(senderPsid, pagePsid, response)
    
def handleSaveToDb(senderPsid, receiveMmessage, pagePsid, response, message_queue, user_queue, bot_queue):
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
    if user_queue.qsize() >= 5:
        database.addUserInfors(user_queue)
        
    bot = fb_api.getBotInfor(pagePsid)
    bot_queue.put(bot)
    print("Bot đã được lưu vào trong hàng đợi.")
    if bot_queue.qsize() >= 5:
        database.addBotInfors(bot_queue)