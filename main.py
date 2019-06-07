#! /usr/bin/env python3
# coding: UTF-8

""" Docstrings """

"""imports"""
import mysql.connector
import json
import requests


class User:

    def answer_choice_1_category(self):
        # If the user chooses the option 1,
        # then he chooses the category : PREVOIR SI CHOIX INEXISTANT
        category = "fresh_frozen"
        number = 1
        print("\nRenseignez le numéro de la catégorie choisie :")
        print("choix", number, ">", category)
        user_answer_category = input("Votre choix : ")

        if str(user_answer_category) == "1":
            self.answer_choice_1_food()
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre.")
            self.answer_choice_1_category()

    def answer_choice_1_food(self):
        # If the user chooses the option 1,
        # then he chooses the food : PREVOIR SI CHOIX INEXISTANT
        food = "butter"
        number = 1
        print("\nRenseignez le numéro de l'aliment choisi :")
        print("choix", number, ">", food)
        user_answer_food = input("Votre choix : ")

        if str(user_answer_food) == "1":
            self.proposed_substitute_favorite()
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre.")
            self.answer_choice_1_food()

    def save_substitute(self, substitute):
        # Confirmation of registration
        print("\nSouhaitez-vous enregistrer ce substitut ? \nchoix 1 > oui \nchoix 2 > non")
        user_answer_save_food = input("Votre choix : ")

        if user_answer_save_food == "1":
            print("\nNous avons bien enregistré le substitut", substitute+".")
        elif user_answer_save_food == "2":
            print("\nEnregistrement non effectué pour le substitut", substitute+".")
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2.")
            self.save_substitute(substitute)

    def proposed_substitute_favorite(self):
        # Detail of the proposed food substitute and choice to save it : PREVOIR SI CHOIX INEXISTANT
        substitute = "cream"
        description = "white"
        store = "auchan"
        link = "http..."
        print("\nSubstitut proposé :", substitute, "\nDescription :", description, "\nMagasin où le trouver :",
              store, "\nLien internet :", link)
        self.save_substitute(substitute)

    def answer_choice_2(self):
        # If the user chooses the option 2 :
        print("\nMes aliments substitués enregistrés :")
        print("\nSubstitute (substitut de food) \nDescription : descrition \nMagasin où le trouver : store "
              "\nLien internet : link")

    def first_question(self):
        # First question at the user :
        print("\nRenseignez votre choix avant de valider : \nchoix 1 > Quel aliment souhaitez-vous remplacer ?"
                                "\nchoix 2 > Retrouver mes aliments substitués.")
        user_answer = input("Tapez votre choix : ")

        if str(user_answer) == "1":
            self.answer_choice_1_category()
        elif str(user_answer) == "2":
            self.answer_choice_2()
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2.")
            self.first_question()

new_user = User()
new_user.first_question()
