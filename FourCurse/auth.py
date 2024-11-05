import mysql.connector
from mysql.connector import Error
import bcrypt

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="234565",
            database="clinika"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Ошибка подключения к базе данных", e)
    return None

def register_user(username, password, email, birth, gender, role="user"):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            query = """
            INSERT INTO users (Username, Password, Email, Birth, gender, Role)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, hashed_password, email, birth, gender, role))
            connection.commit()
            print("Пользователь зарегистрирован")
            cursor.close()
            connection.close()
    except Error as e:
        print("Ошибка при регистрации", e)

def authenticate_user(username, password):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT Password FROM users WHERE Username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()

            if result and bcrypt.checkpw(password.encode("utf-8"), result[0].encode("utf-8")):
                print("Авторизация успешна")
                return result
            else:
                print("Неправильное имя пользователя или пароль")
                return None
    except Error as e:
        print("Ошибка при авторизации", e)
    return None
