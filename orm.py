#! /usr/bin/env python3
# coding: UTF-8


""" Class Orm """


# import
import model



class Orm:
    """ Transforming data to python object """


    @classmethod
    def transform_categories_to_object(cls, sql_data):
        """ transform sql data (id and name of categories) to python object """
        object_list = []

        for elt in sql_data:
            data = model.Categories(categories_id=elt[0], name_categories=elt[1])
            object_list.append(data)

        return object_list


    @classmethod
    def transform_foods_to_object(cls, sql_data):
        """ transform sql data (id and name of foods) to python object """
        object_list = []

        for elt in sql_data:
            data = model.Foods(foods_id=elt[0], name_food=elt[1])
            object_list.append(data)

        return object_list


    @classmethod
    def transform_substitute_to_object(cls, sql_data):
        """ transform sql data (name and nustriscore of food chooses
        and the substitute information) to python object """
        object_list_1 = []
        object_list_2 = []

        for elt in sql_data:
            data1 = model.Foods(name_food=elt[0], nutriscore=elt[1])
            data2 = model.Foods(name_food=elt[2], nutriscore=elt[3],
                                description=elt[4], store=elt[5], link=elt[6])
            object_list_1.append(data1)
            object_list_2.append(data2)

        return object_list_1, object_list_2


    @classmethod
    def transform_favorite_foods_to_object(cls, sql_data1, sql_data2):
        """ transform sql data (favorite food name
        and id, name of its substitute) to python object """
        object_list_1 = []
        object_list_2 = []
        object_list_3 = []

        for elt in sql_data1:
            data1 = model.Favorite(favorite_id=elt[0])
            data2 = model.Foods(name_food=elt[1])
            object_list_1.append(data1)
            object_list_2.append(data2)

        for elt in sql_data2:
            data3 = model.Foods(name_food=elt)
            object_list_3.append(data3)

        return object_list_1, object_list_2, object_list_3


    @classmethod
    def transform_detail_substitute_to_object(cls, sql_data):
        """ transform sql data (substitute information) to python object """
        object_list = []

        for elt in sql_data:
            data = model.Foods(name_food=elt[0], nutriscore=elt[1],
                               description=elt[2], store=elt[3], link=elt[4])
            object_list.append(data)

        return object_list
