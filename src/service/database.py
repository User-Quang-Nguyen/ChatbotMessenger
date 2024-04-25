from src.repo.database import Database
import logging
import json

db = Database()

def addHistoryData(message_queue):
    try:
        result = db.addHistoryData(message_queue)
        return result
    except Exception as e:
        logging.getLogger.infor(f"[ERROR] insert data from database: {str(e)}")
        return False

def addUserInfors(user_queue):
    try:
        result = db.addUserInfor(user_queue)
        return result
    except Exception as e:
        logging.getLogger.infor(f"[ERROR] insert data from database: {str(e)}")
        return False
    
def addBotInfors(bot_queue):
    try:
        result = db.addBotInfor(bot_queue)
        return result
    except Exception as e:
        logging.getLogger.infor(f"[ERROR] insert data from database: {str(e)}")
        return False

def getMessageSenderIdForPageid(senderid, receiveid, page):
    try:
        result = []
        results = db.getMessageSenderIdForPageid(senderid, receiveid, page)
        for item in results:
            item_dict = {
                "id": item[0],
                "senderid": item[1],
                "message": item[2],
                "createdat": item[3],
                "receiveid": item[4]
            }
            result.append(item_dict)
        return result
    except Exception as e:
        print(str(e))
        return False