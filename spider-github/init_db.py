import sqlite3
from sqlite3 import Error

class InitDb :
    def create_db_and_table(self):
        conn = sqlite3.connect('spider-github.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE REPOSITORIES
                    (id INT PRIMARY KEY     NOT NULL,
                    name           char(50)    NOT NULL,
                    star           INT     NOT NULL,
                    link           CHAR(250) NOT NULL,
                    description    CHAR(250),
                    language       ChAR(50));''')
        print("Table created successfully")
        conn.commit()
        conn.close()

    def init(self):
        # self.create_database()
        self.create_db_and_table()

init_db = InitDb()
init_db.init()