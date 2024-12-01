import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="234565",
    database="studentsDb"
)
cursor = db.cursor()

def create_widgets(root):
    tab_control = ttk.Notebook(root)

    tab_students = ttk.Frame(tab_control)
    tab_courses = ttk.Frame(tab_control)

    tab_control.add(tab_students, text='Студенты')
    tab_control.add(tab_courses, text='Курсы')

    tab_control.pack(expand=1, fill='both')

    create_students_tab(tab_students)
    create_courses_tab(tab_courses)

def create_students_tab(tab_students):
    students_tree = ttk.Treeview(tab_students, columns=('ID', 'Name', 'Group', 'Date of Birth', 'Address', 'Phone'), show='headings')
    students_tree.heading('ID', text='ID')
    students_tree.heading('Name', text='ФИО')
    students_tree.heading('Group', text='Группа')
    students_tree.heading('Date of Birth', text='Дата рождения')
    students_tree.heading('Address', text='Адрес')
    students_tree.heading('Phone', text='Телефон')
    students_tree.pack(expand=True, fill='both')

    load_students(students_tree)
    students_tree.bind('<ButtonRelease-1>', lambda event: select_student(event, students_tree, entry_name, entry_group, entry_date_of_birth, entry_address, entry_phone))

    student_frame = ttk.Frame(tab_students)
    student_frame.pack(pady=10)

    ttk.Label(student_frame, text="ФИО:").grid(row=0, column=0, padx=5, pady=5)
    entry_name = ttk.Entry(student_frame)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(student_frame, text="Группа:").grid(row=1, column=0, padx=5, pady=5)
    entry_group = ttk.Entry(student_frame)
    entry_group.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(student_frame, text="Дата рождения:").grid(row=2, column=0, padx=5, pady=5)
    entry_date_of_birth = ttk.Entry(student_frame)
    entry_date_of_birth.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(student_frame, text="Адрес:").grid(row=3, column=0, padx=5, pady=5)
    entry_address = ttk.Entry(student_frame)
    entry_address.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(student_frame, text="Телефон:").grid(row=4, column=0, padx=5, pady=5)
    entry_phone = ttk.Entry(student_frame)
    entry_phone.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(student_frame, text="Добавить", command=lambda: add_student(students_tree, entry_name, entry_group, entry_date_of_birth, entry_address, entry_phone)).grid(row=5, column=0, padx=5, pady=5)
    ttk.Button(student_frame, text="Редактировать", command=lambda: edit_student(students_tree, entry_name, entry_group, entry_date_of_birth, entry_address, entry_phone)).grid(row=5, column=1, padx=5, pady=5)
    ttk.Button(student_frame, text="Удалить", command=lambda: delete_student(students_tree)).grid(row=5, column=2, padx=5, pady=5)

