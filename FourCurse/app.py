import flet as ft
from data_handler import get_hospitalizations, get_medical_procedures, get_patients, insert_patient, insert_hospital, insert_procedures
from auth import register_user, authenticate_user

def main(page: ft.Page):
    page.title = "Управление потоком пациентов"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def create_data_table(data, columns, aliases):
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(aliases[i])) for i in range(len(columns))],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(item[col]))) for col in columns]) for item in data]
        )
        return ft.Column(controls=[table], scroll=True)

    def show_data(data, title, columns, aliases, button=None):
        data_view = ft.Column()
        title_row = ft.Row([ft.Text(title, size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        if button:
            title_row.controls.append(button)
        data_view.controls.append(title_row)
        if data:
            data_view.controls.append(create_data_table(data, columns, aliases))
        else:
            data_view.controls.append(ft.Text("Нет данных"))
        return data_view

    def login_form():
        def login(e):
            username = username_field.value
            password = password_field.value
            if authenticate_user(username, password):
                page.controls.remove(login_view)
                page.add(main_view)
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Неверное имя пользователя или пароль"), open=True)
                page.update()

        username_field = ft.TextField(label="Имя пользователя", hint_text="Введите имя пользователя")
        password_field = ft.TextField(label="Пароль", hint_text="Введите пароль", password=True,
                                      can_reveal_password=True)
        login_button = ft.ElevatedButton("Войти", on_click=login)

        return ft.Column(
            [
                username_field,
                password_field,
                login_button
            ]
        )

    def register_form():
        def register(e):
            username = username_field.value
            password = password_field.value
            email = email_field.value
            birth = birth_field.value
            gender = gender_field.value
            role = role_field.value
            if register_user(username, password, email, birth, gender, role):
                page.snack_bar = ft.SnackBar(ft.Text("Регистрация успешна"), open=True)
                page.update()
                show_view(login_view)
                for control in [username_field, password_field, email_field, birth_field, gender_field, role_field]:
                    if isinstance(control, ft.TextField):
                        control.value = ""
                    elif isinstance(control, ft.Dropdown):
                        control.value = None
                register_form().update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Ошибка регистрации"), open=True)
                page.update()

        username_field = ft.TextField(label="Имя пользователя", hint_text="Введите имя пользователя")
        password_field = ft.TextField(label="Пароль", hint_text="Введите пароль", password=True,
                                      can_reveal_password=True)
        email_field = ft.TextField(label="Email", hint_text="Введите email")
        birth_field = ft.TextField(label="Дата рождения", hint_text="Введите дату рождения")
        gender_field = ft.Dropdown(label="Пол", options=[ft.dropdown.Option("М"), ft.dropdown.Option("Ж")])
        role_field = ft.TextField(label="Роль", hint_text="Введите роль")
        register_button = ft.ElevatedButton("Зарегистрироваться", on_click=register)

        return ft.Column(
            [
                username_field,
                password_field,
                email_field,
                birth_field,
                gender_field,
                role_field,
                register_button
            ]
        )

    login_view = login_form()
    register_view = register_form()

    hospitalizations = get_hospitalizations()
    medical_procedures = get_medical_procedures()
    patients = get_patients()

    hospitalizations_columns = ["id", "full_name", "passport_data", "diagnosis", "hospitalization_date_time", "hospitalization_code"]
    hospitalizations_aliases = ["ID", "ФИО", "Паспортные данные", "Диагноз", "Дата госпитализации", "Код госпитализации"]

    medical_procedures_columns = ["id", "patient_id", "Procedure_date", "Doctor", "Procedure_type", "Procedure_name"]
    medical_procedures_aliases = ["ID", "Пациент ID", "Дата процедуры", "Врач", "Тип процедуры", "Название процедуры"]

    patients_columns = ["id", "First_name", "Last_name", "Patronymic", "Date_of_birth", "Gender", "Phone_number"]
    patients_aliases = ["ID", "Имя", "Фамилия", "Отчество", "Дата рождения", "Пол", "Телефон"]

    register_hospital_button = ft.ElevatedButton("Создать госпитализацию", on_click=lambda _: show_view(register_hospital_view))
    hospitalizations_view = show_data(hospitalizations, "Госпитализации", hospitalizations_columns, hospitalizations_aliases, button=register_hospital_button)

    register_procedure_button = ft.ElevatedButton("Создать медицинскую процедуру", on_click=lambda _: show_view(register_procedure_view))
    medical_procedures_view = show_data(medical_procedures, "Медицинские процедуры", medical_procedures_columns, medical_procedures_aliases, button=register_procedure_button)

    register_patient_button = ft.ElevatedButton("Зарегистрировать пациента", on_click=lambda _: show_view(register_patient_view))
    patients_view = show_data(patients, "Пациенты", patients_columns, patients_aliases, button=register_patient_button)

    current_view = ft.Text("Выберите раздел для просмотра")

    def show_view(view):
        nonlocal current_view
        if current_view in page.controls:
            page.controls.remove(current_view)
        current_view = view
        page.add(current_view)
        page.update()

    def register_patient_form():
        def keep_focus(e):
            e.control.focus()

        form = ft.Column(
            [
                ft.TextField(label="Имя", hint_text="Введите имя", key="First_name", on_change=keep_focus),
                ft.TextField(label="Фамилия", hint_text="Введите фамилию", key="Last_name", on_change=keep_focus),
                ft.TextField(label="Отчество", hint_text="Введите отчество", key="Patronymic", on_change=keep_focus),
                ft.TextField(label="Дата рождения", hint_text="Введите дату рождения", key="Date_of_birth", on_change=keep_focus),
                ft.TextField(label="Паспорт", hint_text="Введите серию и номер паспорта", key="Passport_number", on_change=keep_focus),
                ft.TextField(label="Email", hint_text="Введите e-mail", key="Email", on_change=keep_focus),
                ft.Dropdown(label="Пол", options=[ft.dropdown.Option("М"), ft.dropdown.Option("Ж")], key="Gender"),
                ft.TextField(label="Телефон", hint_text="Введите телефон", key="Phone_number", on_change=keep_focus),
                ft.ElevatedButton("Зарегистрировать", on_click=lambda _: register_patient(form))
            ]
        )
        return form

    def register_patient(form):
        data = {
            "First_name": form.controls[0].value,
            "Last_name": form.controls[1].value,
            "Patronymic": form.controls[2].value,
            "Date_of_birth": form.controls[3].value,
            "Passport_number": form.controls[4].value,
            "Email": form.controls[5].value,
            "Gender": form.controls[6].value,
            "Phone_number": form.controls[7].value
        }
        insert_patient(data)
        updated_patients = get_patients()
        nonlocal patients_view
        patients_view = show_data(updated_patients, "Пациенты", patients_columns, patients_aliases, button=register_patient_button)
        show_view(patients_view)

        for control in form.controls:
            if isinstance(control, ft.TextField):
                control.value = ""
            elif isinstance(control, ft.Dropdown):
                control.value = None
        form.update()

    register_patient_view = register_patient_form()

    def register_hospital_form():
        def keep_focus(e):
            e.control.focus()

        form = ft.Column(
            [
                ft.TextField(label="ФИО", hint_text="Введите полное имя", key="full_name", on_change=keep_focus),
                ft.TextField(label="Паспорт", hint_text="Введите серию и номер паспорта", key="passport_data", on_change=keep_focus),
                ft.TextField(label="Диагноз", hint_text="Введите диагноз", key="diagnosis", on_change=keep_focus),
                ft.TextField(label="Дата госпитализации", hint_text="Укажите дату", key="hospitalization_date_time", on_change=keep_focus),
                ft.TextField(label="Код госпитализации", hint_text="Укажите код госпитализации", key="hospitalization_code", on_change=keep_focus),
                ft.ElevatedButton("Создать", on_click=lambda _: register_hospital(form))
            ]
        )
        return form

    def register_hospital(form):
        data = {
            "full_name": form.controls[0].value,
            "passport_data": form.controls[1].value,
            "diagnosis": form.controls[2].value,
            "hospitalization_date_time": form.controls[3].value,
            "hospitalization_code": form.controls[4].value
        }
        insert_hospital(data)
        updated_hospitalizations = get_hospitalizations()
        nonlocal hospitalizations_view
        hospitalizations_view = show_data(updated_hospitalizations, "Госпитализации", hospitalizations_columns, hospitalizations_aliases, button=register_hospital_button)
        show_view(hospitalizations_view)

        for control in form.controls:
            if isinstance(control, ft.TextField):
                control.value = ""
            elif isinstance(control, ft.Dropdown):
                control.value = None
        form.update()

    register_hospital_view = register_hospital_form()

    def register_procedure_form():
        def keep_focus(e):
            e.control.focus()

        form = ft.Column(
            [
                ft.TextField(label="Пациент ID", hint_text="Введите ID пациента", key="patient_id", on_change=keep_focus),
                ft.TextField(label="Дата процедуры", hint_text="Введите дату процедуры", key="Procedure_date", on_change=keep_focus),
                ft.TextField(label="Врач", hint_text="Введите имя врача", key="Doctor", on_change=keep_focus),
                ft.TextField(label="Тип процедуры", hint_text="Введите тип процедуры", key="Procedure_type", on_change=keep_focus),
                ft.TextField(label="Название процедуры", hint_text="Введите название процедуры", key="Procedure_name", on_change=keep_focus),
                ft.ElevatedButton("Создать", on_click=lambda _: register_procedure(form))
            ]
        )
        return form

    def register_procedure(form):
        data = {
            "patient_id": form.controls[0].value,
            "Procedure_date": form.controls[1].value,
            "Doctor": form.controls[2].value,
            "Procedure_type": form.controls[3].value,
            "Procedure_name": form.controls[4].value
        }
        insert_procedures(data)
        updated_procedures = get_medical_procedures()
        nonlocal medical_procedures_view
        medical_procedures_view = show_data(updated_procedures, "Медицинские процедуры", medical_procedures_columns, medical_procedures_aliases, button=register_procedure_button)
        show_view(medical_procedures_view)

        for control in form.controls:
            if isinstance(control, ft.TextField):
                control.value = ""
            elif isinstance(control, ft.Dropdown):
                control.value = None
        form.update()

    register_procedure_view = register_procedure_form()

    main_view = ft.Column(
        [
            ft.Row([
                ft.ElevatedButton("Госпитализации", on_click=lambda _: show_view(hospitalizations_view)),
                ft.ElevatedButton("Медицинские процедуры", on_click=lambda _: show_view(medical_procedures_view)),
                ft.ElevatedButton("Пациенты", on_click=lambda _: show_view(patients_view))
            ], alignment=ft.MainAxisAlignment.CENTER),
            current_view
        ]
    )

    login_view = login_form()
    page.add(login_view)

ft.app(target=main)


def main(page: ft.Page):
    page.title = "Управление потоком пациентов"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    current_view = ft.Text("Выберите раздел для просмотра")

    def show_view(view):
        nonlocal current_view
        if current_view in page.controls:
            page.controls.remove(current_view)
        current_view = view
        page.add(current_view)
        page.update()

    def login_form():
        def login(e):
            username = username_field.value
            password = password_field.value
            if authenticate_user(username, password):
                page.controls.remove(login_view)
                page.add(main_view)
                page.update()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Неверное имя пользователя или пароль"), open=True)
                page.update()

        username_field = ft.TextField(label="Имя пользователя", hint_text="Введите имя пользователя")
        password_field = ft.TextField(label="Пароль", hint_text="Введите пароль", password=True,
                                      can_reveal_password=True)
        login_button = ft.ElevatedButton("Войти", on_click=login)

        return ft.Column(
            [
                username_field,
                password_field,
                login_button
            ]
        )

    def register_form():
        def register(e):
            username = username_field.value
            password = password_field.value
            email = email_field.value
            birth = birth_field.value
            gender = gender_field.value
            role = role_field.value
            if register_user(username, password, email, birth, gender, role):
                page.snack_bar = ft.SnackBar(ft.Text("Регистрация успешна"), open=True)
                page.update()
                show_view(login_view)
                # Очистка полей формы регистрации
                for control in [username_field, password_field, email_field, birth_field, gender_field, role_field]:
                    if isinstance(control, ft.TextField):
                        control.value = ""
                    elif isinstance(control, ft.Dropdown):
                        control.value = None
                register_form().update()  # Обновление формы регистрации
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Ошибка регистрации"), open=True)
                page.update()

        username_field = ft.TextField(label="Имя пользователя", hint_text="Введите имя пользователя")
        password_field = ft.TextField(label="Пароль", hint_text="Введите пароль", password=True, can_reveal_password=True)
        email_field = ft.TextField(label="Email", hint_text="Введите email")
        birth_field = ft.TextField(label="Дата рождения", hint_text="Введите дату рождения")
        gender_field = ft.Dropdown(label="Пол", options=[ft.dropdown.Option("М"), ft.dropdown.Option("Ж")])
        role_field = ft.TextField(label="Роль", hint_text="Введите роль")
        register_button = ft.ElevatedButton("Зарегистрироваться", on_click=register)
        login_button = ft.ElevatedButton("Войти", on_click=lambda _: show_view(login_view))

        return ft.Column(
            [
                username_field,
                password_field,
                email_field,
                birth_field,
                gender_field,
                role_field,
                register_button,
                login_button
            ]
        )

    login_view = login_form()
    register_view = register_form()

    hospitalizations = get_hospitalizations()
    medical_procedures = get_medical_procedures()
    patients = get_patients()

    hospitalizations_columns = ["id", "full_name", "passport_data", "diagnosis", "hospitalization_date_time", "hospitalization_code"]
    hospitalizations_aliases = ["ID", "ФИО", "Паспортные данные", "Диагноз", "Дата госпитализации", "Код госпитализации"]

    medical_procedures_columns = ["id", "patient_id", "Procedure_date", "Doctor", "Procedure_type", "Procedure_name"]
    medical_procedures_aliases = ["ID", "Пациент ID", "Дата процедуры", "Врач", "Тип процедуры", "Название процедуры"]

    patients_columns = ["id", "First_name", "Last_name", "Patronymic", "Date_of_birth", "Gender", "Phone_number"]
    patients_aliases = ["ID", "Имя", "Фамилия", "Отчество", "Дата рождения", "Пол", "Телефон"]

    register_hospital_button = ft.ElevatedButton("Создать госпитализацию", on_click=lambda _: show_view(register_hospital_view))
    hospitalizations_view = show_data(hospitalizations, "Госпитализации", hospitalizations_columns, hospitalizations_aliases, button=register_hospital_button)

    register_procedure_button = ft.ElevatedButton("Создать медицинскую процедуру", on_click=lambda _: show_view(register_procedure_view))
    medical_procedures_view = show_data(medical_procedures, "Медицинские процедуры", medical_procedures_columns, medical_procedures_aliases, button=register_procedure_button)

    register_patient_button = ft.ElevatedButton("Зарегистрировать пациента", on_click=lambda _: show_view(register_patient_view))
    patients_view = show_data(patients, "Пациенты", patients_columns, patients_aliases, button=register_patient_button)

    def create_data_table(data, columns, aliases):
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(aliases[i])) for i in range(len(columns))],
            rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(item[col]))) for col in columns]) for item in data]
        )
        return ft.Column(controls=[table], scroll=True)

    def show_data(data, title, columns, aliases, button=None):
        data_view = ft.Column()
        title_row = ft.Row([ft.Text(title, size=20, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        if button:
            title_row.controls.append(button)
        data_view.controls.append(title_row)
        if data:
            data_view.controls.append(create_data_table(data, columns, aliases))
        else:
            data_view.controls.append(ft.Text("Нет данных"))
        return data_view

    def register_patient_form():
        def keep_focus(e):
            e.control.focus()

        form = ft.Column(
            [
                ft.TextField(label="Имя", hint_text="Введите имя", key="First_name", on_change=keep_focus),
                ft.TextField(label="Фамилия", hint_text="Введите фамилию", key="Last_name", on_change=keep_focus),
                ft.TextField(label="Отчество", hint_text="Введите отчество", key="Patronymic", on_change=keep_focus),
                ft.TextField(label="Дата рождения", hint_text="Введите дату рождения", key="Date_of_birth", on_change=keep_focus),
                ft.TextField(label="Паспорт", hint_text="Введите серию и номер паспорта", key="Passport_number", on_change=keep_focus),
                ft.TextField(label="Email", hint_text="Введите e-mail", key="Email", on_change=keep_focus),
                ft.Dropdown(label="Пол", options=[ft.dropdown.Option("М"), ft.dropdown.Option("Ж")], key="Gender"),
                ft.TextField(label="Телефон", hint_text="Введите телефон", key="Phone_number", on_change=keep_focus),
                ft.ElevatedButton("Зарегистрировать", on_click=lambda _: register_patient(form))
            ]
        )
        return form

    def register_patient(form):
        data = {
            "First_name": form.controls[0].value,
            "Last_name": form.controls[1].value,
            "Patronymic": form.controls[2].value,
            "Date_of_birth": form.controls[3].value,
            "Passport_number": form.controls[4].value,
            "Email": form.controls[5].value,
            "Gender": form.controls[6].value,
            "Phone_number": form.controls[7].value
        }
        insert_patient(data)
        updated_patients = get_patients()
        nonlocal patients_view
        patients_view = show_data(updated_patients, "Пациенты", patients_columns, patients_aliases, button=register_patient_button)
        show_view(patients_view)

        for control in form.controls:
            if isinstance(control, ft.TextField):
                control.value = ""
            elif isinstance(control, ft.Dropdown):
                control.value = None
        form.update()

    register_patient_view = register_patient_form()

    def register_hospital_form():
        def keep_focus(e):
            e.control.focus()

        form = ft.Column(
            [
                ft.TextField(label="ФИО", hint_text="Введите полное имя", key="full_name", on_change=keep_focus),
                ft.TextField(label="Паспорт", hint_text="Введите серию и номер паспорта", key="passport_data", on_change=keep_focus),
                ft.TextField(label="Диагноз", hint_text="Введите диагноз", key="diagnosis", on_change=keep_focus),
                ft.TextField(label="Дата госпитализации", hint_text="Укажите дату", key="hospitalization_date_time", on_change=keep_focus),
                ft.TextField(label="Код госпитализации", hint_text="Укажите код госпитализации", key="hospitalization_code", on_change=keep_focus),
                ft.ElevatedButton("Создать", on_click=lambda _: register_hospital(form))
            ]
        )
        return form

    def register_hospital(form):
        data = {
            "full_name": form.controls[0].value,
            "passport_data": form.controls[1].value,
            "diagnosis": form.controls[2].value,
            "hospitalization_date_time": form.controls[3].value,
            "hospitalization_code": form.controls[4].value
        }
        insert_hospital(data)
        updated_hospitalizations = get_hospitalizations()
        nonlocal hospitalizations_view
        hospitalizations_view = show_data(updated_hospitalizations, "Госпитализации", hospitalizations_columns, hospitalizations_aliases, button=register_hospital_button)
        show_view(hospitalizations_view)

        for control in form.controls:
            if isinstance(control, ft.TextField):
                control.value = ""
            elif isinstance(control, ft.Dropdown):
                control.value = None
        form.update()

    register_hospital_view = register_hospital_form()

    def register_procedure_form():
        def keep_focus(e):
            e.control.focus()

        form = ft.Column(
            [
                ft.TextField(label="Пациент ID", hint_text="Введите ID пациента", key="patient_id", on_change=keep_focus),
                ft.TextField(label="Дата процедуры", hint_text="Введите дату процедуры", key="Procedure_date", on_change=keep_focus),
                ft.TextField(label="Врач", hint_text="Введите имя врача", key="Doctor", on_change=keep_focus),
                ft.TextField(label="Тип процедуры", hint_text="Введите тип процедуры", key="Procedure_type", on_change=keep_focus),
                ft.TextField(label="Название процедуры", hint_text="Введите название процедуры", key="Procedure_name", on_change=keep_focus),
                ft.ElevatedButton("Создать", on_click=lambda _: register_procedure(form))
            ]
        )
        return form

    def register_procedure(form):
        data = {
            "patient_id": form.controls[0].value,
            "Procedure_date": form.controls[1].value,
            "Doctor": form.controls[2].value,
            "Procedure_type": form.controls[3].value,
            "Procedure_name": form.controls[4].value
        }
        insert_procedures(data)
        updated_procedures = get_medical_procedures()
        nonlocal medical_procedures_view
        medical_procedures_view = show_data(updated_procedures, "Медицинские процедуры", medical_procedures_columns, medical_procedures_aliases, button=register_procedure_button)
        show_view(medical_procedures_view)

        for control in form.controls:
            if isinstance(control, ft.TextField):
                control.value = ""
            elif isinstance(control, ft.Dropdown):
                control.value = None
        form.update()

    register_procedure_view = register_procedure_form()

    main_view = ft.Column(
        [
            ft.Row([
                ft.ElevatedButton("Госпитализации", on_click=lambda _: show_view(hospitalizations_view)),
                ft.ElevatedButton("Медицинские процедуры", on_click=lambda _: show_view(medical_procedures_view)),
                ft.ElevatedButton("Пациенты", on_click=lambda _: show_view(patients_view))
            ], alignment=ft.MainAxisAlignment.CENTER),
            current_view
        ]
    )

    page.add(register_view)

ft.app(target=main)