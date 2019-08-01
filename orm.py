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


    def create_list(self, function_data):
        """ .... """
        data = self.new_database.function_data
        for elt in data:
            self.list.append(elt)
        return self.list


    def create_foods_list(self):
        """ .... """
        all_id_name_foods = self.new_database.select_foods_database()
        for elt in all_id_name_foods:
            self.list.append(elt)

        return self.list
