

class DBCursor:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = self.connection.cursor(buffered=True)
    
    def close(self):

        self.connection.close()