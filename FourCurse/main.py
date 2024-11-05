import flet as ft
from auth import register_user, authenticate_user
from app import main_app
from data_handler import get_user_data

def main(page: ft.Page):
    page.title = "Авторизация и Регистрация"

    def load_main_app(username):
        page.clean()
        user_data = get_user_data(username)
        main_app(page, user_data)

    def keep_focus(e):
        e.control.focus()

    def login_form():
        form = ft.Column([
            ft.TextField(label="Имя пользователя", key="username", on_change=keep_focus),
            ft.TextField(label="Пароль", password=True, key="password", on_change=keep_focus),
            ft.ElevatedButton("Войти", on_click=lambda _: login_action(form)),
            ft.TextButton("Нет аккаунта? Зарегистрироваться", on_click=lambda _: show_registration_form())
        ])
        return form

    def registration_form():
        form = ft.Column([
            ft.TextField(label="Имя пользователя", key="username", on_change=keep_focus),
            ft.TextField(label="Пароль", password=True, key="password", on_change=keep_focus),
            ft.TextField(label="Email", key="email", on_change=keep_focus),
            ft.TextField(label="Дата рождения", key="birth", on_change=keep_focus),
            ft.Dropdown(label="Пол", options=[ft.dropdown.Option("М"), ft.dropdown.Option("Ж")], key="gender"),
            ft.ElevatedButton("Зарегистрироваться", on_click=lambda _: register_action(form)),
            ft.TextButton("Уже есть аккаунт? Войти", on_click=lambda _: show_login_form())
        ])
        return form

    def login_action(form):
        username = form.controls[0].value
        password = form.controls[1].value

        user_data = authenticate_user(username, password)
        if user_data:
            page.snack_bar = ft.SnackBar(ft.Text("Авторизация успешна!"), open=True)
            page.update()
            load_main_app(username)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Ошибка авторизации!"), open=True)
            page.update()

    def register_action(form):
        username = form.controls[0].value
        password = form.controls[1].value
        email = form.controls[2].value
        birth = form.controls[3].value
        gender = form.controls[4].value

        register_user(username, password, email, birth, gender)
        page.snack_bar = ft.SnackBar(ft.Text("Регистрация успешна! Войдите для продолжения."), open=True)
        show_login_form()
        page.update()

    def show_login_form():
        page.clean()
        page.add(
            ft.Text("Авторизация", size=20, weight=ft.FontWeight.BOLD),
            login_form()
        )

    def show_registration_form():
        page.clean()
        page.add(
            ft.Text("Регистрация", size=20, weight=ft.FontWeight.BOLD),
            registration_form()
        )

    show_login_form()

ft.app(target=main)
