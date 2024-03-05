from datetime import datetime
from sqlalchemy import create_engine

class Database:
    def __init__(self, db_name: str, username: str, password: str, host: str, port: int):
        self.db_name = db_name
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def get_connection_string(self):
        return f'sqlite:///{self.db_name}.db'


class Connector:
    def __init__(self, database: Database):
        self.database = database
        self.engine = None
        self.connection_history = []

    def connect(self):
        try:
            connection_string = self.database.get_connection_string()
            self.engine = create_engine(connection_string)
            self.connection_history.append({"db": self.database.db_name, "time_connected": datetime.now()})
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def get_connection(self):
        if self.engine:
            return self.engine.connect()
        else:
            raise RuntimeError("Connection has not been established.")

    def disconnect(self):
        if self.engine:
            self.engine.dispose() 
            self.engine = None

    def __del__(self):
        self.disconnect()