def create_courses_tab(tab_courses):
    courses_tree = ttk.Treeview(tab_courses, columns=('ID', 'Name', 'Description'), show='headings')
    courses_tree.heading('ID', text='ID')
    courses_tree.heading('Name', text='Название')
    courses_tree.heading('Description', text='Описание')
    courses_tree.pack(expand=True, fill='both')

    load_courses(courses_tree)
    courses_tree.bind('<ButtonRelease-1>', lambda event: select_course(event, courses_tree, entry_course_name, entry_course_description))

    course_frame = ttk.Frame(tab_courses)
    course_frame.pack(pady=10)

    ttk.Label(course_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
    entry_course_name = ttk.Entry(course_frame)
    entry_course_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(course_frame, text="Описание:").grid(row=1, column=0, padx=5, pady=5)
    entry_course_description = ttk.Entry(course_frame)
    entry_course_description.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(course_frame, text="Добавить", command=lambda: add_course(courses_tree, entry_course_name, entry_course_description)).grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(course_frame, text="Редактировать", command=lambda: edit_course(courses_tree, entry_course_name, entry_course_description)).grid(row=2, column=1, padx=5, pady=5)
    ttk.Button(course_frame, text="Удалить", command=lambda: delete_course(courses_tree)).grid(row=2, column=2, padx=5, pady=5)

def load_students(students_tree):
    students_tree.delete(*students_tree.get_children())
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        students_tree.insert('', 'end', values=row)

def load_courses(courses_tree):
    courses_tree.delete(*courses_tree.get_children())
    cursor.execute("SELECT * FROM courses")
    for row in cursor.fetchall():
        courses_tree.insert('', 'end', values=row)

def select_student(event, students_tree, entry_name, entry_group, entry_date_of_birth, entry_address, entry_phone):
    selected_item = students_tree.selection()[0]
    values = students_tree.item(selected_item, 'values')
    entry_name.delete(0, tk.END)
    entry_name.insert(0, values[1])
    entry_group.delete(0, tk.END)
    entry_group.insert(0, values[2])
    entry_date_of_birth.delete(0, tk.END)
    entry_date_of_birth.insert(0, values[3])
    entry_address.delete(0, tk.END)
    entry_address.insert(0, values[4])
    entry_phone.delete(0, tk.END)
    entry_phone.insert(0, values[5])

def select_course(event, courses_tree, entry_course_name, entry_course_description):
    selected_item = courses_tree.selection()[0]
    values = courses_tree.item(selected_item, 'values')
    entry_course_name.delete(0, tk.END)
    entry_course_name.insert(0, values[1])
    entry_course_description.delete(0, tk.END)
    entry_course_description.insert(0, values[2])

def add_student(students_tree, entry_name, entry_group, entry_date_of_birth, entry_address, entry_phone):
    name = entry_name.get()
    group = entry_group.get()
    date_of_birth = entry_date_of_birth.get()
    address = entry_address.get()
    phone = entry_phone.get()

    sql = "INSERT INTO students (name, course, date_of_birth, address, phone) VALUES (%s, %s, %s, %s, %s)"
    val = (name, group, date_of_birth, address, phone)
    cursor.execute(sql, val)
    db.commit()

    load_students(students_tree)
    clear_student_entries(entry_name, entry_group, entry_date_of_birth, entry_address, entry_phone)

def edit_student(students_tree, entry_name, entry_group, entry_date_of_birth, entry_address, entry_phone):
    selected_item = students_tree.selection()[0]
    student_id = students_tree.item(selected_item, 'values')[0]
    name = entry_name.get()
    group = entry_group.get()
    date_of_birth = entry_date_of_birth.get()
    address = entry_address.get()
    phone = entry_phone.get()

    sql = "UPDATE students SET name=%s, course=%s, date_of_birth=%s, address=%s, phone=%s WHERE id=%s"
    val = (name, group, date_of_birth, address, phone, student_id)
    cursor.execute(sql, val)
    db.commit()

    load_students(students_tree)
    clear_student_entries(entry_name, entry_group, entry_date_of_birth, entry_address, entry_phone)

def delete_student(students_tree):
    selected_item = students_tree.selection()[0]
    student_id = students_tree.item(selected_item, 'values')[0]

    sql = "DELETE FROM students WHERE id=%s"
    val = (student_id,)
    cursor.execute(sql, val)
    db.commit()

    load_students(students_tree)

def clear_student_entries(entry_name, entry_group, entry_date_of_birth, entry_address, entry_phone):
    entry_name.delete(0, tk.END)
    entry_group.delete(0, tk.END)
    entry_date_of_birth.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_phone.delete(0, tk.END)

def add_course(courses_tree, entry_course_name, entry_course_description):
    name = entry_course_name.get()
    description = entry_course_description.get()

    sql = "INSERT INTO courses (name, description) VALUES (%s, %s)"
    val = (name, description)
    cursor.execute(sql, val)
    db.commit()

    load_courses(courses_tree)
    clear_course_entries(entry_course_name, entry_course_description)

def edit_course(courses_tree, entry_course_name, entry_course_description):
    selected_item = courses_tree.selection()[0]
    course_id = courses_tree.item(selected_item, 'values')[0]
    name = entry_course_name.get()
    description = entry_course_description.get()

    sql = "UPDATE courses SET name=%s, description=%s WHERE id=%s"
    val = (name, description, course_id)
    cursor.execute(sql, val)
    db.commit()

    load_courses(courses_tree)
    clear_course_entries(entry_course_name, entry_course_description)

def delete_course(courses_tree):
    selected_item = courses_tree.selection()[0]
    course_id = courses_tree.item(selected_item, 'values')[0]

    sql = "DELETE FROM courses WHERE id=%s"
    val = (course_id,)
    cursor.execute(sql, val)
    db.commit()

    load_courses(courses_tree)

def clear_course_entries(entry_course_name, entry_course_description):
    entry_course_name.delete(0, tk.END)
    entry_course_description.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Управление базой данных студентов")
    create_widgets(root)
    root.mainloop()