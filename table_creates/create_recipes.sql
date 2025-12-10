CREATE TABLE IF NOT EXISTS recipes (
    recipe_id     SERIAL PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    medicines      TEXT,
    recipe_text    TEXT,
    created_at     TIMESTAMP DEFAULT NOW()
);