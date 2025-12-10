INSERT INTO medcards (patient_id, doctor_id, allergies, diagnosis)
VALUES (<ID_ПАЦИЕНТА>, <ID_ВРАЧА>, '<АЛЛЕРГИИ>', pgp_sym_encrypt('<ДИАГНОЗ>','<ПАРОЛЬ>', 'compress-algo=1, cipher-algo=aes256'));