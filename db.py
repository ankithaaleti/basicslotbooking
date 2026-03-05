import mysql.connector
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@123",
        database="mysql"
    )

