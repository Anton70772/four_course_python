import mysql.connector

def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="234565",
            database="clinika"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def exec_query(connection, query):
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        return cursor.fetchall()