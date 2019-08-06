#! /usr/bin/env python3
# coding: UTF-8

""" Class Categories, Foods and Favorite """



# imports
import orm
import controller


class Categories:

    def __init__(self):

        self.new_orm = orm.Orm()
        self.all_id_name_categories = self.new_orm.create_categories_list()

class Foods:

    def __init__(self):
        self.new_controller = controller.Controller()
        print("j'affiche", self.new_controller.user_answer_id_category)
        self.new_orm = orm.Orm()
        self.all_id_name_foods = self.new_orm.create_foods_list(self.new_controller.user_answer_id_category)