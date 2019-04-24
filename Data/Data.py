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
            message_id = cursor.fetchone()[0]
            print("Got: schedule_message_id = " + message_id + " from params table")

            cursor.close()
            return message_id
        except (Exception, psycopg2.Error) as er:
            self.dataBase.connection.close()
            self.dataBase.connect()
            print(er)
        return None

    def setSchedule(self,message_id):
        try:
            cursor = self.dataBase.connection.cursor();

            commands = """ UPDATE PARAMS
                           SET value = %s
                           WHERE var_name = 'schedule_message_id'; """

            cursor.execute(commands, (message_id,))
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
            print("Message " + message.message_id + " from chat: " + message.chat.id + " added to DB")
        except (Exception, psycopg2.Error) as er:
            self.dataBase.connection.close()
            self.dataBase.connect()
            print(er)
