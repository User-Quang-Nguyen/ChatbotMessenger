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

def send_message(sender_id, page_id, response):
    fb_api.send_message(sender_id, page_id, message = response)
        
def handle_message(sender_id, page_id, message, timestamp):
    if 'text' not in message:
        response = {"text": 'This chatbot only accepts text messages'}
    else:
        question = message['text']
        if not pre_process.is_text_valid(question):
            response = {"text": "Sorry, you used an invalid keyword"}
        else:
            try:
                answer = GPT.AI(question)
            except:
                answer = generator_message.chatbot_response(question)
            response = {"text": answer}
            
    user_thread = threading.Thread(target=send_message, args=(sender_id, page_id, response))
    user_thread.daemon = True
    user_thread.start()

    db_thread = threading.Thread(target=queue_handler.save_to_db, args=(sender_id, message, page_id, response, message_queue, user_queue, bot_queue, timestamp))
    db_thread.start()

    user_thread.join()
    db_thread.join()

    return "ok", 200
    
def get_messages_for_page(sender_id, page_id, page_num):
    """
    Get messages for a specific page.
    
    Args:
        sender_id (int): The id of the sender.
        page_id (int): The id of the page.
        page_num (int): The page number.
        
    Returns:
        list: The list of messages.
    """
    messages = database.get_message_sender_ids_for_page(sender_id, page_id, page_num)
    return messages
