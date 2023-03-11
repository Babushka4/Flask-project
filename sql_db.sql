CREATE TABLE IF NOT EXISTS User(
    id integer PRIMARY KEY AUTOINCREMENT, 
    login varchar(50) NOT NULL, 
    password text NOT NULL, 
    email varchar(50), 
    name varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Offer(
    id integer PRIMARY KEY AUTOINCREMENT, 
    owner integer NOT NULL, 
    title varchar(50), 
    creation_date date  NULL, 
    info text NOT NULL, 
    FOREIGN KEY (owner) REFERENCES User (id)
);
