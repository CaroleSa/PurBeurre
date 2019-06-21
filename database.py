#! /usr/bin/env python3
# coding: UTF-8

""" Class Database """



# import library
import json
import requests
import mysql.connector



class Database:
    """ Creation database and insert data """

    def __init__(self):
        """ Connection at MySQL, creation cursor and list of chosen categories """
        # read the file connection.yml
        file = open('connection.yml', 'r')
        info = file.read().split()

        # connection at MySQL with data of connection.yml file and creation cursor
        self.data_base = mysql.connector.connect(user=info[0], password=info[1], host=info[2])
        self.cursor = self.data_base.cursor()

        # food categories (list) used in the program
        self.categories = ['pizza', 'pate a tartiner', 'gateau', 'yaourt', 'bonbon']

        # food data of categories chooses
        self.list_data = []

    def creation_database(self):
        """ Running file "base.sql" requests : for the creation of the database """
        with open("base.sql", "r") as file:
            base = file.read()
            self.cursor.execute(base, multi=True)

    def load_insert_data(self):
        """ Loading data of API Openfoodfacts, convert to json
        and inserting data into the database """

        # executed "use Purbeurre" request
        self.cursor.execute("USE Purbeurre;")

        # creating the list that contains food data of categories chooses
        for elt in self.categories:
            request = requests.get("https://fr.openfoodfacts.org/cgi/search.pl"
                                   "?action=process"
                                   "&tagtype_0=categories"
                                   "&tag_contains_0=contains"
                                   "&tag_0={0}"
                                   "&sort_by=unique_scans_n"
                                   "&page_size=1000"
                                   "&axis_x=energy"
                                   "&axis_y=products_n"
                                   "&action=display"
                                   "&json=1".format("\'"+elt+"\'"))
            data = json.loads(request.text)
            self.list_data.append(data)

        for elt, element in zip(self.categories, self.list_data):

            # inserting data into Category table
            insert_data_categories = ("""INSERT IGNORE INTO Category (categories) VALUES({0});"""
                                      .format("\'"+elt+"\'"))
            self.cursor.execute(insert_data_categories)
            self.data_base.commit()

            # inserting data into Food table
            for value in element['products']:
                if element['products'].index(value) < 20:
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
                                            {2}, {3}, {4}, {5});"""
                                            .format(product_name, "\'"+elt+"\'", nutrition_grade,
                                                    ingredients, store_tags, url))
                        self.cursor.execute(insert_data_food)
                        self.data_base.commit()

                    # if errors
                    except KeyError:
                        continue


# instantiate the class Database and call creation_database() method
NEW_DATABASE = Database()
#NEW_DATABASE.creation_database()
NEW_DATABASE.load_insert_data()
