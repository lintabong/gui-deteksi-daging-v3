import sqlite3
from datetime import datetime


class Database():
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor     = self.connection.cursor()

        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        
        tableList = [x[0] for x in self.cursor]

        for table in tableList:
            print(table)
        
        if "data" not in tableList:
            self.cursor.execute('''CREATE TABLE data (
                id int AUTO_INCREMENT,
                name varchar(255),
                datetime varchar(255),
                phone_number varchar(255),
                type varchar(255),
                PRIMARY KEY (id)
            );''')

db = Database()