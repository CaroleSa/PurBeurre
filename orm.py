#! /usr/bin/env python3
# coding: UTF-8


""" Class Orm """

import model

class Orm:
    """ Transforming data into a python object """

    def transform_categories_to_object(self, sql_data):
        object_list = []
        for elt in sql_data:
            data = model.Categories(elt[0], elt[1])
            object_list.append(data)
        return object_list

    def transform_foods_to_object(self, sql_data):
        object_list = []
        for elt in sql_data:
            data = model.Foods(elt[0], elt[1], 0, 0, 0, 0, 0)
            object_list.append(data)
        print(object_list)
        return object_list

    def transform_substitute_to_object(self, sql_data):
        object_list = []
        for elt in sql_data:
            data = model.Foods(elt[0], elt[1], 0, 0, 0, 0, 0)
            object_list.append(data)
        print(object_list)
        return object_list

    def transform_detail_substitute_to_object(self, sql_data):
        object_list = []
        for elt in sql_data:
            data = model.Foods(0, elt[0], 0, elt[1], elt[2], elt[3], elt[4])
            object_list.append(data)
        print(object_list)
        return object_list