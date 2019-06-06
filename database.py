#! /usr/bin/env python3
# coding: UTF-8

"""Database pur_beurre"""

import mysql.connector
import json
import requests

class Database:

    def __init__(self):
        # connection at MySQL and
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
            print(value['product_name_fr'])
            print(value['categories'])
            print(value['nutrition_grade_fr'])
            print(value['ingredients_text_with_allergens'])
            print(value['stores_tags'])
            print(value['url'])

new_database = Database()
#new_database.creation_database()
new_database.load_insert_data()


