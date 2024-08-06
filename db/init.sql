CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    source VARCHAR(255),
    title VARCHAR(255),
    url TEXT UNIQUE,
    time VARCHAR(255),
    category VARCHAR(255)
);
