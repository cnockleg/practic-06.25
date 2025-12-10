import time

import psycopg2
from psycopg2 import sql
from psycopg2 import OperationalError
from tabulate import tabulate



def connect_with_failover(dbname, user, password, host="localhost", ports=[5432, 5433, 5434], retry=True):
    conn = None
    while True:
        for port in ports:
            try:
                print(f"\nПодключение к localhost:{port}...")
                conn = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                print(f"Успешное подключение к порту {port}\n")
                return conn
            except OperationalError:
                print(f"Не удалось подключиться к порту {port}")
        if not retry:
            return None
        print("Повтор через 5 секунд\n")
        time.sleep(5)


def connect_to_db(user="postgres", password=101010, dbname="medical_cards", host="localhost", ports=[5432, 5433]):
    return connect_with_failover(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        ports=ports,
        retry=True
    )




# Создание таблиц
# -------------------------------------------------------------------------------

def create_admins_table():
    conn = connect_to_db()
    cur = conn.cursor()
    
    with open('table_creates\create_admins.sql', 'r', encoding='utf-8') as f:
        script = f.read()
    cur.execute(script)

    conn.commit()
    cur.close()
    conn.close()



def create_doctors_table():
    conn = connect_to_db()
    cur = conn.cursor()
    
    with open('table_creates\create_doctors.sql', 'r', encoding='utf-8') as f:
        script = f.read()
    cur.execute(script)

    conn.commit()
    cur.close()
    conn.close()



def create_patients_table():
    conn = connect_to_db()
    cur = conn.cursor()
    
    with open('table_creates\create_patients.sql', 'r', encoding='utf-8') as f:
        script = f.read()
    cur.execute(script)

    conn.commit()
    cur.close()
    conn.close()



def create_medcards_table():
    conn = connect_to_db()
    cur = conn.cursor()
    
    with open('table_creates\create_medcards.sql', 'r', encoding='utf-8') as f:
        script = f.read()
    cur.execute(script)

    conn.commit()
    cur.close()
    conn.close()



def create_appointments_table():
    conn = connect_to_db()
    cur = conn.cursor()
    
    with open('table_creates\create_appointments.sql', 'r', encoding='utf-8') as f:
        script = f.read()
    cur.execute(script)

    conn.commit()
    cur.close()
    conn.close()



def create_recepies_table():
    conn = connect_to_db()
    cur = conn.cursor()
    
    with open('table_creates\create_recepies.sql', 'r', encoding='utf-8') as f:
        script = f.read()
    cur.execute(script)

    conn.commit()
    cur.close()
    conn.close()



# Заполнение таблиц
# ---------------------------------------------------------------------------------------------------------

def insert_admin(name, birthdate, gender, email, post):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO admins (name, birthdate, gender, email, post) VALUES (%s, %s, %s, %s, %s) RETURNING admin_id;",
        (name, birthdate, gender, email, post)
    )
    new_admin_id = cur.fetchone()[0]

    conn.commit()
    print("добавлен администратор: ", new_admin_id)
    cur.close()
    conn.close()
    return new_admin_id



def insert_doctor(name, birthdate, gender, experience, specialization):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO doctors (name, birthdate, gender, experience, specialization) VALUES (%s, %s, %s, %s, %s) RETURNING doctor_id;",
        (name, birthdate, gender, experience, specialization)
    )
    new_doctor_id = cur.fetchone()[0]

    conn.commit()
    print("добавлен врач: ", new_doctor_id)
    cur.close()
    conn.close()
    return new_doctor_id



def insert_patient(name, birthdate, gender, phone, doctor_name):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT doctor_id FROM doctors WHERE name = %s;", (doctor_name,))
    doctor = cur.fetchone()

    if not doctor:
        print(f"Врач с именем '{doctor_name}' не найден.")
        conn.close()
        return None
    doctor_id = doctor[0]

    cur.execute(
        "INSERT INTO patients (doctor_id, name, birthdate, gender, phone) VALUES (%s, %s, %s, %s, %s) RETURNING patient_id;",
        (doctor_id, name, birthdate, gender, phone)
    )
    new_patient_id = cur.fetchone()[0]

    conn.commit()
    print("добавлен пациент: ", new_patient_id)
    cur.close()
    conn.close()
    return new_patient_id



