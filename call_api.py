#! /usr/bin/env python3
# coding: UTF-8

""" Class Call_api """



# imports
import json
import requests



class Call_api:

    def __init__(self):
        # food categories (list) used in the program
        self.categories = ['pizza', 'pate a tartiner', 'gateau', 'yaourt', 'bonbon']

        # food data of categories chooses
        self.list_data = []

    def load_data(self):
        """ Loading data of the A.P.I. Open Food Facts and convert to json """
        # creating the list that contains food data of categories chooses
        for elt in self.categories:
            request = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process"
                                "&tagtype_0=categories&tag_contains_0=contains&tag_0={0}"
                                "&sort_by=unique_scans_n&page_size=1000"
                                "&axis_x=energy&axis_y=products_n&action=display&json=1"
                                .format("\'"+elt+"\'"))
            data = json.loads(request.text)
            self.list_data.append(data)

