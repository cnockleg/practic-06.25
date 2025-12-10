import datetime
import main

def admin_panel():
    user_check = input("Введите пароль: ")
    if user_check == "doctor1010":
        user = "doctor"
    elif user_check == "admin1010":
        user = "admin"
    elif user_check == "dev1010":
        user = "developer"
    else:
        print("Неправильный пароль. Доступ запрещён.")
        return

    print("Добро пожловать в панель управления медкартами, что вы хотите сделать?")

    while True:
        action = int(input(
            "\n\n\n1) Добавить запись в таблицу\n" \
            "2) Изменить запись в таблице\n" \
            "3) Удалить запись из таблицы\n" \
            "4) Посмотреть записи\n" \
            "5) Узнать диагноз пациента\n\n" \
            "6) Руководство пользователя\n\n" \
            "0) Завершить работу\n\n\n"))



        if action == 0:
            print("Выход...")
            break



        if action == 1:
            print("\n Выберите таблицу, в которую хотите добавить запись: ")
            stradd_choise = int(input(
                "1) Администрация\n" \
                "2) Врачи\n" \
                "3) Пациенты\n" \
                "4) Медкарты\n" \
                "5) Назначения\n" \
                "6) Рецепты\n\n" \
                "0) Выйти\n\n\n"
            ))


            if stradd_choise == 0:
                print("Выход...")
                continue            


            if stradd_choise == 1:
                if user != "developer":
                    print("Доступ запрещен")
                else:
                    print("Введите данные администратора: \n")
                    name = input("Введите ФИО: ")
                    date_str = input("Введите дату рождения: ")
                    birthdate = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
                    gender = input("Введите пол (М/Ж): ")
                    email = input("Введите рабочую почту: ")
                    post = input("Введите должность: ")

                    main.insert_admin(name, birthdate, gender, email, post)
            
            if stradd_choise == 2:
                if user == "doctor":
                    print("Доступ запрещен")
                else:
                    print("Введите данные врача: \n")
                    name = input("Введите ФИО: ")
                    date_str = input("Введите дату рождения: ")
                    birthdate = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
                    gender = input("Введите пол (М/Ж): ")
                    experience = input("Введите опыт работы в годах: ")
                    specialization = input("Введите область специализации: ")
                    
                    main.insert_doctor(name, birthdate, gender, experience, specialization)

            if stradd_choise == 3:
                if user == "doctor":
                    print("Доступ запрещен")
                else:
                    print("Введите данные пациента: \n")
                    name = input("Введите ФИО: ")
                    date_str = input("Введите дату рождения: ")
                    birthdate = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
                    gender = input("Введите пол (М/Ж): ")
                    phone = input("Введите номер телефона: ")
                    doctor_name = input("Введите ФИО врача, привязываемого к пациенту: ")
                    
                    main.insert_patient(name, birthdate, gender, phone, doctor_name)

            if stradd_choise == 4:
                if user == "admin":
                    print("Доступ запрещен")
                else:
                    print("Введите данные для медкарты: \n")
                    patient_name = input("Введите ФИО пацента: ")
                    # doctor_name = input("Введите ФИО врача: ")
                    allergies = input("Введите аллергии пациента: ")
                    diagnosis = input("Введите диагноз пациента: ")
                    
                    main.insert_medcard(patient_name, allergies, diagnosis)

            if stradd_choise == 5:
                if user == "admin":
                    print("Доступ запрещен")
                else:
                    print("Введите данные назначения: \n")
                    patient_name = input("Введите ФИО пацента: ")
                    doctor_name = input("Введите ФИО врача: ")
                    date_str = input("Введите дату и время назначения: ")
                    appointment_date = datetime.datetime.strptime(date_str, "%d.%m.%Y %H:%M")
                    reason = input("Введите цель назначения: ")
                    
                    main.insert_appointment(patient_name, doctor_name, appointment_date, reason, result="Ожидается")

            if stradd_choise == 6:
                if user == "admin":
                    print("Доступ запрещен")
                else:
                    patient_name = input("Введите имя пациента для создания рецепта: ")
                    appointments = main.get_appointment(patient_name)

                    for idx, (app_id, date) in enumerate(appointments):
                        print(f"{idx + 1}) {date.strftime('%d.%m.%Y')}")
                    
                    chosen_index = int(input("Выберите номер приёма: ")) - 1
                    appointment_id = appointments[chosen_index][0]

                    medicines = input("Введите выписанные препараты: ")
                    recipe_text = input("Введите полный текст рецепта: ")
                    
                    main.insert_recipe(appointment_id, medicines, recipe_text)        
            


        if action == 2:
            print("\n Выберите таблицу, запись в которой хотите изменить: ")
            strchng_choise = int(input(
                "1) Администрация\n" \
                "2) Врачи\n" \
                "3) Пациенты\n" \
                "4) Медкарты\n" \
                "5) Назначения\n" \
                "6) Рецепты\n\n" \
                "0) Выйти\n\n\n"
            ))


            if strchng_choise == 0:
                print("Выход...")
                continue


            if strchng_choise == 1:
                if user == "doctor":
                    print("Доступ запрещен")
                else:
                    name = input("Введите ФИО администратора: ")
                    column = input("Введите название колонки для изменения: ")
                    new_val = input("Введите новое значение: ")

                    main.update_admin(name, column, new_val)
            
            if strchng_choise == 2:
                if user == "doctor":
                    print("Доступ запрещен")
                else:
                    name = input("Введите ФИО врача: ")
                    column = input("Введите название колонки для изменения: ")
                    new_val = input("Введите новое значение: ")

                    main.update_doctor(name, column, new_val)

            if strchng_choise == 3:
                if user == "doctor":
                    print("Доступ запрещен")
                else:
                    name = input("Введите ФИО пациента: ")
                    column = input("Введите название колонки для изменения: ")
                    new_val = input("Введите новое значение: ")

                    main.update_patient(name, column, new_val)


            if strchng_choise == 4:
                if user == "admin":
                    print("Доступ запрещен")
                else:
                    patient_name = input("Введите ФИО пацента: ")
                    doctor_name = input("Введите ФИО врача: ")
                    column = input("Введите название колонки для изменения: ")
                    new_val = input("Введите новое значение: ")
                    
                    main.update_medcard(patient_name, doctor_name, column, new_val)

            if strchng_choise == 5:
                if user == "admin":
                    print("Доступ запрещен")
                else:
                    patient_name = input("Введите ФИО пацента: ")
                    doctor_name = input("Введите ФИО врача: ")
                    column = input("Введите название колонки для изменения: ")
                    new_val = input("Введите новое значение: ")
                    
                    main.update_appointment(patient_name, doctor_name, column, new_val)

            if strchng_choise == 6:
                if user == "admin":
                    print("Доступ запрещен")
                else:
                    name = input("Введите ФИО пациента: ")
                    column = input("Введите название колонки для изменения: ")
                    new_val = input("Введите новое значение: ")

                    main.update_recipe(name, column, new_val)



        if action == 3:
            print("\n Выберите таблицу, запись в которой хотите удалить: ")
            strdel_choise = int(input(
                "1) Администрация\n" \
                "2) Врачи\n" \
                "3) Пациенты\n" \
                "4) Медкарты\n" \
                "5) Назначения\n" \
                "6) Рецепты\n\n" \
                "0) Выйти\n\n\n"
            ))        



            if strdel_choise == 0:
                print("Выход...")
                continue


            if strdel_choise == 1:
                date_str = input("Введите дату, запись по которой необходимо удалить: ")
                date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

                main.delete_row("admins", date)

            if strdel_choise == 2:
                date_str = input("Введите дату, запись по которой необходимо удалить: ")
                date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

                main.delete_row("doctors", date)            

            if strdel_choise == 3:
                date_str = input("Введите дату, запись по которой необходимо удалить: ")
                date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

                main.delete_row("patients", date)   

            if strdel_choise == 4:
                date_str = input("Введите дату, запись по которой необходимо удалить: ")
                date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

                main.delete_row("medcards", date)   

            if strdel_choise == 5:
                date_str = input("Введите дату, запись по которой необходимо удалить: ")
                date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

                main.delete_row("appointments", date)   

            if strdel_choise == 6:
                date_str = input("Введите дату, запись по которой необходимо удалить: ")
                date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

                main.delete_row("recipes", date)   



        if action == 4:
            print("\n Выберите таблицу, которую хотите просмотреть: ")
            strchk_choise = int(input(
                "1) Администрация\n" \
                "2) Врачи\n" \
                "3) Пациенты\n" \
                "4) Медкарты\n" \
                "5) Назначения\n" \
                "6) Рецепты\n\n" \
                "0) Выйти\n\n\n"
            ))           


            if strchk_choise == 0:
                print("Выход...")
                continue
            

            if strchk_choise == 1:
                main.check_data("admins")

            if strchk_choise == 2:
                main.check_data("doctors")

            if strchk_choise == 3:
                main.check_data("patients")

            if strchk_choise == 4:
                main.check_data("medcards")

            if strchk_choise == 5:
                main.check_data("appointments")

            if strchk_choise == 6:
                main.check_data("recipes")



        if action == 5:
            if user == "admin":
                print("Доступ запрещен")

            name = input("Введите имя пациента для просмотра диагноза: ")
            passkey = input("Введите ключ безопасности: ")

            if passkey == 'F2388451B0954326':
                main.decrypt_diagnosis(name, passkey)
            else:
                print("Неверный ключ")
                return
            
            


        if action == 6:
            with open('user_guide.txt', encoding='utf-8', errors='replace') as f:
                print(f"\n{f.read()}")
                continue


admin_panel()
