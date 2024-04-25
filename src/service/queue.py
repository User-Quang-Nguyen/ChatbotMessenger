from src.service import call_facebook_api as fb_api
from src.service import database
from datetime import datetime

def handleSaveToDb(senderPsid, receiveMmessage, pagePsid, response, message_queue, user_queue, bot_queue, time):
    current_time = int(datetime.now().timestamp())*1000
    
    message_req = {"senderid": senderPsid, "receiveid": pagePsid, "content": receiveMmessage['text'], "time": time}
    message_res = {"senderid": pagePsid, "receiveid": senderPsid, "content": response['text'], "time": current_time}
    message_queue.put(message_req)
    message_queue.put(message_res)
    
    print("Tin nhắn đã được lưu vào trong hàng đợi.")
    if message_queue.qsize() >= 6:
        database.addHistoryData(message_queue)
        
    user = fb_api.getUserInfor(senderPsid)
    user_queue.put(user)
    print("Người dùng đã được lưu vào trong hàng đợi.")
    if user_queue.qsize() >= 3:
        database.addUserInfors(user_queue)
        
    bot = fb_api.getBotInfor(pagePsid)
    bot_queue.put(bot)
    print("Bot đã được lưu vào trong hàng đợi.")
    if bot_queue.qsize() >= 3:
        database.addBotInfors(bot_queue)