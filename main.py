#! /usr/bin/env python3
# coding: UTF-8

""" Docstrings """

"""imports"""
import mysql.connector


class User:

    def __init__(self):
        """new_database = db.Database()
        self.cursor = new_database.cursor"""
        with open('connection.yml', 'r') as f:
            info = f.read().split()
            self.data_base = mysql.connector.connect(user=info[0], password=info[1], host=info[2])
            self.cursor = self.data_base.cursor()

    def answer_choice_1_category(self):
        # if the user chooses the option 1,
        # he chooses the category :
        print("\nRenseignez le numéro de la catégorie choisie :")

        # display of categories
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("SELECT id, categories FROM Category;")
        result_categories = self.cursor.fetchall()
        for id, categories in result_categories:
            print("choix", id, ">", categories)

        # the user chooses one category
        user_answer_category = input("Votre choix : ")

        # if wrong answer
        try:
            if int(user_answer_category) <= len(result_categories) and int(user_answer_category) != 0:
                self.answer_choice_1_food()
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre.")
                self.answer_choice_1_category()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre.")
            self.answer_choice_1_category()
        return user_answer_category

    def answer_choice_1_food(self):
        # he chooses the food of the category :
        print("\nRenseignez le numéro de l'aliment choisi :")

        # display of foods
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT id, name_food FROM Food WHERE id = 
                            (SELECT id_food FROM Food_category WHERE id_category = %s) 
                            as id_food_category;""", (int(self.answer_choice_1_category())))
        result_food = self.cursor.fetchall()
        for id, name_food in result_food:
            print("choix", id, ">", name_food)

        # the user chooses one food
        user_answer_food = input("Votre choix : ")

        # if wrong answer
        try:
            if int(user_answer_food) <= len(result_food) and int(user_answer_food) != 0:
                self.data_base.close()
                print("MySQL est fermé")
                self.proposed_substitute_favorite()
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre.")
                self.answer_choice_1_food()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre.")
            self.answer_choice_1_food()
        return user_answer_food

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
