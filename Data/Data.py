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
            return False
class ParamsTable(DataBase):
    def __init__(self):
        try:
            cursor = super().connection.cursor();

            commands = """ INSERT INTO PARAMS(var_name)
                           VALUES(%s);"""

            cursor.execute(commands, ('schedule_message_id',))
            super().connection.commit()
            cursor.close()
            print("Successful initialization of Params")
        except (Exception, psycopg2.Error) as er:
            super().connection.close()
            super().connect()
            print(er)

    def getSchedule(self):
        try:
            cursor = super().connection.cursor();
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
            print(er)
        return None

    def setSchedule(self,message_id):
        try:
            cursor = super().connection.cursor();

            commands = """ UPDATE PARAMS
                           SET value = %s
                           WHERE var_name = 'schedule_message_id'; """

            cursor.execute(commands, (message_id,))
            super().connection.commit()
            cursor.close()
            print("Successfully saved")
        except (Exception, psycopg2.Error) as er:
            print(er)
class UselessMessagesTable(DataBase):
    def addMessage(message):
        try:
            cursor = super().connection.cursor()
            commands = """
            INSERT INTO UselessMessages(message_id,chat_id)
            VALUES(%s,%s);
            """
            cursor.execute(commands,(message.message_id,message.chat.id,))
            cursor.commit()
            cursor.close()
        except (Exception, psycopg2.Error) as er:
            print(er)
