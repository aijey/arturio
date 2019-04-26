import psycopg2
class DataBase:
    def __init__(self, DATABASE_URL):
        self.DATABASE_URL = DATABASE_URL;
        self.connection = None
        self.connect()
    def __del__(self):
        self.connection.close()
        print("Connection closed")
    def connect(self):
        try:
            self.connection = psycopg2.connect(self.DATABASE_URL, sslmode = 'require')
            print("Connected to db")
            return True
        except(Exception, psycopg2.Error) as er:
            print(er)
        print("gg")
        return False
    def reconnect(self):
        self.connection.close()
        self.connect()
class ParamsTable(DataBase):
    def __init__(self,dataBase):
        self.dataBase = dataBase
        try:
            cursor = self.dataBase.connection.cursor();

            commands = """ INSERT INTO PARAMS(var_name)
                           VALUES(%s);"""

            cursor.execute(commands, ('schedule_message_id',))
            self.dataBase.connection.commit()
            cursor.close()
            print("Successful initialization of Params")
        except (Exception, psycopg2.Error) as er:
            self.dataBase.connection.close()
            self.dataBase.connect()
            print(er)

    def getSchedule(self):
        try:
            cursor = self.dataBase.connection.cursor();
            commands = """
            SELECT value
            FROM params
            WHERE var_name = 'schedule_message_id';
            """
            cursor.execute(commands)
            data = cursor.fetchone()[0]
            print("Got: schedule_message_id = " + str(data[1]) + " chat_id = " + str(data[0]) + " from params table")

            cursor.close()
            return data
        except (Exception, psycopg2.Error) as er:
            self.dataBase.connection.close()
            self.dataBase.connect()
            print(er)
        return None

    def setSchedule(self,message):
        try:
            cursor = self.dataBase.connection.cursor();

            commands = """ UPDATE PARAMS
                           SET value = %s
                           WHERE var_name = 'schedule_message_id'; """
            data = [message.chat.id,message.message_id]
            cursor.execute(commands, (data,))
            self.dataBase.connection.commit()
            cursor.close()
            print("Successfully saved")
        except (Exception, psycopg2.Error) as er:
            self.dataBase.connection.close()
            self.dataBase.connect()
            print(er)
class UselessMessagesTable(DataBase):
    def __init__(self, dataBase):
        self.dataBase = dataBase
    def addMessage(self,message):
        try:
            cursor = self.dataBase.connection.cursor()
            commands = """
            INSERT INTO UselessMessages(message_id,chat_id)
            VALUES(%s,%s);
            """
            cursor.execute(commands,(message.message_id,message.chat.id,))
            self.dataBase.connection.commit()
            cursor.close()
            print("Message " + str(message.message_id) + " from chat: " + str(message.chat.id) + " added to DB")
        except (Exception, psycopg2.Error) as er:
            self.dataBase.connection.close()
            self.dataBase.connect()
            print(er)
    def removeMessage(self,message):
        try:
            cursor = self.dataBase.connection.cursor()
            commands = """
            DELETE FROM UselessMessages
            WHERE message_id = %s AND chat_id = %s
            """
            cursor.execute(commands,(message.message_id,message.chat.id,))
            self.dataBase.connection.commit()
            cursor.close()
            print("Deleted message_id = " + str(message.message_id) + " chat_id = " + str(message.chat.id))
        except (Exception, psycopg2.Error) as er:
            self.dataBase.reconnect()
            print(er)
    def clearMessages(self,chat_id):
        try:
            cursor = self.dataBase.connection.cursor()
            commands = """
            DELETE From UselessMessages
            WHERE chat_id = %s
            """
            cursor.execute(commands,(chat_id,))
            self.dataBase.connection.commit()
            cursor.close()
            print("Deleted useless messages from " + str(chat_id))
        except(Exception, psycopg2.Error) as er:
            self.reconnect()
            print(er)

    def getMessages(self, chat_id):
        try:
            cursor = self.dataBase.connection.cursor()
            commands = """
            SELECT message_id
            FROM UselessMessages
            WHERE chat_id = %s
            """

            cursor.execute(commands,(chat_id,))
            data = cursor.fetchall()
            print("GOT: ")
            messages = []
            for i in data:
                messages.append(i[0])
            print(messages)
            cursor.close()
            return messages
        except(Exception, psycopg2.Error) as er:
            self.dataBase.connection.close()
            self.dataBase.connect()
            print(er)
        return None
