#! /usr/bin/env python3
# coding: UTF-8

""" Class Controller """


import database as db


class Controller:


    def __init__(self):
        # instantiate the class Database
        self.new_database = db.Database()


    def get_id_name_categories(self):
        # call Database method : use database for selected categories
        all_id_name_categories = self.new_database.select_categories_database()
        return all_id_name_categories