CREATE DATABASE Purbeurre;

USE Purbeurre;

CREATE TABLE Food(
id INT AUTO_INCREMENT PRIMARY KEY,
name_food VARCHAR(50) NOT NULL,
nutriscore VARCHAR(3) NOT NULL,
description VARCHAR(500),
store VARCHAR(100),
link VARCHAR(300)
);

CREATE TABLE Favorite(
id INT AUTO_INCREMENT PRIMARY KEY,
id_food INT,
substitute_chooses VARCHAR(50) NOT NULL
);

CREATE TABLE Category(
id INT AUTO_INCREMENT NOT NULL UNIQUE,
categories VARCHAR(50)
);

CREATE TABLE Food_category(
id_food INT NOT NULL,
id_category INT NOT NULL
);

ALTER TABLE Category ADD PRIMARY KEY (categories);

ALTER TABLE Food ADD INDEX ind_nutriscore (nutriscore);

ALTER TABLE Favorite ADD CONSTRAINT fk_favorite_id_food FOREIGN KEY (id_food) REFERENCES Food (id);

ALTER TABLE Food_category ADD CONSTRAINT fk_food_category_id_food FOREIGN KEY (id_food) REFERENCES Food (id);

ALTER TABLE Food_category ADD CONSTRAINT fk_food_category_id_category FOREIGN KEY (id_category) REFERENCES Category (id);