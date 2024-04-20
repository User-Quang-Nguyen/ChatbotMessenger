import psycopg2
import logging
import queue
from src.config import database
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    def __init__(self):
        self.host = database.get('host')
        self.port = database.get('port')
        self.db_name = database.get('db_name')
        self.user = database.get('user')
        self.password = database.get('password')
    
    def get_connection(self):
        try:
            conn = psycopg2.connect(database = self.db_name, user = self.user,
                                    password = self.password, host = self.host, port = self.port)
            return conn
        except Exception as e:
            logging.getLogger().info(f"[ERROR] connection refuse: {str(e)}")
    
    def addHistoryData(self, message_queue):
        conn = self.get_connection()
        cur = conn.cursor()
        try:
            while not message_queue.empty():
                message = message_queue.get()
                query = 'INSERT INTO history (senderid, message) VALUES (%s, %s)'
        
                cur.execute(query, (message["senderid"], message["content"]))
                conn.commit()
                message_queue.task_done()
                print("Tin nhắn đã được lưu vào cơ sở dữ liệu.")
            message_queue.join()
        except Exception as e:
            logging.getLogger().info(f"[ERROR] connection refuse: {str(e)}")
            return False
        finally:
            cur.close()
            conn.close()
    
    def addUserInfor(self, user_queue):
        conn = self.get_connection()
        cur = conn.cursor()
    
        try:
            while not user_queue.empty():
                formData = user_queue.get()
                query = 'INSERT INTO users (psid, firstname, lastname, avatar, gender, locale) VALUES (%s, %s, %s, %s, %s, %s)'
            
                cur.execute(query, (formData['id'], formData['first_name'], formData['last_name'], formData['profile_pic'], formData['gender'], formData['locale']))
                conn.commit()
                print("Người dùng đã được lưu vào cơ sở dữ liệu.")
                user_queue.task_done()
            user_queue.join()
        
        except Exception as e:
            logging.getLogger().info(f"[ERROR] connection refuse: {str(e)}")
            return False
        finally:
            cur.close()
            conn.close()
            
    def addBotInfor(self, bot_queue):
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            while not bot_queue.empty():
                formData = bot_queue.get()
                query = 'INSERT INTO bot (pageid, name, category) VALUES (%s, %s, %s)'
                cur.execute(query, (formData['id'], formData['name'], formData['category']))
                conn.commit()
                print("Bot đã được lưu vào cơ sở dữ liệu.")
                bot_queue.task_done()
            bot_queue.join()
            
        except Exception as e:
            print(e)
            return False
        finally:
            cur.close()
            conn.close()