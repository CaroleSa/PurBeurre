#! /usr/bin/env.python3
# coding: utf-8

""" Docstrings """

import requests

r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=pizza&sort_by=unique_scans_n&page_size=1000&axis_x=energy&axis_y=products_n&action=display")
"""data = r.json()"""

print(r)
