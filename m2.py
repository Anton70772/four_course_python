import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as mysql
import tkinter.font as tkfont

db = mysql.connect(host="localhost", user="root", password="234565", database="variant5")
cur = db.cursor()

root = tk.Tk()
root.title("Данные материалов")
root.geometry("1000x500")
# root.iconbitmap('icon.ico')

style = ttk.Style()
style.configure("Treeview.Heading", font=('Candara', 10, 'bold'))
style.configure("TButton", font=('Candara', 10), background="#355CBD", foreground="white")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

main_tab = ttk.Frame(notebook)
notebook.add(main_tab, text="Главная")

cols = ("id", "Тип", "Наименование материала", "Минимальное кол-во", "Кол-во на складе", "Цена", "Требуемое кол-во")
tree = ttk.Treeview(main_tab, columns=cols, show='headings')
tree.column("id", width=0, stretch=tk.NO)

for c in cols[1:]:
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
    query = """
    SELECT 
        m.id,
        mt.material_type, 
        m.name, 
        m.min_count, 
        m.count_storage, 
        CONCAT(m.unit_price, ' ', m.unit_metrik, ' | ', m.count_package) as price_info
    FROM materials m
    JOIN material_type mt ON m.material_type_id = mt.id
    """
    for row in fetch(query):
        try:
            min_val = float(row[3].replace(',', '.'))
            storage_val = float(row[4].replace(',', '.'))
            required = max(0, min_val - storage_val)
            required_str = format(required, '.2f').replace('.', ',')
        except:
            required_str = "0,00"

        tree.insert('', tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5], required_str))


def selected():
    if not (item := tree.focus()):
        messagebox.showwarning("Внимание", "Выберите запись")
        return
    return tree.item(item)['values']


def form_tab(mode, current_mid=None):
    form = ttk.Frame(notebook)
    tab_title = "Добавить материал" if mode == 'add' else "Редактировать материал"
    notebook.add(form, text=tab_title)
    notebook.select(form)

    fields = [
        ('Тип материала', 'type', 'combo', 'str', "SELECT material_type FROM material_type"),
        ('Наименование', 'name', 'entry', 'str'),
        ('Цена единицы', 'price', 'entry', 'num'),
        ('Единица измерения', 'unit', 'entry', 'str'),
        ('Количество в упаковке', 'pack', 'entry', 'num'),
        ('Количество на складе', 'storage', 'entry', 'num'),
        ('Минимальное количество', 'min', 'entry', 'num')
    ]

    entries = {}
    for r, (lbl, name, typ, dtype, *q) in enumerate(fields):
        tk.Label(form, text=lbl).grid(row=r, column=0, sticky=tk.W, padx=5, pady=5)
        if typ == 'combo':
            cb = ttk.Combobox(form, state='readonly')
            cb['values'] = [x[0] for x in fetch(q[0])]
            cb.grid(row=r, column=1, padx=5, pady=5)
            entries[name] = (cb, dtype)
        else:
            e = ttk.Entry(form)
            e.grid(row=r, column=1, padx=5, pady=5)
            entries[name] = (e, dtype)

    if mode == 'edit':
        p = fetch(
            "SELECT name, unit_price, unit_metrik, count_package, count_storage, min_count, material_type_id FROM materials WHERE id=%s",
            (current_mid,), one=True)
        if not p:
            messagebox.showerror("Ошибка", "Материал не найден")
            notebook.forget(notebook.index(form))
            return

        entries['name'][0].insert(0, p[0])
        entries['price'][0].insert(0, p[1])
        entries['unit'][0].insert(0, p[2])
        entries['pack'][0].insert(0, p[3])
        entries['storage'][0].insert(0, p[4])
        entries['min'][0].insert(0, p[5])
        entries['type'][0].set(fetch("SELECT material_type FROM material_type WHERE id=%s", (p[6],), one=True)[0])

    def validate_fields():
        errors = []
        vals = {}

        for name, (widget, dtype) in entries.items():
            value = widget.get().strip()

            if not value:
                errors.append(f"Поле '{name}' не заполнено")
                continue

            if dtype == 'num':
                try:
                    value = value.replace(',', '.')
                    value_float = float(value)
                    if value_float < 0:
                        errors.append(f"Поле '{name}' должно быть положительным числом")
                    else:
                        vals[name] = format(value_float, '.2f').replace('.', ',')
                except ValueError:
                    errors.append(f"Поле '{name}' должно содержать число")
            else:
                vals[name] = value

        if errors:
            messagebox.showerror("Ошибки в данных", "\n".join(errors))
            return None

        return vals

    def save():
        if not (vals := validate_fields()):
            return

        type_id = get_id('material_type', 'material_type', vals['type'])
        if type_id is None:
            messagebox.showerror("Ошибка", "Неверный тип материала")
            return

        data = (
            vals['name'],
            vals['price'],
            vals['unit'],
            vals['pack'],
            vals['storage'],
            vals['min'],
            type_id
        )

        try:
            if mode == 'add':
                cur.execute("""
                    INSERT INTO materials 
                    (name, unit_price, unit_metrik, count_package, count_storage, min_count, material_type_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, data)
                messagebox.showinfo("Успех", "Материал успешно добавлен")
            else:
                cur.execute("""
                    UPDATE materials SET 
                    name=%s, unit_price=%s, unit_metrik=%s, count_package=%s, count_storage=%s, min_count=%s, material_type_id=%s 
                    WHERE id=%s
                """, (*data, current_mid))
                messagebox.showinfo("Успех", "Материал успешно обновлен")

            db.commit()
            load_data()
            notebook.forget(notebook.index(form))

        except Exception as e:
            db.rollback()
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")

    def on_close():
        notebook.forget(notebook.index(form))

    tk.Button(form, text='Сохранить', command=save, font=('Candara', 10), bg="#355CBD", fg="white").grid(row=8,
                                                                                                         column=0,
                                                                                                         pady=10)
    tk.Button(form, text='Назад', command=on_close, font=('Candara', 10), bg="#355CBD", fg="white").grid(row=8,
                                                                                                         column=1,
                                                                                                         pady=10)

def delete():
    if not (s := selected()):
        return
    material_id = s[0]

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот материал? Это также удалит все связанные записи в продуктах."):
        try:
            cur.execute("DELETE FROM material_products WHERE material_id=%s", (material_id,))
            cur.execute("DELETE FROM materials WHERE id=%s", (material_id,))
            db.commit()
            load_data()
            messagebox.showinfo("Успех", "Материал и связанные данные успешно удалены")
        except Exception as e:
            db.rollback()
            messagebox.showerror("Ошибка", f"Не удалось удалить запись: {str(e)}")

btn_frame = ttk.Frame(main_tab)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Добавить", command=lambda: form_tab('add'),
          font=('Candara', 10), bg="#355CBD", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Редактировать",
          command=lambda: form_tab('edit', selected()[0]) if selected() else None,
          font=('Candara', 10), bg="#355CBD", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Удалить", command=delete,
          font=('Candara', 10), bg="#355CBD", fg="white").pack(side=tk.LEFT, padx=5)

load_data()
root.mainloop()
cur.close()
db.close()