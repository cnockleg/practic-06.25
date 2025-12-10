CREATE TABLE IF NOT EXISTS medcards (
    medcard_id   SERIAL PRIMARY KEY,
    patient_id    INTEGER NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    allergies     TEXT,
    diagnosis     BYTEA NOT NULL,
    created_at    TIMESTAMP DEFAULT NOW()
);