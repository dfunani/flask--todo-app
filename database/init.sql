CREATE TABLE users(
    id serial PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) NOT NULL,
    hashcode VARCHAR(255) NOT NULL
);
CREATE TABLE todo(
    id serial PRIMARY KEY,
    user_id int NOT NULL,
    task VARCHAR(255) NOT NULL,
    created TIMESTAMP NOT NULL,
    status VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
