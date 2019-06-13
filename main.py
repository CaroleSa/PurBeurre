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

        self.user_answer_category = 0
        self.user_answer_food = 0

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
        self.user_answer_category = input("Votre choix : ")

        # if wrong answer
        try:
            if int(self.user_answer_category) <= len(result_categories) and int(self.user_answer_category) != 0:
                self.answer_choice_1_food()
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 1 et", len(result_categories), ".")
                self.answer_choice_1_category()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 1 et", len(result_categories), ".")
            self.answer_choice_1_category()

    def answer_choice_1_food(self):
        # he chooses the food of the category :
        print("\nRenseignez le numéro de l'aliment choisi :")

        # display of foods
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT id, name_food 
                            FROM Food 
                            WHERE id IN (SELECT id_food FROM Food_category WHERE id_category = {});"""
                            .format(self.user_answer_category))
        result_food = self.cursor.fetchall()
        for id, name_food in result_food:
            print("choix", id, ">", name_food)

        # the user chooses one food
        self.user_answer_food = input("Votre choix : ")

        # if wrong answer
        try:
            if int(self.user_answer_food) <= len(result_food) and int(self.user_answer_food) != 0:
                self.proposed_substitute_favorite()
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 1 et", len(result_food), ".")
                self.answer_choice_1_food()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 1 et", len(result_food), ".")
            self.answer_choice_1_food()

    def proposed_substitute_favorite(self):
        # Detail of the proposed food substitute and choice to save it

        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT (SELECT name_food FROM Food WHERE id = {2}) as name_food_chooses, 
                            (SELECT nutriscore FROM Food WHERE id = {2}) as nutriscore_of_food_chooses, 
                            name_food, nutriscore, description, store, link
                            FROM Food
                            WHERE id IN (SELECT id_food FROM Food_category WHERE id_category = {1}) 
                            as id_foods_of_category_chooses 
                            AND nutriscore < (SELECT nutriscore FROM Food WHERE id = {2}) as nutriscore_of_food_chooses
                            ORDER BY nutriscore ASC;""".format(self.user_answer_category, self.user_answer_food))
        result_substitute = self.cursor.fetchall()

        for name_food_chooses, name_food, nutriscore_of_food_chooses, nutriscore, description, store, link in result_substitute:
            print("L'aliment", name_food_chooses, "peut être remplacé par", name_food,
              "(", nutriscore_of_food_chooses, "):\nnutriscore :", nutriscore, "\nDescription :", description,
              "\nMagasin où le trouver :", store, "\nLien internet :", link)

        self.save_substitute(substitute)

        self.data_base.close()
        print("MySQL est fermé")

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

    def answer_choice_2(self):
        # If the user chooses the option 2 :

        print("\nMes aliments substitués enregistrés :")
        print("\nSubstitute (substitut de food) \nDescription : descrition \nMagasin où le trouver : store "
              "\nLien internet : link")

new_user = User()
new_user.first_question()
