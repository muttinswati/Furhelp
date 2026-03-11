import pymysql
import os

def get_db_connection():
    sqlkey = os.environ.get("sqlpassword")  # your MySQL password from environment
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password=sqlkey,
        database="furhelp"
    )

    # # Test: show tables
    # sqlcursor = mydb.cursor()
    # sqlcursor.execute("SHOW TABLES")
    # print("Tables in furhelp database:")
    # for table in sqlcursor.fetchall():
    #     print(table)

    return mydb

