#! /usr/bin/env python3
# coding: UTF-8

""" Class User """



# imports
from mysql.connector.errors import IntegrityError

import database as db
# pylint: disable=too-many-function-args



class User:
    """ Command line interface"""


    def __init__(self):
        # instantiate the class Database
        self.new_database = db.Database()

        # attributes
        self.user_answer_id_category = 0
        self.user_answer_i_food = 0
        self.dict_equivalence_i_id_food = {}
        self.dict_equivalence_i_id_food_substitute = {}


    def menu(self):
        """ menu """
        # first question to the user : menu
        print("\nRenseignez votre choix avant de valider : "
              "\nchoix 1 > Quel aliment souhaitez-vous remplacer ?"
              "\nchoix 2 > Retrouver mes aliments substitués "
              "\nchoix 3 > Quitter")

        # user's answer
        user_answer_choice_menu = input("Tapez votre choix : ")
        if str(user_answer_choice_menu) == "1":
            self.propose_categories()
        elif str(user_answer_choice_menu) == "2":
            self.show_food_and_substitute()
        elif str(user_answer_choice_menu) == "3":
            print("\nMerci pour votre visite et à bientôt !")

        # if the answer does not exist
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3.")
            self.menu()


    def propose_categories(self):
        """ choice of category """
        # call Database method : use database for selected categories
        all_id_name_categories = self.new_database.select_categories_database()

        # display the categories
        print("\nRenseignez le numéro de la catégorie choisie :")
        print("choix 0 > Retourner au menu")
        for id_categories, name_categories in all_id_name_categories:
            print("choix", id_categories, ">", name_categories)

        # user's answer
        self.user_answer_id_category = input("Votre choix : ")
        try:
            if int(self.user_answer_id_category) <= len(all_id_name_categories) \
                    and int(self.user_answer_id_category) != 0:
                self.propose_foods()
            elif int(self.user_answer_id_category) == 0:
                self.menu()

            # if the answer does not exist
            else:
                print("\nCE CHOIX N'EXISTE PAS. "
                      "\nVeuillez taper un chiffre entre 0 et", len(all_id_name_categories), ".")
                self.propose_categories()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. "
                  "\nVeuillez taper un chiffre entre 0 et", len(all_id_name_categories), ".")
            self.propose_categories()


    def propose_foods(self):
        """ choice of food """
        # call Database method : use database for selected foods
        all_id_name_food = self.new_database.select_foods_database(self.user_answer_id_category)

        # display the foods
        print("\nRenseignez le numéro de l'aliment choisi :")
        print("choix 0 > Retourner aux catégories")
        i = 0
        for id_food, name_food in all_id_name_food:
            i += 1
            print("choix", i, ">", name_food)
            self.dict_equivalence_i_id_food[i] = id_food

        # user's answer
        self.user_answer_i_food = input("Votre choix : ")
        try:
            if int(self.user_answer_i_food) <= len(all_id_name_food) \
                    and int(self.user_answer_i_food) != 0:
                self.propose_substitute(0)
            elif int(self.user_answer_i_food) == 0:
                self.propose_categories()

            # if the answer does not exist
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et",
                      len(all_id_name_food), ".")
                self.propose_foods()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et",
                  len(all_id_name_food), ".")
            self.propose_foods()


    def propose_substitute(self, read_line_substitute):
        """ detail of the substitute and choice to save it """
        # id recovery from i (choice number)
        user_answer_id_food = self.dict_equivalence_i_id_food.get(int(self.user_answer_i_food))

        # call Database method : select the substitute and the substituted food
        result_food_chooses_and_substitute = self.new_database.select_substitute\
            (self.user_answer_id_category, user_answer_id_food, read_line_substitute)

        # 'for loop' for use data of the database
        for name_food_chooses, nutriscore_of_food_chooses, name_substitute, \
                nutriscore_substitute, description_substitute, store_substitute, \
                link_substitute in result_food_chooses_and_substitute:

            def order_letters(letter):
                """ indicates the location number of letters of the alphabet """
                return int(ord(letter) - ord('a') + 1)

            # if the food chosen does not have a substitute
            if order_letters(nutriscore_of_food_chooses) \
                    <= order_letters(nutriscore_substitute):
                self.no_substitute(name_food_chooses)

            # if the food chosen have a substitute > display the detail of the substitute
            else:
                print("\nL'aliment", name_food_chooses,
                      "(Nutriscore :", nutriscore_of_food_chooses,
                      ") peut être remplacé par", name_substitute,
                      ":\nnutriscore :", nutriscore_substitute,
                      "\nDescription :", description_substitute,
                      "\nMagasin(s) où le trouver :", store_substitute,
                      "\nLien internet :", link_substitute)
                self.save_substituted_food(name_substitute,
                                           read_line_substitute,
                                           user_answer_id_food)


    def no_substitute(self, name_food_chooses):
        """ the food chosen does not have a substitute,
        propose a new search or return to the menu """
        # new choices
        print("\nL'aliment", name_food_chooses,
              "n'a pas d'autres substituts possibles."
              "\n\nSouhaitez-vous faire une nouvelle recherche ? "
              "\nchoix 1 > oui "
              "\nchoix 2 > non")

        # user's answer
        user_answer_new_search = input("Votre choix : ")
        if user_answer_new_search == "1":
            self.propose_categories()
        elif user_answer_new_search == "2":
            self.menu()

        # if the answer does not exist
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2.")
            self.no_substitute(name_food_chooses)


    def save_substituted_food(self, name_substitute, read_line_substitute, user_answer_id_food):
        """ propose save or another substitute """
        # question to the user
        print("\nSouhaitez-vous enregistrer l'aliment et son substitut ? "
              "\nchoix 1 > oui "
              "\nchoix 2 > non "
              "\nchoix 3 > Je souhaite un autre substitut possible")

        # user's answer
        user_answer_save_food = input("Votre choix : ")
        try:
            # use Database method for save substituted food and his substitute into database
            if user_answer_save_food == "1":
                self.new_database.insert_favorite_food(user_answer_id_food, name_substitute)
                print("\nNous avons bien enregistré l'aliment "
                      "et son substitut", name_substitute+".")
                self.menu()

            # no save substituted food and his substitute
            elif user_answer_save_food == "2":
                print("\nEnregistrement non effectué.")
                self.menu()

            # propose a new substitute
            elif user_answer_save_food == "3":
                read_line_substitute += 1
                self.propose_substitute(0 + read_line_substitute)

            # if the answer does not exist or if the food is already registered
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3.")
                self.save_substituted_food(name_substitute, read_line_substitute,
                                           user_answer_id_food)
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3.")
            self.save_substituted_food(name_substitute, read_line_substitute,
                                       user_answer_id_food)
        except IntegrityError:
            print("\nCet aliment et son substitut sont déjà enregistrés.")
            self.show_food_and_substitute()


    def show_food_and_substitute(self):
        """ show the favorite foods """
        # call Database method : select the favorite foods and their substitutes
        all_id_name_substitute = self.new_database.select_favorite_foods()[0]
        all_substituted_food = self.new_database.select_favorite_foods()[1]

        # if not exist favorite foods
        if not all_id_name_substitute:
            print("\nVous n'avez pas d'aliments substitués enregistrés.")
            self.menu()

        # display favorite foods
        else:
            print("\nVoici vos aliments et substituts enregistrés :"
                  "\nchoix 0 > quitter mes aliments et substituts enregistrés")
            i = 0
            for id_name_substitute, name_substituted_food \
                    in zip(all_id_name_substitute, all_substituted_food):
                i += 1
                print("choix", i, ">", name_substituted_food[0],
                      "(substitué par", id_name_substitute[1]+")")
                self.dict_equivalence_i_id_food_substitute[i] = id_name_substitute[0]
            print("Tapez un choix pour avoir plus de détail sur le substitut ou le supprimer.")

            # user's answer
            try:
                user_answer_choice_i_substitute = input("Votre choix : ")
                user_answer_choice_id_substitute = self.dict_equivalence_i_id_food_substitute.get\
                    (int(user_answer_choice_i_substitute))
                if int(user_answer_choice_i_substitute) <= len(all_substituted_food) \
                        and int(user_answer_choice_i_substitute) != 0:
                    self.detail_substitute(all_substituted_food, user_answer_choice_id_substitute)
                elif int(user_answer_choice_i_substitute) == 0:
                    self.menu()

                # if the answer does not exist
                else:
                    print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et",
                          len(all_substituted_food), ".")
                    self.show_food_and_substitute()
            except ValueError:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et",
                      len(all_substituted_food), ".")
                self.show_food_and_substitute()


    def detail_substitute(self, all_substituted_food, user_answer_choice_id_substitute):
        """ display the detail of the substitute """
        # call Database method : select the detail of the substitute
        show_substitute = self.new_database.select_detail_substitute\
            (user_answer_choice_id_substitute)

        # display the detail of the substitute
        for name_substitute, nutriscore_substitute, description_substitute, store_substitute, \
                link_substitute in show_substitute:
            print("\nAliment : ", name_substitute,
                  "\nNutriscore : ", nutriscore_substitute,
                  "\nDescription : ", description_substitute,
                  "\nMagasin(s) où le trouver : ", store_substitute,
                  "\nLien d'information : ", link_substitute,
                  "\n\nVous souhaitez : "
                  "\nchoix 1 : supprimer cet aliment"
                  "\nchoix 2 : chercher un autre aliment substitué enregistré"
                  "\nchoix 3 : retourner au menu")

            # user's answer
            user_answer_return_delete_substitute_menu = input("Votre choix : ")
            if int(user_answer_return_delete_substitute_menu) == 1:
                self.delete_food_substitute(user_answer_choice_id_substitute)
            elif int(user_answer_return_delete_substitute_menu) == 2:
                self.show_food_and_substitute()
            elif int(user_answer_return_delete_substitute_menu) == 3:
                self.menu()

            # if the answer does not exist
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2")
                self.detail_substitute(all_substituted_food, user_answer_choice_id_substitute)


    def delete_food_substitute(self, user_answer_choice_id_substitute):
        """ deleted the favorite food and his substitute """
        # call Database method : delete favorite food
        self.new_database.delete_favorite_food(user_answer_choice_id_substitute)

        # confirmation of deletion and return to favorite foods
        print("\nL'aliment a bien été supprimé.")
        self.show_food_and_substitute()



# instantiate the class User and call menu() method
NEW_USER = User()
NEW_USER.menu()

def main():
    """ use of class Database """
    db.Database()

if __name__ == "main":
    # execute only if run as a script
    main()
