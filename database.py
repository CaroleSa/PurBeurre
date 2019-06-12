#! /usr/bin/env python3
# coding: UTF-8

"""Creation database"""

import mysql.connector
import json
import requests


class Database:

    def __init__(self):
        # connection at MySQL and creation cursor
        with open('connection.yml', 'r') as f:
            info = f.read().split()
            self.data_base = mysql.connector.connect(user=info[0], password=info[1], host=info[2])
            self.cursor = self.data_base.cursor()

    def creation_database(self):
        # running file "base.sql" requests : for the creation of the database
        with open("base.sql", "r") as file:
            base = file.read()
            self.cursor.execute(base)
            print('Création de la database ok !!!!')

    def test(self):
        self.cursor.execute("use purbeurre;")
        self.cursor.execute("""INSERT INTO Food (name_food, nutriscore, description, store, link)
                          VALUES('fromage', 'd', 'à la vache', 'ferme', 'lien fromage');""")
        self.data_base.commit()
        self.cursor.close()
        self.data_base.close()
        print("MySQL est fermé")


    def load_insert_data(self):
        # loading data of API Openfoodfacts, convert to json and inserting data into the database
        self.cursor.execute("use purbeurre;")
        try:

            r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_"
                             "contains_0=contains&tag_0=pizza&sort_by=unique_scans_n&page_size=1000&axis_x=energy&"
                             "axis_y=products_n&action=display&json=1")
            data = json.loads(r.text)

            for value in data['products']:
                product_name = value['product_name_fr']
                categories = value['categories']
                nutrition_grade = value['nutrition_grade_fr']
                ingredients = value['ingredients_text']
                store_tags = value['stores_tags']
                url = value['url']
                print(categories)

                insert_data = ("""INSERT INTO Food (name_food, nutriscore, description, store, link)
                          VALUES(%s, %s, %s, %s, %s);""", (product_name, nutrition_grade, ingredients, store_tags, url))
                self.cursor.execute(insert_data)
                self.data_base.commit()
                self.cursor.close()
                self.data_base.close()
                print("MySQL est fermé")

        except (mysql.connector.errors.OperationalError, mysql.connector.errors.DatabaseError) as m:
            print("Insertion de données ne marche pas, voici le message d'erreur :", m)
            self.data_base.close()
            print("MySQL est fermé")



new_database = Database()
#new_database.creation_database()
new_database.load_insert_data()

