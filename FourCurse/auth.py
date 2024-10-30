from db_connection import connect_to_db, execute_query
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email, birth, gender, role):
    connection = connect_to_db()
    if connection:
        hashed_password = hash_password(password)
        query = """
        INSERT INTO users (Username, Password, Email, Birth, gender, Role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor = connection.cursor()
        cursor.execute(query, (username, hashed_password, email, birth, gender, role))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    return False

def authenticate_user(username, password):
    connection = connect_to_db()
    if connection:
        hashed_password = hash_password(password)
        query = "SELECT * FROM users WHERE Username = %s AND Password = %s"
        cursor = connection.cursor()
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user is not None
    return False