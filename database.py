#! /usr/bin/env python3
# coding: UTF-8

"""Creation database"""

import mysql.connector
import json
import requests


class Database:

    def __init__(self):
        # connection at MySQL and creation cursor
        f = open('connection.yml', 'r')
        info = f.read().split()
        self.data_base = mysql.connector.connect(user=info[0], password=info[1], host=info[2])
        self.cursor = self.data_base.cursor()
        self.categories = ['pizza', 'pate a tartiner', 'gateau', 'yaourt', 'bonbon']
        self.i = 1

    def creation_database(self):
        # running file "base.sql" requests : for the creation of the database
        with open("base.sql", "r") as file:
            base = file.read()
            self.cursor.execute(base)
        print('Création de la database ok !!!!')

    def load_insert_data(self):
        # loading data of API Openfoodfacts, convert to json and inserting data into the database
        try:
            self.cursor.execute("use purbeurre;")

            for self.i, elt in enumerate(self.categories) :

                # inserting data into Category table
                insert_data_category = ("""INSERT IGNORE INTO Category (categories) VALUES({});""".format("\'"+elt+"\'"))
                self.cursor.execute(insert_data_category)
                self.data_base.commit()

                # inserting data into Food table
                r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_"
                                 "contains_0=contains&tag_0={0}&sort_by=unique_scans_n&page_size=1000&axis_x=energy&"
                                 "axis_y=products_n&action=display&json=1".format("\'"+elt+"\'"))
                data = json.loads(r.text)
                self.i += 1

                for elt, value in zip(self.categories, data['products']):

                    product_name = "\'"+value['product_name_fr'].replace("'", "")+"\'"
                    nutrition_grade = "\'"+value['nutrition_grade_fr'].replace("'", "")+"\'"
                    ingredients = "\'"+value['ingredients_text'].replace("'", "")+"\'"
                    store_tags = "\'"+", ".join(value['stores_tags']).replace("'", "")+"\'"
                    url = "\'"+value['url'].replace("'", "")+"\'"

                    insert_data_food = ("""INSERT IGNORE INTO Food (name_food, category_id, nutriscore, description, 
                                        store, link) VALUES({0}, {1}, {2}, {3}, {4}, {5});"""
                                        .format(product_name, self.i, nutrition_grade, ingredients, store_tags, url))

                    print(insert_data_food)
                    self.cursor.execute(insert_data_food)
                    self.data_base.commit()

        except KeyError:
            pass

        except (mysql.connector.errors.OperationalError, mysql.connector.errors.DatabaseError) as m:
            print("Insertion de données ne marche pas, voici le message d'erreur :", m)

new_database = Database()
#new_database.creation_database()
new_database.load_insert_data()
