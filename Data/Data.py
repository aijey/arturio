import psycopg2

class ParamsTable:
    def __init__(self, DATABASE_URL):
        self.DATABASE_URL = DATABASE_URL;
        self.init()
    def __del__(self):
        self.connection.close()
        print("Connection closed")
    def init(self):
        try:
            self.connection = psycopg2.connect(self.DATABASE_URL, sslmode='require')

            cursor = self.connection.cursor();

            commands = """ INSERT INTO PARAMS(var_name)
                           VALUES(%s);"""

            cursor.execute(commands, ('schedule_message_id',))
            self.connection.commit()
            cursor.close()
            print("Successful initialization of Params")
            self.connection.close()
        except (Exception, psycopg2.Error) as er:
            print(er)

    def getSchedule(self):
        try:
            cursor = self.connection.cursor();
            commands = """
            SELECT value
            FROM params
            WHERE var_name = 'schedule_message_id';
            """
            cursor.execute(commands)
            message_id = cursor.fetchall()[0]
            print("Got: schedule_message_id = " + message_id + " from params table")

            cursor.close()
            self.connection.close()
            return message_id
        except (Exception, psycopg2.Error) as er:
            print(er)
        return None

    def setSchedule(self,message_id):
        try:
            cursor = self.connection.cursor();

            commands = """ UPDATE PARAMS
                           SET value = %s
                           WHERE var_name = 'schedule_message_id'; """

            cursor.execute(commands, (message_id,))
            self.connection.commit()
            cursor.close()
            self.connection.close()
            print("Successfully saved")
        except (Exception, psycopg2.Error) as er:
            print(er)
