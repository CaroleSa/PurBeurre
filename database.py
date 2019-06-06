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

    def load_data(self):
        # loading data of API Openfoodfacts and convert to json
        r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_"
                         "0=contains&tag_0=pizza&sort_by=unique_scans_n&page_size=10&axis_x=energy&axis_y=products_n&action=display&json=1")
        result = json.loads(r.text)

    def insert_data(self):
        # inserting data into the database
        for value in result['products']:
            print(value['product_name_fr'])

test = Database()
test.creation_database()