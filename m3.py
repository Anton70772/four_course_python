import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import tkinter.font as tkfont

db = mysql.connector.connect(host="localhost", user="root", password="234565", database="exam")
cursor = db.cursor()

root = tk.Tk()
root.title("Данные продуктов")
root.geometry("1000x500")

default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(family="Candara", size=10)

columns = (
"Тип", "Наименование продукта", "Артикул", "Минимальная стоимость", "Основной материал", "Время изготовления")

tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill=tk.BOTH, expand=True)

def get_list(query):
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def get_id_by_name(table, name_field, name_value):
    cursor.execute(f"SELECT id FROM {table} WHERE {name_field}=%s", (name_value,))
    res = cursor.fetchone()
    return res[0] if res else None

def get_product_id_by_article(article):
    cursor.execute("SELECT id FROM products WHERE article_number=%s", (article,))
    return cursor.fetchone()

def load_data():
    query = """
        SELECT 
            product_types.product_type,
            products.product_name,
            products.article_number,
            products.min_partner_price,
            materials.material_type,
            product_workshop_details.production_time
        FROM products
        JOIN product_types ON products.product_type_id = product_types.id
        JOIN materials ON products.material_id = materials.id
        JOIN product_workshop_details ON products.id = product_workshop_details.product_id
        JOIN product_workshops ON product_workshop_details.workshop_id = product_workshops.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert('', tk.END, values=row)

def get_selected():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Внимание", "Выберите запись")
        return None
    return tree.item(selected)['values']

def get_workshop_id():
    cursor.execute("SELECT id FROM product_workshops LIMIT 1")
    return cursor.fetchone()[0]

def create_form_window(mode='add', product_id=None):
    form = tk.Toplevel(root)
    form.title("Добавить продукт" if mode == 'add' else "Редактировать продукт")
    form.geometry("400x300")
    form.grab_set()

    fields = [
        {'label': 'Артикул', 'name': 'article', 'type': 'entry'},
        {'label': 'Тип продукта', 'name': 'product_type', 'type': 'combobox',
         'query': "SELECT product_type FROM product_types"},
        {'label': 'Наименование', 'name': 'name', 'type': 'entry'},
        {'label': 'Минимальная стоимость', 'name': 'price', 'type': 'entry'},
        {'label': 'Основной материал', 'name': 'material', 'type': 'combobox',
         'query': "SELECT material_type FROM materials"},
    ]

    vars = {}
    for i, field in enumerate(fields):
        ttk.Label(form, text=field['label']).grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)
        if field['type'] == 'entry':
            entry = ttk.Entry(form)
            entry.grid(row=i, column=1, pady=5, padx=5)
            vars[field['name']] = entry
        elif field['type'] == 'combobox':
            cb = ttk.Combobox(form, state='readonly')
            cb['values'] = get_list(field['query'])
            cb.grid(row=i, column=1, pady=5, padx=5)
            vars[field['name']] = cb

    def load_product_data():
        cursor.execute(
            "SELECT article_number, product_name, min_partner_price, material_id, product_type_id FROM products WHERE id=%s",
            (product_id,))
        prod = cursor.fetchone()
        if not prod:
            messagebox.showerror("Ошибка", "Продукт не найден")
            form.destroy()
            return
        article, name, price, material_id, type_id = prod
        vars['article'].insert(0, article)
        vars['name'].insert(0, name)
        vars['price'].insert(0, str(price))
        cursor.execute("SELECT product_type FROM product_types WHERE id=%s", (type_id,))
        vars['product_type'].set(cursor.fetchone()[0])
        cursor.execute("SELECT material_type FROM materials WHERE id=%s", (material_id,))
        vars['material'].set(cursor.fetchone()[0])

    def save_data():
        data = {}
        for field in fields:
            val = vars[field['name']].get()
            data[field['name']] = val
        if not all(data.values()):
            messagebox.showwarning("Внимание", "Заполните все поля")
            form.lift()
            return
        try:
            price = float(data['price'])
        except:
            messagebox.showwarning("Внимание", "Некорректная цена")
            return

        type_id = get_id_by_name('product_types', 'product_type', data['product_type'])
        material_id = get_id_by_name('materials', 'material_type', data['material'])

        if mode == 'add':
            cursor.execute(
                "INSERT INTO products (article_number, product_name, min_partner_price, material_id, product_type_id) VALUES (%s,%s,%s,%s,%s)",
                (data['article'], data['name'], price, material_id, type_id)
            )
            db.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            new_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO product_workshop_details (product_id, workshop_id, production_time) VALUES (%s, %s, %s)",
                (new_id, get_workshop_id(), 0)
            )
            db.commit()
        else:
            cursor.execute(
                "UPDATE products SET product_name=%s, min_partner_price=%s, material_id=%s, product_type_id=%s WHERE id=%s",
                (data['name'], price, material_id, type_id, product_id))
            cursor.execute("UPDATE product_workshop_details SET production_time=%s WHERE product_id=%s",
                           (0, product_id))
            db.commit()

        load_data()
        form.destroy()

    if mode == 'edit' and product_id:
        load_product_data()

    ttk.Button(form, text="Сохранить", command=save_data).grid(row=len(fields), column=0, pady=10)
    ttk.Button(form, text="Назад", command=form.destroy).grid(row=len(fields), column=1, pady=10)

def open_add():
    create_form_window(mode='add')

def open_edit():
    selected = get_selected()
    if selected:
        product_id = get_product_id_by_article(selected[2])
        if product_id:
            create_form_window(mode='edit', product_id=product_id[0])

def delete_product():
    selected = get_selected()
    if selected:
        product_id = get_product_id_by_article(selected[2])
        if product_id:
            cursor.execute("DELETE FROM product_workshop_details WHERE product_id=%s", (product_id[0],))
            cursor.execute("DELETE FROM products WHERE id=%s", (product_id[0],))
            db.commit()
            load_data()

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)
ttk.Button(btn_frame, text="Добавить", command=open_add).pack(side=tk.LEFT, padx=5)
ttk.Button(btn_frame, text="Редактировать", command=open_edit).pack(side=tk.LEFT, padx=5)
ttk.Button(btn_frame, text="Удалить", command=delete_product).pack(side=tk.LEFT, padx=5)

load_data()

root.mainloop()

cursor.close()
db.close()