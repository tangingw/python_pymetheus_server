

class DBCursor:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = self.connection.cursor()
    
    def close(self):

        self.connection.close()