def insert_medcard(patient_name, allergies, diagnosis):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT patient_id FROM patients WHERE name = %s;", (patient_name,))
    patient = cur.fetchone()

    if not patient:
        print(f"Пациент с именем '{patient_name}' не найден.")
        conn.close()
        return None
    patient_id = patient[0]

    cur.execute(
        "INSERT INTO medcards (patient_id, allergies, diagnosis) VALUES (%s, %s, pgp_sym_encrypt(%s,'F2388451B0954326','compress-algo=1, cipher-algo=aes256')) RETURNING medcard_id",
        (patient_id, allergies, diagnosis)
    )
    new_medcard_id = cur.fetchone()[0]

    conn.commit()
    print("добавлена карта: ", new_medcard_id)
    cur.close()
    conn.close()
    return new_medcard_id




def insert_appointment(patient_name, doctor_name, appointment_date, reason, result):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT patient_id FROM patients WHERE name = %s;", (patient_name,))
    patient = cur.fetchone()
    
    if not patient:
        print(f"Пациент с именем '{patient_name}' не найден.")
        conn.close()
        return None
    patient_id = patient[0]

    cur.execute("SELECT medcard_id FROM medcards WHERE patient_id = %s ORDER BY created_at DESC LIMIT 1;", (patient_id,))
    medcard = cur.fetchone()

    if not medcard:
        print(f"Медкарта {patient_name} не найдена")
        return None
    medcard_id = medcard[0]

    cur.execute("SELECT doctor_id FROM doctors WHERE name = %s;", (doctor_name,))
    doctor = cur.fetchone()

    if not doctor:
        print(f"Врач с именем '{doctor_name}' не найден.")
        conn.close()
        return None
    doctor_id = doctor[0]

    cur.execute(
        "INSERT INTO appointments (medcard_id, doctor_id, appointment_date, reason, result) VALUES (%s, %s, %s, %s, %s) RETURNING appointment_id;",
        (medcard_id, doctor_id, appointment_date, reason, result)
    )
    new_appointment_id = cur.fetchone()[0]

    conn.commit()
    print("добавлена запись: ", new_appointment_id)
    cur.close()
    conn.close()
    return new_appointment_id



