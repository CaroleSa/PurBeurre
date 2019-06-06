#! /usr/bin/env python3
# coding: UTF-8

"""Creation database"""

import mysql.connector
import json
import requests

class Database:

    def __init__(self):
        # connection at MySQL and creation cursor
        self.data_base = mysql.connector.connect(user='root', password='Root', host='localhost')
        self.cursor = self.data_base.cursor()

    def creation_database(self):
        # running file "base.sql" requests : for the creation of the database
        self.cursor.execute("SOURCE base.sql;")

    def load_insert_data(self):
        # loading data of API Openfoodfacts, convert to json and inserting data into the database
        r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_"
                         "0=contains&tag_0=pizza&sort_by=unique_scans_n&page_size=10&axis_x=energy&axis_"
                         "y=products_n&action=display&json=1")
        data = json.loads(r.text)

        for value in data['products']:
            product_name = value['product_name_fr']
            categories = value['categories']
            nutrition_grade = value['nutrition_grade_fr']
            ingredients = value['ingredients_text_with_allergens']
            store_tags = value['stores_tags']
            url = value['url']

            insert_data = ("""INSERT INTO Food (name_food, category, nutriscore, description, store, link)
            VALUES(product_name, categories, nutrition_grade, ingredients, store_tags, url);""")
            self.cursor.execute(insert_data)

            self.data_base.commit()

            self.cursor.close()

new_database = Database()
new_database.creation_database()
#new_database.load_insert_data()


