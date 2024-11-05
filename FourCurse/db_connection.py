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

def execute_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result