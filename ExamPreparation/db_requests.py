from db_connection import connect_to_db, exec_query

def get_hospital():
    connection = connect_to_db()
    if not connection:
        return []

    query = "SELECT * FROM hospitalizations"
    result = exec_query(connection, query)
    connection.close()
    return result

def add_hospital(data):
    connection = connect_to_db()
    if connection:
        query = """
        INSERT INTO hospitalizations (full_name, passport_data) VALUES (%(full_name)s, %(passport_data)s)"""
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()