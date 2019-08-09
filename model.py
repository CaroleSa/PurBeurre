#! /usr/bin/env python3
# coding: UTF-8


""" Class Categories, Foods and Favorite """


class Categories:
    """ class Categories """

    def __init__(self, categories_id=None, name_categories=None):
        self.id = categories_id
        self.categories = name_categories

class Foods:
    """ class Foods """

    def __init__(self, foods_id=None, name_food=None, category_id=None,
                 nutriscore=None, description=None, store=None, link=None):
        self.id = foods_id
        self.name_food = name_food
        self.category_id = category_id
        self.nutriscore = nutriscore
        self.description = description
        self.store = store
        self.link = link

class Favorite:
    """ class Favorite """

    def __init__(self, favorite_id=None, id_food=None, id_substitute_chooses=None):
        self.id = favorite_id
        self.id_food = id_food
        self.id_substitute_chooses = id_substitute_chooses
