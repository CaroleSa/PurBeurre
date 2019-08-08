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
        object_list_11 = []
        for elt in sql_data:
            data1 = model.Foods(0, elt[0], 0, elt[1], 0, 0, 0)
            data = model.Foods(0, elt[2], 0, elt[3], elt[4], elt[5], elt[6])
            object_list.append(data)
            object_list_11.append(data1)

        return object_list, object_list_11

    def transform_favorite_food_to_object(self, sql_data1, sql_data2):
        object_list_1 = []
        object_list_11 = []
        for elt in sql_data1:
            data = model.Favorite(elt[0], 0, 0)
            data1 = model.Foods(0, elt[1], 0, 0, 0, 0, 0)
            object_list_1.append(data)
            object_list_11.append(data1)

        object_list_2 = []
        for elt in sql_data2:
            data = model.Foods(0, elt, 0, 0, 0, 0, 0)
            object_list_2.append(data)

        return object_list_1, object_list_2, object_list_11

    def transform_detail_substitute_to_object(self, sql_data):
        object_list = []
        for elt in sql_data:
            data = model.Foods(0, elt[0], 0, elt[1], elt[2], elt[3], elt[4])
            object_list.append(data)
        print(object_list)
        return object_list