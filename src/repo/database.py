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
                is_exist = self.check_exist_user(formData["id"])
                print(is_exist)
                if is_exist:
                    print("User existed")
                    user_queue.task_done()
                    continue
                
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
                is_exist = self.check_exist_bot(formData["id"])
                if is_exist:
                    print("Bot existed")
                    bot_queue.task_done()
                    continue
                
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
            
    def check_exist_user(self, id):
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            query = 'SELECT EXISTS (SELECT 1 FROM users WHERE psid = %s)'
            cur.execute(query, (id,))
            result = cur.fetchone()[0]
            conn.commit()
            return result
        except Exception as e:
            print(str(e))
            return False
        finally:
            cur.close()
            conn.close()
    
    def check_exist_bot(self, id):
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            query = 'SELECT EXISTS (SELECT 1 FROM bot WHERE pageid = %s)'
            cur.execute(query, (id,))
            result = cur.fetchone()[0]
            conn.commit()
            return result
        except Exception as e:
            print(str(e))
            return False
        finally:
            cur.close()
            conn.close()