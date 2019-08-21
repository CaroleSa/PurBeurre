#! /usr/bin/env python3
# coding: UTF-8

""" Class Database """



# imports
import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared

import call_api as ca
import orm



class Database:
    """ Creation database and insert data """

    def __init__(self):
        """ Connection at MySQL and creation of cursor """
        # instantiate the class Orm
        self.new_orm = orm.Orm()

        # read the file connection.yml
        with open('connection.yml', 'r') as file:
            self.info = file.read().split()

        # connection at MySQL with data of connection.yml file and creation cursor
        self.data_base = mysql.connector.connect(user=self.info[0], password=self.info[1],
                                                 host=self.info[2])
        self.cursor = self.data_base.cursor()

    def creation_database(self):
        """ Running file "base.sql" requests : for the creation of the database """
        with open("base.sql", "r") as file:
            base = file.read()
            self.cursor.execute(base)

        # call Database method to insert data
        self.insert_data()

    def connection_database(self):
        """ Connection at MySQL and use database """
        # connection to the database
        self.data_base = mysql.connector.connect(user=self.info[0], password=self.info[1],
                                                 host=self.info[2])
        self.cursor = self.data_base.cursor()

        # executed "use Purbeurre" request
        self.cursor.execute("USE Purbeurre")

    def insert_data(self):
        """ Inserting data into the database """
        self.connection_database()

        # no insertion if the table Food already contains any data
        self.cursor.execute("SELECT * FROM Food")
        data_table_food = self.cursor.fetchall()
        if not data_table_food:

            # instantiate the class Call_api
            new_call_api = ca.CallApi()
            new_call_api.load_data()
            categories = new_call_api.categories
            list_data = new_call_api.list_data

            for elt, element in zip(categories, list_data):

                # inserting data into Category table
                insert_data_categories = ("""INSERT IGNORE INTO Category (categories)
                                          VALUES({0})"""
                                          .format("\'"+elt+"\'"))
                self.cursor.execute(insert_data_categories)
                self.data_base.commit()

                # inserting data into Food table
                for value in element['products']:
                    if element['products'].index(value) < 100:
                        try:
                            product_name = "\'"+value['product_name_fr'].replace("'", "")+"\'"
                            nutrition_grade = "\'"+value['nutrition_grade_fr'].replace("'", "")+"\'"
                            ingredients = "\'"+value['ingredients_text'].replace("'", "")+"\'"
                            store_tags = "\'"+", ".join(value['stores_tags']).replace("'", "")+"\'"
                            url = "\'"+value['url'].replace("'", "")+"\'"

                            insert_data_food = ("""INSERT IGNORE INTO Food (name_food, category_id,
                                                nutriscore, description, store, link) 
                                                VALUES({0}, 
                                                (SELECT id FROM Category WHERE categories = {1}),
                                                {2}, {3}, {4}, {5})"""
                                                .format(product_name, "\'"+elt+"\'",
                                                        nutrition_grade, ingredients,
                                                        store_tags, url))
                            self.cursor.execute(insert_data_food)
                            self.data_base.commit()

                        # if errors
                        except KeyError:
                            continue

    def select_categories_database(self):
        """ use database to selected the id and name of categories
        and call orm """
        # connection to the database
        self.cursor = self.data_base.cursor(MySQLCursorPrepared)
        self.cursor.execute("USE Purbeurre")
        self.cursor.execute("SELECT id, categories FROM Category ORDER BY id")
        id_name_categories = self.cursor.fetchall()
        id_name_categories = self.new_orm.transform_categories_to_object(id_name_categories)
        return id_name_categories

    def select_foods_database(self, user_answer_id_category):
        """ use database to selected the id and name of foods
        and call orm """
        self.cursor = self.data_base.cursor(MySQLCursorPrepared)
        self.cursor.execute("""SELECT id, name_food
                            FROM Food
                            WHERE category_id = {}""".format(user_answer_id_category))
        id_name_food = self.cursor.fetchall()
        id_name_food = self.new_orm.transform_foods_to_object(id_name_food)
        return id_name_food

    def select_substitute(self, user_answer_id_category, user_answer_id_food, read_line_substitute):
        """ use database to selected the name and nutriscore of food chooses,
        the information of its substitute and call orm"""
        self.cursor = self.data_base.cursor(MySQLCursorPrepared)
        self.cursor.execute("""SELECT (SELECT name_food FROM Food WHERE id = {1}),
                            (SELECT nutriscore FROM Food WHERE id = {1}), 
                            name_food, nutriscore, description, store, link
                            FROM Food
                            WHERE category_id = {0}
                            ORDER BY nutriscore LIMIT {2},1""" \
                            .format(user_answer_id_category,
                                    user_answer_id_food,
                                    read_line_substitute))
        info_food_chooses_and_substitute = self.cursor.fetchall()
        info_food_chooses_and_substitute = self.new_orm.transform_substitute_to_object\
            (info_food_chooses_and_substitute)
        info_food_chooses = info_food_chooses_and_substitute[0]
        info_substitute = info_food_chooses_and_substitute[1]
        return info_substitute, info_food_chooses

    def insert_favorite_food(self, user_answer_id_food, name_substitute):
        """ use database to save favorite food and its substitute """
        self.cursor = self.data_base.cursor(MySQLCursorPrepared)
        save_favorite_food = """INSERT INTO Favorite
                                (id_food, id_substitute_chooses)
                                VALUES({0}, 
                                (SELECT id FROM Food WHERE name_food = {1}))""" \
                                .format(int(user_answer_id_food),
                                        "\'" + name_substitute + "\'")
        self.cursor.execute(save_favorite_food)
        self.data_base.commit()

    def select_favorite_foods(self):
        """ use database to select the name of favorite foods,
        the id and the name of substitutes and call orm"""
        self.cursor = self.data_base.cursor(MySQLCursorPrepared)
        self.cursor.execute("USE Purbeurre")
        self.cursor.execute("""SELECT Favorite.id, Food.name_food
                            FROM Food 
                            JOIN Favorite ON Food.id = Favorite.id_substitute_chooses 
                            WHERE Food.id = Favorite.id_substitute_chooses
                            ORDER BY Favorite.id""")
        id_name_substitute = self.cursor.fetchall()
        self.cursor.execute("""SELECT Food.name_food
                            FROM Food
                            JOIN Favorite ON Food.id = Favorite.id_food
                            WHERE Food.id = Favorite.id_food
                            ORDER BY Favorite.id""")
        name_substituted_food = self.cursor.fetchall()
        substituted_food_substitute = self.new_orm.transform_favorite_foods_to_object\
            (id_name_substitute, name_substituted_food)
        id_substitute = substituted_food_substitute[0]
        name_substitute = substituted_food_substitute[1]
        name_substituted_food = substituted_food_substitute[2]
        return id_substitute, name_substituted_food, name_substitute

    def select_detail_substitute(self, user_answer_choice_id_substitute):
        """ use database to select the substitute information and call orm """
        self.cursor = self.data_base.cursor(MySQLCursorPrepared)
        self.cursor.execute("""SELECT name_food, nutriscore, description, store, link
                            FROM Food 
                            WHERE id = 
                            (SELECT id_substitute_chooses FROM Favorite WHERE id = {})"""
                            .format(int(user_answer_choice_id_substitute)))
        info_substitute = self.cursor.fetchall()
        info_substitute = self.new_orm.transform_detail_substitute_to_object(info_substitute)
        return info_substitute

    def delete_favorite_food(self, user_answer_choice_id_substitute):
        """ use database to delete favorite food """
        self.cursor = self.data_base.cursor(MySQLCursorPrepared)
        self.cursor.execute("""DELETE FROM Favorite where id = {}"""
                            .format(int(user_answer_choice_id_substitute)))
        self.data_base.commit()

# instantiate the class Database
NEW_DATABASE = Database()
NEW_DATABASE.creation_database()
