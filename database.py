#! /usr/bin/env python3
# coding: UTF-8

""" Class Database """



# imports
import mysql.connector
import call_api



class Database:
    """ Creation database and insert data """

    def __init__(self):
        """ Connection at MySQL, creation cursor and list of categories """
        # read the file connection.yml
        with open('connection.yml', 'r') as file:
            self.info = file.read().split()

        # connection at MySQL with data of connection.yml file and creation cursor
        self.data_base = mysql.connector.connect(user=self.info[0], password=self.info[1],
                                                 host=self.info[2])
        self.cursor = self.data_base.cursor()

        # instantiate the class Api
        new_api = call_api.Call_api()
        self.categories = new_api.categories
        self.list_data = new_api.list_data

    def creation_database(self):
        """ Running file "base.sql" requests : for the creation of the database """
        with open("base.sql", "r") as file:
            base = file.read()
            self.cursor.execute(base)

    def select_categories_database(self):
        """ use database to selected categories """
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("EXECUTE select_categories;")
        all_id_name_categories = self.cursor.fetchall()
        return all_id_name_categories

    def select_foods_database(self, user_answer_id_category):
        """ use database to selected foods """
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT id, name_food
                            FROM Food
                            WHERE category_id = {};""".format(user_answer_id_category))
        all_id_name_food = self.cursor.fetchall()
        return all_id_name_food

    def select_substitute(self, user_answer_id_category, user_answer_id_food, read_line_substitute):
        """ use database to selected food chooses and his substitute """
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT (SELECT name_food FROM Food WHERE id = {1}),
                            (SELECT nutriscore FROM Food WHERE id = {1}), 
                            name_food, nutriscore, description, store, link
                            FROM Food
                            WHERE category_id = {0}
                            ORDER BY nutriscore LIMIT {2},1;""" \
                            .format(user_answer_id_category,
                                    user_answer_id_food,
                                    read_line_substitute))
        result_food_chooses_and_substitute = self.cursor.fetchall()
        return result_food_chooses_and_substitute

    def insert_favorite_food(self, user_answer_id_food, name_substitute):
        """ use database to save substituted food and his substitute """
        save_favorite_substituted_food = """INSERT INTO Favorite
                                        (id_food, id_substitute_chooses)
                                        VALUES({0}, 
                                        (SELECT id FROM Food WHERE name_food = {1}));""" \
            .format(int(user_answer_id_food),
                    "\'" + name_substitute + "\'")
        self.cursor.execute(save_favorite_substituted_food)
        self.data_base.commit()

    def select_favorite_foods(self):
        """ use database to select the favorite foods and their substitutes """
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT Favorite.id, Food.name_food
                            FROM Food 
                            JOIN Favorite ON Food.id = Favorite.id_substitute_chooses 
                            WHERE Food.id = Favorite.id_substitute_chooses
                            ORDER BY Favorite.id;""")
        all_id_name_substitute = self.cursor.fetchall()
        self.cursor.execute("""SELECT Food.name_food
                            FROM Food
                            JOIN Favorite ON Food.id = Favorite.id_food
                            WHERE Food.id = Favorite.id_food
                            ORDER BY Favorite.id;""")
        all_substituted_food = self.cursor.fetchall()
        return all_id_name_substitute, all_substituted_food

    def select_detail_substitute(self, user_answer_choice_id_substitute):
        """ use database to select the detail of the substitute """
        self.cursor.execute("""SELECT name_food, nutriscore, description, store, link
                            FROM Food 
                            WHERE id = 
                            (SELECT id_substitute_chooses FROM Favorite WHERE id = {});"""
                            .format(int(user_answer_choice_id_substitute)))
        show_substitute = self.cursor.fetchall()
        return show_substitute

    def delete_favorite_food(self, user_answer_choice_id_substitute):
        """ use database to delete favorite food """
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""DELETE FROM Favorite where id = {};"""
                            .format(int(user_answer_choice_id_substitute)))
        self.data_base.commit()


# instantiate the class Database and call creation_database() method
NEW_DATABASE = Database()
NEW_DATABASE.creation_database()