def get_appointment(patient_name):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT a.appointment_id, a.appointment_date
        FROM appointments a
        JOIN medcards m ON a.medcard_id = m.medcard_id
        JOIN patients p ON m.patient_id = p.patient_id
        WHERE p.name = %s
        ORDER BY a.appointment_date DESC
        LIMIT 10;
        """,    
        (patient_name,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
        


def insert_recipe(appointment_id, medicines, recipe_text):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO recipes (appointment_id, medicines, recipe_text) VALUES (%s, %s, %s) RETURNING recipe_id",
        (appointment_id, medicines, recipe_text)
    )
    recipe_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    return recipe_id



# Обновление данных
# -----------------------------------------------------------------------------------------------------------------

def update_admin(admin_name, col_name, new_value):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT admin_id FROM admins WHERE name = %s", (admin_name,))
    admin = cur.fetchone()

    if not admin:
        print(f"Администратор с ID {admin_name} не найден.")
        cur.close()
        conn.close()
        return None
    admin_id = admin[0]


    query = sql.SQL("UPDATE admins SET {col} = %s WHERE admin_id = %s").format(col=sql.Identifier(col_name))
    cur.execute(query, (new_value, admin_id))

    conn.commit()
    print(f"Значение {col_name} у администратора {admin_name} изменено на {new_value}")
    cur.close()
    conn.close()


    
def update_doctor(doctor_name, col_name, new_value):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT doctor_id FROM doctors WHERE name = %s", (doctor_name,))
    doctor = cur.fetchone()

    if not doctor:
        print(f"Врач с ID {doctor_name} не найден.")
        cur.close()
        conn.close()
        return None
    doctor_id = doctor[0]

    query = sql.SQL("UPDATE doctors SET {col} = %s WHERE doctor_id = %s").format(col=sql.Identifier(col_name))
    cur.execute(query, (new_value, doctor_id))

    conn.commit()
    print(f"Значение {col_name} у врача {doctor_name} изменено на {new_value}")
    cur.close()
    conn.close()



def update_patient(patient_name, col_name, new_value):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT admin_id FROM admins WHERE admin_id = %s", (patient_name,))
    patient = cur.fetchone()

    if not patient:
        print(f"Пациент с ID {patient_name} не найден.")
        cur.close()
        conn.close()
        return None
    patient_id = patient[0]

    query = sql.SQL("UPDATE patients SET {col} = %s WHERE patient_id = %s").format(col=sql.Identifier(col_name))
    cur.execute(query, (new_value, patient_id))

    conn.commit()
    print(f"Значение {col_name} у пацента {patient_name} изменено на {new_value}")
    cur.close()
    conn.close()



def update_medcard(patient_name, col_name, new_value):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT patient_id FROM patients WHERE name = %s;", (patient_name,))
    patient = cur.fetchone()

    if not patient:
        print(f"Пациент с именем '{patient_name}' не найден.")
        cur.close()
        conn.close()
        return None
    patient_id = patient[0]

    cur.execute("SELECT medcard_id FROM medcards WHERE patient_id = %s;", (patient_id,))
    medcard = cur.fetchone()

    if not medcard:
        print(f"Медкарта пациента {patient_name} не найдена.")
        cur.close()
        conn.close()
        return None
    medcard_id = medcard[0]

    if col_name == "diagnosis":
        query = sql.SQL("UPDATE medcards SET {col} = pgp_sym_encrypt(%s, 'F2388451B0954326', 'compress-algo=1, cipher-algo=aes256') WHERE medcard_id = %s").format(col=sql.Identifier(col_name))
    else:
        query = sql.SQL("UPDATE medcards SET {col} = %s WHERE medcard_id = %s").format(col=sql.Identifier(col_name))

    cur.execute(query, (new_value, medcard_id))

    conn.commit()
    print(f"Значение {col_name} в медкарте пациента {patient_name} изменено на {new_value}")
    cur.close()
    conn.close()



def update_appointment(patient_name, doctor_name, col_name, new_value):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT patient_id FROM patients WHERE name = %s;", (patient_name,))
    patient = cur.fetchone()
    
    if not patient:
        print(f"Пациент с именем '{patient_name}' не найден.")
        cur.close()
        conn.close()
        return None
    patient_id = patient[0]    

    cur.execute("SELECT medcard_id FROM medcards WHERE patient_id = %s ORDER BY created_at DESC LIMIT 1;", (patient_id,))
    medcard = cur.fetchone()

    if not medcard:
        print(f"Медкарта {patient_name} не найдена")
        cur.close()
        conn.close()
        return None
    medcard_id = medcard[0]

    cur.execute("SELECT doctor_id FROM doctors WHERE name = %s;", (doctor_name,))
    doctor = cur.fetchone()

    if not doctor:
        print(f"Врач с именем '{doctor_name}' не найден.")
        cur.close()
        conn.close()
        return None
    doctor_id = doctor[0]

    cur.execute("SELECT appointment_id FROM appointments WHERE medcard_id = %s AND doctor_id = %s;", (medcard_id, doctor_id))
    appointment = cur.fetchone()    

    if not appointment:
        print(f"Запись на прием не найдена")
        cur.close()
        conn.close()
        return None
    appointment_id = appointment[0]

    query = sql.SQL("UPDATE appointments SET {col} = %s WHERE appointment_id = %s").format(col=sql.Identifier(col_name))
    cur.execute(query, (new_value, appointment_id))

    conn.commit()
    print(f"Значение {col_name} в записи на прием пациента {patient_name} изменено на {new_value}")
    cur.close()
    conn.close()



def update_recipe(patient_name, col_name, new_value):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT patient_id FROM patients WHERE name = %s;", (patient_name,))
    patient = cur.fetchone()[0]
    
    if not patient:
        print(f"Пациент с именем '{patient_name}' не найден.")
        cur.close()
        conn.close()
        return None
    patient_id = patient[0]

    cur.execute("SELECT medcard_id FROM medcards WHERE patient_id = %s ORDER BY created_at DESC LIMIT 1;", (patient_id,))
    medcard = cur.fetchone()

    if not medcard:
        print(f"Медкарта {patient_name} не найдена")
        cur.close()
        conn.close()
        return None
    medcard_id = medcard[0]

    cur.execute("SELECT appointment_id FROM appointments WHERE medcard_id = %s;", (medcard_id,))
    appointment = cur.fetchone()

    if not appointment:
        print(f"Записи {patient_name} не найдены")
        cur.close()
        conn.close()
        return None
    appointment_id = appointment[0]

    cur.execute("SELECT recipe_id FROM recipes WHERE appointment_id = %s;", (appointment_id,))
    recipe = cur.fetchone()

    if not recipe:
        print(f"Рецепты для {patient_name} не найдены")
        cur.close()
        conn.close()
        return None
    recipe_id = recipe[0]

    query = sql.SQL("UPDATE recipes SET {col} = %s WHERE recipe_id = %s").format(col=sql.Identifier(col_name))
    cur.execute(query, (new_value, recipe_id))

    conn.commit()
    print(f"Значение {col_name} в рецепте пациента {patient_name} изменено на {new_value}")
    cur.close()
    conn.close()



# Удаление данных
# -----------------------------------------------------------------------------------------------------------------------

def delete_row(table_name, creation_date):
    conn = connect_to_db()
    cur = conn.cursor()

    date_column = "created_at"

    query = sql.SQL("SELECT * FROM {table} WHERE DATE({col}) = %s").format(
        table=sql.Identifier(table_name),
        col=sql.Identifier(date_column)
    )
    cur.execute(query, (creation_date,))
    rows = cur.fetchall()

    if not rows:
        print("Записей за эту дату не найдено.")
        cur.close()
        conn.close()
        return

    print(f"\nЗаписи из таблицы '{table_name}' за {creation_date}:")
    for i, row in enumerate(rows):
        print(f'{i+1}) {row}')
    
    try:
        choice = int(input("\nВведите номер записи для удаления: ")) - 1
        if choice < 0 or choice >= len(rows):
            print("Неверный выбор.")
            return
    except ValueError:
        print("Ожидался номер.")
        return
    
    if input("Для подтверждения удаления введите ответ на 19*4: ") == "76":
        print("Удаление...")
    else:
        print("Неверно")
        return

    id_column = table_name[0:-1] + "_id"
    record_id = rows[choice][0]

    delete = sql.SQL("DELETE FROM {table} WHERE {id_col} = %s").format(
        table = sql.Identifier(table_name),
        id_col = sql.Identifier(id_column)
    )
    cur.execute(delete, (record_id,))

    conn.commit()
    print(f"Запись удалена из {table_name}: {record_id}")
    cur.close()
    conn.close()




# Просмотр данных
# ----------------------------------------------------------------------------------------------------------------------

def check_data(table_name):
    conn = connect_to_db()
    cur = conn.cursor()

    query = sql.SQL("SELECT * FROM {name}").format(name = sql.Identifier(table_name))
    cur.execute(query,)
    rows = cur.fetchall()

    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position", [table_name])
    headers = [col[0] for col in cur.fetchall()]

    print(tabulate(rows, headers, tablefmt='rounded_grid', maxcolwidths=[None, None, None, 55, None]))
    cur.close()
    conn.close()



def decrypt_diagnosis(patient_name, passphrase):
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT patient_id FROM patients WHERE name = %s;", (patient_name,))
    patient = cur.fetchone()
    
    if not patient:
        print(f"Пациент с именем '{patient_name}' не найден.")
        cur.close()
        conn.close()
        return None
    patient_id = patient[0]

    cur.execute("SELECT medcard_id FROM medcards WHERE patient_id = %s;", (patient_id,))
    medcard = cur.fetchone()

    if not medcard:
        print(f"Медкарта пациента {patient_name} не найдена.")
        cur.close()
        conn.close()
        return None
    medcard_id = medcard[0]

    cur.execute("SELECT pgp_sym_decrypt(diagnosis, %s)::text FROM medcards WHERE medcard_id = %s;", (passphrase, medcard_id))
    result = cur.fetchone()

    print(result[0])
    cur.close()
    conn.close()
    

# Дополнительные функции
# ----------------------------------------------------------------------------------------------------------------------

def create_indexes():
    conn = connect_to_db()
    cur = conn.cursor()
    
    with open('index_creates\create_index_onappointmentdate.sql', 'r', encoding='utf-8') as f:
        script = f.read()
    cur.execute(script)
    with open('index_creates\create_index_onpatients.sql', 'r', encoding='utf-8') as f:
        script = f.read()
    cur.execute(script)

    conn.commit()
    print("индексы созданы")
    cur.close()
    conn.close()



def create_extensions():
    conn = connect_to_db()
    cur = conn.cursor()

    with open('extensions_creates\creating_extensions.sql', 'r', encoding='utf-8') as f:
        script = f.read()
    cur.execute(script)

    conn.commit()
    print("расширения добавлены")
    cur.close()
    conn.close()

# ----------------------------------------------------------------------------------------------------------------------

# create_indexes()
# create_extensions()


