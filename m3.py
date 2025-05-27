import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as mysql
import tkinter.font

db = mysql.connect(host="localhost", user="root", password="234565", database="exam")
cur = db.cursor()

root = tk.Tk()
root.title("Данные продуктов")
root.geometry("1000x500")
tk.font.nametofont("TkDefaultFont").configure(family="Candara", size=10)

cols = ("Тип", "Наименование продукта", "Артикул", "Минимальная стоимость", "Основной материал", "Время изготовления")
tree = ttk.Treeview(root, columns=cols, show='headings')
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=150)
tree.pack(fill=tk.BOTH, expand=True)

def fetch(q, params=(), one=False):
    cur.execute(q, params)
    return (cur.fetchone() if one else cur.fetchall())

def get_id(table, field, value):
    res = fetch(f"SELECT id FROM {table} WHERE {field}=%s", (value,), one=True)
    return res[0] if res else None

def load_data():
    tree.delete(*tree.get_children())
    query = """SELECT pt.product_type, p.product_name, p.article_number, p.min_partner_price,
               m.material_type, pwd.production_time FROM products p
               JOIN product_types pt ON p.product_type_id = pt.id
               JOIN materials m ON p.material_id = m.id
               JOIN product_workshop_details pwd ON p.id = pwd.product_id"""
    for row in fetch(query):
        tree.insert('', tk.END, values=row)

def selected():
    if not (item := tree.focus()):
        messagebox.showwarning("Внимание", "Выберите запись")
        return
    return tree.item(item)['values']

def form_window(mode, current_pid=None):
    form = tk.Toplevel(root)
    form.title("Добавить продукт" if mode == 'add' else "Редактировать продукт")
    form.grab_set()

    fields = [
        ('Артикул', 'article', 'entry'),
        ('Тип продукта', 'type', 'combo', "SELECT product_type FROM product_types"),
        ('Наименование', 'name', 'entry'),
        ('Минимальная стоимость', 'price', 'entry'),
        ('Основной материал', 'material', 'entry')
    ]

    entries = {}
    for r, (lbl, name, typ, *q) in enumerate(fields):
        tk.Label(form, text=lbl).grid(row=r, column=0, sticky=tk.W, padx=5, pady=5)
        if typ == 'combo':
            cb = ttk.Combobox(form, state='readonly')
            cb['values'] = [x[0] for x in fetch(q[0])]
            cb.grid(row=r, column=1, padx=5, pady=5)
            entries[name] = cb
        else:
            e = ttk.Entry(form)
            e.grid(row=r, column=1, padx=5, pady=5)
            entries[name] = e

    if mode == 'edit':
        p = fetch(
            "SELECT article_number, product_name, min_partner_price, material_id, product_type_id FROM products WHERE id=%s",
            (current_pid,), one=True)
        if not p:
            messagebox.showerror("Ошибка", "Продукт не найден")
            form.destroy()
            return
        entries['article'].insert(0, p[0])
        entries['name'].insert(0, p[1])
        entries['price'].insert(0, p[2])
        entries['type'].set(fetch("SELECT product_type FROM product_types WHERE id=%s", (p[4],), one=True)[0])
        entries['material'].insert(0, fetch("SELECT material_type FROM materials WHERE id=%s", (p[3],), one=True)[0])

    def save():
        vals = {n: w.get() for n, w in entries.items()}
        if not all(vals.values()):
            messagebox.showwarning("Внимание", "Заполните все поля")
            return
        try:
            price = float(vals['price'])
        except:
            messagebox.showwarning("Ошибка", "Некорректная цена")
            return

        type_id = get_id('product_types', 'product_type', vals['type'])
        material = vals['material'].strip()
        mat_id = get_id('materials', 'material_type', material)
        if not mat_id:
            cur.execute("INSERT INTO materials (material_type) VALUES (%s)", (material,))
            mat_id = cur.lastrowid
            db.commit()

        data = (vals['article'], vals['name'], price, mat_id, type_id)
        if mode == 'add':
            cur.execute(
                "INSERT INTO products (article_number, product_name, min_partner_price, material_id, product_type_id) VALUES (%s,%s,%s,%s,%s)",
                data)
            pid = cur.lastrowid
            cur.execute(
                "INSERT INTO product_workshop_details (product_id, workshop_id, production_time) VALUES (%s, (SELECT id FROM product_workshops LIMIT 1), 0)",
                (pid,))
        else:
            cur.execute(
                "UPDATE products SET article_number=%s, product_name=%s, min_partner_price=%s, material_id=%s, product_type_id=%s WHERE id=%s",
                (*data, current_pid))
        db.commit()
        load_data()
        form.destroy()

    tk.Button(form, text="Сохранить", command=save).grid(row=5, column=0, pady=10)
    tk.Button(form, text="Назад", command=form.destroy).grid(row=5, column=1, pady=10)

def delete():
    if (s := selected()) and (pid := fetch("SELECT id FROM products WHERE article_number=%s", (s[2],), one=True)):
        try:
            cur.execute("DELETE FROM product_workshop_details WHERE product_id=%s", (pid[0],))
            cur.execute("DELETE FROM products WHERE id=%s", (pid[0],))
            db.commit()
            load_data()
        except Exception as e:
            db.rollback()
            messagebox.showerror("Ошибка", f"Не удалось удалить запись: {str(e)}")

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)
ttk.Button(btn_frame, text="Добавить", command=lambda: form_window('add')).pack(side=tk.LEFT, padx=5)
ttk.Button(btn_frame, text="Редактировать", command=lambda: form_window('edit', fetch(
    "SELECT id FROM products WHERE article_number=%s", (selected()[2],), one=True)[0]) if selected() else None).pack(
    side=tk.LEFT, padx=5)
ttk.Button(btn_frame, text="Удалить", command=delete).pack(side=tk.LEFT, padx=5)

load_data()
root.mainloop()
cur.close()
db.close()