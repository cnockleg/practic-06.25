CREATE TABLE IF NOT EXISTS appointments (
    appointment_id   SERIAL PRIMARY KEY,
    medcard_id      INTEGER NOT NULL REFERENCES medcards(medcard_id) ON DELETE CASCADE,
    doctor_id        INTEGER NOT NULL REFERENCES doctors(doctor_id) ON DELETE SET NULL,
    appointment_date TIMESTAMP NOT NULL,
    reason           TEXT,
    result           TEXT,
    created_at       TIMESTAMP DEFAULT NOW()
);