CREATE TABLE IF NOT EXISTS patients (
    patient_id  SERIAL PRIMARY KEY,
    doctor_id   INTEGER REFERENCES doctors(doctor_id) ON DELETE SET NULL,
    name        VARCHAR(100) NOT NULL,
    birthdate   DATE,
    gender      CHAR(1),
    phone       VARCHAR(20),
    created_at  TIMESTAMP DEFAULT NOW()
);