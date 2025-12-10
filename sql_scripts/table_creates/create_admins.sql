CREATE TABLE IF NOT EXISTS admins (
    admin_id SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    birthdate   DATE,
    gender      CHAR(1),
    email       VARCHAR(255),
    post        VARCHAR(100),
    created_at  TIMESTAMP DEFAULT NOW()
);