#! /usr/bin/env python3
# coding: UTF-8


""" Class Categories, Foods and Favorite """


class Categories:

    def __init__(self, id, categories):
        self.id = id
        self.categories = categories

class Foods:

    def __init__(self, id, name_food, category_id, nutriscore, description, store, link):
        self.id = id
        self.name_food = name_food
        self.category_id = category_id
        self.nutriscore = nutriscore
        self.description = description
        self.store = store
        self.link = link

class Favorite:

    def __init__(self, id, id_food, id_substitute_chooses):
        self.id = id
        self.id_food = id_food
        self. id_substitute_chooses = id_substitute_chooses