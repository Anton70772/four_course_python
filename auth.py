import tkinter as tk
from tkinter import messagebox
import mysql.connector
import main
import m2

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="234565",
    database="studentsDb"
)
cursor = db.cursor()

def register(username, password, entry_username, entry_password):
    role = "admin" if password == "admin" else "user"
    sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    val = (username, password, role)
    try:
        cursor.execute(sql, val)
        db.commit()
        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка", f"Ошибка при регистрации: {err}")

def login(username, password, login_window):
    sql = "SELECT role FROM users WHERE username = %s AND password = %s"
    val = (username, password)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        role = result[0]
        login_window.destroy()  # Закрываем окно авторизации
        if role == "admin":
            messagebox.showinfo("Успех", "Вход выполнен как администратор")
            m2.create_widgets_admin(tk.Tk())
        else:
            messagebox.showinfo("Успех", "Вход выполнен как обычный пользователь")
            main.create_widgets(tk.Tk())
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

def create_login_window():
    login_window = tk.Tk()
    login_window.title("Авторизация")

    tk.Label(login_window, text="Логин:").grid(row=0, column=0, padx=10, pady=10)
    entry_username = tk.Entry(login_window)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_window, text="Пароль:").grid(row=1, column=0, padx=10, pady=10)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(login_window, text="Войти", command=lambda: login(entry_username.get(), entry_password.get(), login_window)).grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(login_window, text="Зарегистрироваться", command=lambda: register(entry_username.get(), entry_password.get(), entry_username, entry_password)).grid(row=3, column=0, columnspan=2, pady=10)

    login_window.mainloop()

if __name__ == "__main__":
    create_login_window()