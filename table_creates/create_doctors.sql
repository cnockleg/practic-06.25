CREATE TABLE IF NOT EXISTS doctors (
    doctor_id     SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    birthdate     DATE,
    gender        CHAR(1),
    experience    INTEGER CHECK (experience >= 0),
    specialization VARCHAR(100),
    created_at    TIMESTAMP DEFAULT NOW()
);