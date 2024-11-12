import flet as ft
from db_requests import get_hospital

def main(page: ft.Page):
    page.title = "Управление потоком пациентов"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    hospital = get_hospital()

    hospitalizations_columns = ["id", "full_name", "passport_data"]
    hospitalizations_aliases = ["ID", "ФИО", "Паспортные данные"]

    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(alias)) for alias in hospitalizations_aliases],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(row[col]))) for col in hospitalizations_columns
                ]
            ) for row in hospital
        ]
    )

    page.add(table)
    page.update()

ft.app(target=main)

# from cProfile import label
#
# import flet as ft
# from oauthlib.uri_validate import query
#
# from db_connection import connect_to_db, exec_query
# from dp_requests import get_hospital
#
# def main(page: ft.Page):
#     page.title = "Application"
#     page.vertical_alignment = ft.MainAxisAlignment.START
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
#
#     data_conteiner = ft.Column()
#
#     hospital = get_hospital()
#
#     def load_data():
#         connection = connect_to_db()
#         if not connection:
#             data_conteiner.controls.append( ft.Text("Failed to connection"))
#             return []
#
#         query = "SELECT * FROM hospitalizations"
#         result = exec_query(connection, query)
#         connection.close()
#
#         columns = [
#             ft.DataColumn(ft.Text("ID")),
#             ft.DataColumn(ft.Text("Name")),
#             ft.DataColumn(ft.Text("Passport"))
#         ]
#
#         rows = []
#         for row in result:
#             rows.append(
#                 ft.DataRow(
#                     cells=[
#                         ft.DataCell(ft.Text(str (row['id']))),
#                         ft.DataCell(ft.Text(row ['full_name'])),
#                         ft.DataCell(ft.Text(row ['passport_data']))
#                     ]
#                 )
#             )
#         data_table = ft.DataTable(
#             columns=columns,
#             rows=rows
#         )
#
#         data_conteiner.controls.append(data_table)
#         page.update()
#
#     def new_hospital_form():
#         def keep_focus(e):
#             e.control.focus()
#
#         form = ft.column(
#             [
#                 ft.TextField(label="ФИО", hint_text="Введи полное имя", key="full_name", on_change=keep_focus()),
#                 ft.TextField(label="Паспорт", hint_text="Введите серию и номер паспорта", key="passport_data", on_change=keep_focus()),
#                 ft.ElevatedButton("Создать", on_click=lambda _: new_hospital(form))
#             ]
#         )
#         return form
#
#     def new_hospital(form):
#         data ={
#             "full_name":form.controls[0].value,
#             "passport_data": form.controls[1].value
#         }
#         insert_hospital(data)
#
#
#     load_data()
#
#     page.add(data_conteiner)
#
# ft.app(target=main)