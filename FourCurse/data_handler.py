from db_connection import connect_to_db, execute_query

def get_hospitalizations():
    connection = connect_to_db()
    if connection:
        query = "SELECT * FROM hospitalizations"
        result = execute_query(connection, query)
        connection.close()
        return result
    return []

def get_medical_procedures():
    connection = connect_to_db()
    if connection:
        query = "SELECT * FROM medical_procedures"
        result = execute_query(connection, query)
        connection.close()
        return result
    return []

def get_patients():
    connection = connect_to_db()
    if connection:
        query = "SELECT * FROM patients"
        result = execute_query(connection, query)
        connection.close()
        return result
    return []

def insert_patient(data):
    connection = connect_to_db()
    if connection:
        query = """
        INSERT INTO patients (First_name, Last_name, Patronymic, Date_of_birth, Passport_number, Email, Gender, Phone_number)
        VALUES (%(First_name)s, %(Last_name)s, %(Patronymic)s, %(Date_of_birth)s, %(Passport_number)s, %(Email)s, %(Gender)s, %(Phone_number)s)
        """
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()

def insert_hospital(data):
    connection = connect_to_db()
    if connection:
        query = """
        INSERT INTO hospitalizations (full_name, passport_data, diagnosis, hospitalization_date_time, hospitalization_code)
        VALUES (%(full_name)s, %(passport_data)s, %(diagnosis)s, %(hospitalization_date_time)s, %(hospitalization_code)s)
        """
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()

def insert_procedures(data):
    connection = connect_to_db()
    if connection:
        query = """
        INSERT INTO medical_procedures (patient_id, Procedure_date, Doctor, Procedure_type, Procedure_name)
        VALUES (%(patient_id)s, %(Procedure_date)s, %(Doctor)s, %(Procedure_type)s, %(Procedure_name)s)
        """
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()