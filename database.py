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

    def creation_database(self):
        # running file "base.sql" requests : for the creation of the database
        with open("base.sql", "r") as file:
            base = file.read()
            self.cursor.execute(base)
        print('Création de la database ok !!!!')


    def load_insert_data(self):
        # loading data of API Openfoodfacts, convert to json and inserting data into the database
        self.cursor.execute("use purbeurre;")
        try:

            r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_"
                             "contains_0=contains&tag_0=pizza&sort_by=unique_scans_n&page_size=1000&axis_x=energy&"
                             "axis_y=products_n&action=display&json=1")
            data = json.loads(r.text)

            for value in data['products']:
                product_name = "\'"+value['product_name_fr'].replace("'", "")+"\'"
                categories = "\'"+value['categories'].replace("'", "")+"\'"
                nutrition_grade = "\'"+value['nutrition_grade_fr'].replace("'", "")+"\'"
                ingredients = "\'"+value['ingredients_text'].replace("'", "")+"\'"
                store_tags = "\'"+value['stores_tags'][0].replace("'", "")+"\'"
                url = "\'"+value['url'].replace("'", "")+"\'"


                insert_data = ("""INSERT INTO Food (name_food, nutriscore, description, store, link)
                                VALUES({}, {}, {}, {}, {});"""
                               .format(product_name, nutrition_grade, ingredients, store_tags, url))

                print(insert_data)

                self.cursor.execute(insert_data)
                self.data_base.commit()

        except (mysql.connector.errors.OperationalError, mysql.connector.errors.DatabaseError) as m:
            print("Insertion de données ne marche pas, voici le message d'erreur :", m)

new_database = Database()
#new_database.creation_database()
new_database.load_insert_data()
