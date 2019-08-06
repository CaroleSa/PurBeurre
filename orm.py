#! /usr/bin/env python3
# coding: UTF-8

""" Class Orm """



# imports
import database




class Orm:
    """ Transforming data into a python object """

    def __init__(self):
        """ Instantiate the class Database """
        self.new_database = database.Database()

        self.list = []


    def create_categories_list(self):
        """ .... """
        data = self.new_database.select_categories_database()
        for elt in data:
            self.list.append(elt)
        return self.list


    def create_foods_list(self, user_answer_id_category):
        """ .... """
        data = self.new_database.select_foods_database(user_answer_id_category)
        for elt in data:
            self.list.append(elt)

        return self.list
