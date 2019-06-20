CREATE DATABASE IF NOT EXISTS Purbeurre CHARACTER SET 'utf8';

USE Purbeurre;

CREATE TABLE Food(
id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
name_food VARCHAR(120) NOT NULL UNIQUE,
category_id INT UNSIGNED,
nutriscore VARCHAR(1) NOT NULL,
description VARCHAR(1000),
store VARCHAR(100),
link VARCHAR(300)
);

CREATE TABLE Favorite(
id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
id_food INT UNSIGNED NOT NULL,
id_substitute_chooses INT UNSIGNED NOT NULL
)
ENGINE = InnoDB;

CREATE TABLE Category(
id INT UNSIGNED AUTO_INCREMENT NOT NULL PRIMARY KEY,
categories VARCHAR(50) UNIQUE
);

ALTER TABLE Food
ADD INDEX ind_nutriscore (nutriscore);

ALTER TABLE Food
ADD CONSTRAINT fk_food_id_category FOREIGN KEY (category_id) REFERENCES Category (id);

ALTER TABLE Favorite
ADD CONSTRAINT fk_favorite_id_food FOREIGN KEY (id_food) REFERENCES Food (id);

ALTER TABLE Favorite
ADD CONSTRAINT fk_favorite_substitute_chooses FOREIGN KEY (id_substitute_chooses) REFERENCES Food (id);
