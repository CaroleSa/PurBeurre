CREATE DATABASE Purbeurre CHARACTER SET 'utf8';

USE Purbeurre;

CREATE TABLE Food(
id INT AUTO_INCREMENT PRIMARY KEY,
name_food VARCHAR(50) NOT NULL,
category VARCHAR(50) NOT NULL,
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

ALTER TABLE Food ADD INDEX ind_nutriscore (nutriscore);

ALTER TABLE Food ADD INDEX ind_category (category);

ALTER TABLE Favorite ADD CONSTRAINT fk_id_food FOREIGN KEY (id_food) REFERENCES Food (id);