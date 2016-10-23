CREATE TABLE classes (
  id SERIAL,
  name varchar(30) NOT NULL UNIQUE,
  description text NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE items (
  id SERIAL,
  name varchar(30) NOT NULL UNIQUE,
  description text NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE ais(
  id SERIAL,
  name varchar(30) NOT NULL UNIQUE,
  description text NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE experiences(
  id SERIAL,
  name varchar(30) NOT NULL UNIQUE,
  description text NOT NULL,
  xp int,
  PRIMARY KEY (id)
);

CREATE TABLE users(
  id SERIAL,
  username varchar(30) NOT NULL UNIQUE,
  password varchar(72) NOT NULL,
  class_id int NOT NULL REFERENCES classes (id),
  created_at timestamp NOT NULL, 
  xp int, 
  hp int, 
  PRIMARY KEY (id)
);

CREATE TABLE users_items(
  user_id int NOT NULL REFERENCES users (id),
  item_id int NOT NULL REFERENCES items (id),
  quantity int, 
  PRIMARY KEY (user_id, item_id)
);

CREATE TABLE users_experiences(
  user_id int NOT NULL REFERENCES users (id),
  experience_id int NOT NULL REFERENCES experiences (id),
  PRIMARY KEY (user_id, experience_id)
);
