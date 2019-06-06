#! /usr/bin/env python3
# coding: UTF-8

""" Docstrings """

"""imports"""
import mysql.connector
import json
import requests




"""')



add_database = ("CREATE DATABASE Purbeurre CHARACTER SET 'utf 8';")

add_table_food = (""CREATE TABLE Food (
                  id INT AUTO_INCREMENT
                  name_food VARCHAR(50) NOT NULL
                  category VARCHAR(50) NOT NULL
                  nutriscore VARCHAR(3) NOT NULL
                  description VARCHAR(500)
                  store VARCHAR(100)
                  link VARCHAR(300));
                  "")
add_table_favorite = (""CREATE TABLE Favorite (
                  id INT AUTO_INCREMENT
                  id_food + fk
                  name_food VARCHAR(50) NOT NULL
                  substitute_chooses VARCHAR(50) NOT NULL
                  );"")

add_index_nutriscore = ("ALTER TABLE Food ADD INDEX ind_nutriscore (nutriscore);")

add_index_category = ("ALTER TABLE Food ADD INDEX ind_category (category);")

add_primary_key_food_id = ("ALTER TABLE Food ADD PRIMARY KEY (id);")

add_primary_key_favorite_id = ("ALTER TABLE Favorite ADD PRIMARY KEY (id);")

cursor.execute(add_category)

data_base.commit()

cursor.close()"""

def answer():

    # First answer of the user :
    print("\nRenseignez votre choix avant de valider : \nchoix 1 > Quel aliment souhaitez-vous remplacer ?"
                            "\nchoix 2 > Retrouver mes aliments substitués.")
    user_answer = input("Tapez votre choix : ")

    # If the user chooses the option 1 :
    if str(user_answer) == "1":

        # If chooses the category : PREVOIR SI CHOIX INEXISTANT
        category = "fresh_frozen"
        number = 1
        print("\nRenseignez le numéro de la catégorie choisie :")
        print("choix", number, ">", category)
        user_answer_category = input("Votre choix : ")

        # If chooses the food : PREVOIR SI CHOIX INEXISTANT
        food = "butter"
        number = 1
        print("\nRenseignez le numéro de l'aliment choisi :")
        print("choix", number, ">", food)
        user_answer_food = input("Votre choix : ")

        # Detail of the proposed food substitute and choice to save it : PREVOIR SI CHOIX INEXISTANT
        substitute = "cream"
        description = "white"
        store = "auchan"
        link = "http..."
        print("\nSubstitut proposé :", substitute, "\nDescription :", description, "\nMagasin où le trouver :", store, "\nLien internet :", link)
        print("\nSouhaitez-vous enregistrer ce substitut ? \nchoix 1 > oui \nchoix 2 > non")
        user_answer_save_food = input("Votre choix : ")

        # Confirmation of registration
        if user_answer_save_food == "1":
            print("\nNous avons bien enregistré le substitut", substitute+".")
        elif user_answer_save_food == "2":
            print("\nEnregistrement non effectué pour le substitut", substitute+".")

    # If the user chooses the option 2 :
    elif str(user_answer) == "2":
        print("\nMes aliments substitués enregistrés :")
        print("\nSubstitute (substitut de food) \nDescription : descrition \nMagasin où le trouver : store \nLien internet : link")

    # If the user indicates a wrong answer :
    else:
        while str(user_answer) != "1":
            print("\nCe choix n'existe pas.")
            answer()

answer()