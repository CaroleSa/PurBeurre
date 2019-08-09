#! /usr/bin/env python3
# coding: UTF-8


""" Class Orm """

import model

class Orm:
    """ Transforming data into a python object """

    def transform_categories_to_object(self, sql_data):
        object_list = []
        for elt in sql_data:
            data = model.Categories(id = elt[0], categories = elt[1])
            object_list.append(data)
        return object_list

    def transform_foods_to_object(self, sql_data):
        object_list = []
        for elt in sql_data:
            data = model.Foods(id = elt[0], name_food = elt[1])
            object_list.append(data)
        print(object_list)
        return object_list

    def transform_substitute_to_object(self, sql_data):
        object_list = []
        object_list_11 = []
        for elt in sql_data:
            data1 = model.Foods(name_food = elt[0], nutriscore = elt[1])
            data = model.Foods(name_food = elt[2], nutriscore = elt[3],
                               description = elt[4], store = elt[5], link = elt[6])
            object_list.append(data)
            object_list_11.append(data1)

        return object_list, object_list_11

    def transform_favorite_food_to_object(self, sql_data1, sql_data2):
        object_list_1 = []
        object_list_11 = []
        for elt in sql_data1:
            data = model.Favorite(id = elt[0])
            data1 = model.Foods(name_food = elt[1])
            object_list_1.append(data)
            object_list_11.append(data1)

        object_list_2 = []
        for elt in sql_data2:
            data = model.Foods(name_food = elt)
            object_list_2.append(data)

        return object_list_1, object_list_2, object_list_11

    def transform_detail_substitute_to_object(self, sql_data):
        object_list = []
        for elt in sql_data:
            data = model.Foods(name_food = elt[0], nutriscore = elt[1],
                               description = elt[2], store = elt[3], link = elt[4])
            object_list.append(data)
        print(object_list)
        return object_list