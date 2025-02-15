-- init
-- depends: 

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    segment TEXT NOT NULL,
    phone TEXT  NOT NULL
);

INSERT INTO customers(name, segment, phone) VALUES
    ('Akhil', 'travel', '+91 9876543210'),
    ('Bhushan', 'movies', '+91 9876543210');
