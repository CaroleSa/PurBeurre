#! /usr/bin/env python3
# coding: UTF-8

""" Class Controller """



# imports
from mysql.connector.errors import IntegrityError
import database as db
import main



class Controller:


    def __init__(self):
        # instantiate the class Database and CommandLineInterface
        self.new_database = db.Database()
        self.cli = main.CommandLineInterface()

        # attributes
        self.user_answer_id_category = 0
        self.user_answer_id_food = 0

    def get_id_name_categories(self):
        # call Database method : use database for selected categories
        all_id_name_categories = self.new_database.select_categories_database()
        return all_id_name_categories

    def get_id_name_foods(self):
        # call Database method : use database for selected foods
        all_id_name_foods = self.new_database.select_foods_database(self.user_answer_id_category)
        return all_id_name_foods

    def get_food_chooses_substitute(self, read_line_substitute):
        # call Database method : select the substitute and the substituted food
        result_food_chooses_and_substitute = self.new_database.select_substitute\
            (self.user_answer_id_category, self.user_answer_id_food, read_line_substitute)
        return result_food_chooses_and_substitute

    def save_favorite_food(self, name_substitute):
        self.new_database.insert_favorite_food(self.user_answer_id_food, name_substitute)

    def get_favorite_food_and_substitute(self):
        # call Database method : select the favorite foods and their substitutes
        all_id_name_substitute_and_substituted_food = self.new_database.select_favorite_foods()
        return all_id_name_substitute_and_substituted_food





    def menu(self):
        """ menu """
        # first question to the user : menu
        text = "\nRenseignez votre choix avant de valider : " \
                "\nchoix 1 > Quel aliment souhaitez-vous remplacer ?" \
                "\nchoix 2 > Retrouver mes aliments substitués" \
                "\nchoix 3 > Quitter"

        user_answer = str(self.cli.question_answer(text))

        if user_answer == "1":
            self.propose_categories()
        elif user_answer == "2":
            self.show_food_and_substitute()
        elif user_answer == "3":
            message = "\nMerci pour votre visite et à bientôt !"
            self.cli.display_message(message)

        # if the answer does not exist
        else:
            message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3."
            self.cli.display_message(message)
            self.menu()


    def propose_categories(self):
        """ choice of category """
        # display the categories
        text = "\nRenseignez le numéro de la catégorie choisie :\nchoix 0 > Retourner au menu"
        for id_categories, name_categories in self.get_id_name_categories():
            text_choices = "\nchoix {} > {}".format(id_categories, name_categories)
            text = text + text_choices

        # user's answer
        self.user_answer_id_category = int(self.cli.question_answer(text))
        try:
            if self.user_answer_id_category <= len(self.get_id_name_categories()) \
                    and self.user_answer_id_category != 0:
                self.propose_foods()
            elif self.user_answer_id_category == 0:
                self.menu()

            # if the answer does not exist
            else:
                message = "\nCE CHOIX N'EXISTE PAS.\nVeuillez taper un chiffre entre 0 et {}."\
                    .format(len(self.get_id_name_categories()))
                self.cli.display_message(message)
                self.propose_categories()

        except ValueError:
            message = "\nCE CHOIX N'EXISTE PAS.\nVeuillez taper un chiffre entre 0 et {}."\
                .format(len(self.get_id_name_categories()))
            self.cli.display_message(message)
            self.propose_categories()


    def propose_foods(self):
        """ choice of food """
        # display the foods
        text = "\nRenseignez le numéro de l'aliment choisi :\nchoix 0 > Retourner aux catégories"
        i = 0
        dict_equivalence_i_id_food = {}
        for id_foods, name_foods in self.get_id_name_foods():
            i += 1
            text_choices = "\nchoix {} > {}".format(i, name_foods)
            text = text + text_choices
            dict_equivalence_i_id_food[i] = id_foods

        # user's answer
        self.user_answer_i_food = int(self.cli.question_answer(text))
        # id recovery from i (choice number)
        self.user_answer_id_food = dict_equivalence_i_id_food.get(int(self.user_answer_i_food))
        try:
            if self.user_answer_i_food <= len(self.get_id_name_foods()) \
                    and self.user_answer_i_food != 0:
                self.propose_substitute(0)
            elif self.user_answer_i_food == 0:
                self.propose_categories()

            # if the answer does not exist
            else:
                message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et {}."\
                    .format(len(self.get_id_name_foods()))
                self.cli.display_message(message)
                self.propose_foods()
        except ValueError:
            message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et {}." \
                .format(len(self.get_id_name_foods()))
            self.cli.display_message(message)
            self.propose_foods()


    def propose_substitute(self, read_line_substitute):
        """ detail of the substitute and choice to save it """

        def order_letters(letter):
            """ indicates the location number of letters of the alphabet """
            return int(ord(letter) - ord('a') + 1)

        food_chooses_and_substitute = self.get_food_chooses_substitute(read_line_substitute)

        # if the food chosen does not have a substitute
        if order_letters(food_chooses_and_substitute[0][1]) \
                <= order_letters(food_chooses_and_substitute[0][3]):
            self.no_substitute(food_chooses_and_substitute[0][0])

        # if the food chosen have a substitute > display the detail of the substitute
        else:
            message = ""
            text_list = ["L'aliment :", "Nutriscore :", "Peut être remplacé par :", "Nutriscore :", "Description :",
                         "Magasins où le trouver :", "Lien internet :"]
            i = 0
            for elt in text_list:
                text_substitute = "\n {} {}".format(elt, food_chooses_and_substitute[0][i])
                i += 1
                message = message + text_substitute
            self.cli.display_message(message)
            self.save_substituted_food(food_chooses_and_substitute[0][0], read_line_substitute)

    def no_substitute(self, name_food_chooses):
        """ the food chosen does not have a substitute,
        propose a new search or return to the menu """
        # new choices
        text = "\nL'aliment {}" \
                " n'a pas d'autres substituts possibles." \
                "\n\nSouhaitez-vous faire une nouvelle recherche ?" \
                "\nchoix 1 > oui" \
                "\nchoix 2 > non".format(name_food_chooses)

        user_answer = self.cli.question_answer(text)

        if user_answer == "1":
            self.propose_categories()
        elif user_answer == "2":
            self.menu()

        # if the answer does not exist
        else:
            message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2."
            self.cli.display_message(message)
            self.no_substitute(name_food_chooses)


    def save_substituted_food(self, name_substitute, read_line_substitute):
        """ propose save or another substitute """
        # question to the user
        text = "\nSouhaitez-vous enregistrer l'aliment et son substitut ? " \
                "\nchoix 1 > oui " \
                "\nchoix 2 > non " \
                "\nchoix 3 > Je souhaite un autre substitut possible"

        user_answer = self.cli.question_answer(text)

        try:
            # use Database method for save substituted food and his substitute into database
            if user_answer == "1":
                self.save_favorite_food(name_substitute)
                message = "\nNous avons bien enregistré l'aliment et son substitut {}.".format(name_substitute)
                self.cli.display_message(message)
                self.menu()

            # no save substituted food and his substitute
            elif user_answer == "2":
                message = "\nEnregistrement non effectué."
                self.cli.display_message(message)
                self.menu()

            # propose a new substitute
            elif user_answer == "3":
                read_line_substitute += 1
                self.propose_substitute(0 + read_line_substitute)

            # if the answer does not exist or if the food is already registered
            else:
                message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3."
                self.cli.display_message(message)
                self.save_substituted_food(name_substitute, read_line_substitute)
        except ValueError:
            message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3."
            self.cli.display_message(message)
            self.save_substituted_food(name_substitute, read_line_substitute)
        except IntegrityError:
            message = "\nCet aliment et son substitut sont déjà enregistrés."
            self.cli.display_message(message)
            self.show_food_and_substitute()


    def show_food_and_substitute(self):
        """ show the favorite foods """

        all_id_name_substitute = self.get_favorite_food_and_substitute()[0]
        all_substituted_food = self.get_favorite_food_and_substitute()[1]

        print(all_id_name_substitute)
        print(all_substituted_food)
        # if not exist favorite foods
        if not all_id_name_substitute:
            print("\nVous n'avez pas d'aliments substitués enregistrés.")
            self.menu()

        # display favorite foods
        else:
            print("\nVoici vos aliments et substituts enregistrés :"
                  "\nchoix 0 > quitter mes aliments et substituts enregistrés")
            i = 0
            text = ""
            dict_equivalence_i_id_food_substitute = {}
            list = range(0, len(all_substituted_food))
            for elt in list:
                i += 1
                text_choices = "choix {} > {} (substitué par {})".format(i, all_substituted_food[i], all_id_name_substitute[i][1])

                dict_equivalence_i_id_food_substitute[i] = all_id_name_substitute[i][0]

                text = text + text_choices
            user_answer_choice_i_substitute = self.cli.question_answer(text)
            print("Tapez un choix pour avoir plus de détail sur le substitut ou le supprimer.")

            # user's answer
            try:
                user_answer_choice_id_substitute = dict_equivalence_i_id_food_substitute.get\
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
        self.text = "\nAliment : {0}" \
                    "\nNutriscore : {1} " \
                    "\nDescription : {2} " \
                    "\nMagasin(s) où le trouver : {3} " \
                    "\nLien d'information : {4} " \
                    "\n\nVous souhaitez : " \
                    "\nchoix 1 : supprimer cet aliment" \
                    "\nchoix 2 : chercher un autre aliment substitué enregistré" \
                    "\nchoix 3 : retourner au menu".format((show_substitute[0])[0], (show_substitute[0])[1],
                                                           (show_substitute[0])[2],(show_substitute[0])[3],
                                                           (show_substitute[0])[4])

        self.question_answer()

        if int(self.user_answer) == 1:
            self.delete_food_substitute(user_answer_choice_id_substitute)
        elif int(self.user_answer) == 2:
            self.show_food_and_substitute()
        elif int(self.user_answer) == 3:
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

# instantiate the class Controller and call menu() method
NEW_CONTROLLER = Controller()
NEW_CONTROLLER.menu()