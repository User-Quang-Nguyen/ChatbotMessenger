from src.repo.database import Database
import logging
import json

db = Database()

def insert_messages(messages):
    try:
        return db.insert_messages(messages)
    except Exception as e:
        logging.error(f"Failed to insert messages into database: {e}")
        return False

def add_user_infos(user_infos):
    try:
        return db.add_user_infor(user_infos)
    except Exception as e:
        logging.error(f"Failed to add user infos into database: {e}")
        return False
    
def add_bot_infos(bot_queue):
    try:
        return db.add_bot_info(bot_queue)
    except Exception as error:
        logging.error(f"Failed to add bot info into database: {error}")
        return False

def get_message_sender_ids_for_page(sender_id, recipient_id, page_id):
    try:
        results = db.get_message_sender_ids_for_page(sender_id, recipient_id, page_id)
        return [
            {
                "id": result[0],
                "sender_id": result[1],
                "message": result[2],
                "created_at": result[3],
                "recipient_id": result[4],
            }
            for result in results
        ]
    except Exception:
        return []
