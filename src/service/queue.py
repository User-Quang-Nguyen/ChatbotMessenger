from src.service import call_facebook_api as fb_api
from src.service import database
from datetime import datetime

def save_to_db(
        sender_id, received_message, page_id, 
        response, message_queue, user_queue, 
        bot_queue, time):
    current_time = int(datetime.now().timestamp()) * 1000

    request_message = {
        "sender_id": sender_id, 
        "receive_id": page_id, 
        "content": received_message['text'], 
        "time": time
    }
    response_message = {
        "sender_id": page_id, 
        "receive_id": sender_id, 
        "content": response['text'], 
        "time": current_time
    }
    message_queue.put(request_message)
    message_queue.put(response_message)

    if message_queue.qsize() >= 6:
        database.insert_messages(message_queue)
        print("Đã lưu tin nhắn")
    
    user = fb_api.fetch_user_info(sender_id)
    user_queue.put(user)
    if user_queue.qsize() >= 3:
        database.add_user_infos(user_queue)
        
    bot = fb_api.get_bot_info(page_id)
    bot_queue.put(bot)
    if bot_queue.qsize() >= 3:
        database.add_bot_infos(bot_queue)