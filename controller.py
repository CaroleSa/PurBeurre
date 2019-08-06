#! /usr/bin/env python3
# coding: UTF-8

""" Class Controller """



# imports
from mysql.connector.errors import IntegrityError
import database
import view
import model




class Controller:
    """ logic and program direction """


    def __init__(self):
        """ constructor """
        # instantiate the class Database and CommandLineInterface
        self.new_database = database.Database()
        self.new_cli = view.CommandLineInterface()

        # attributes
        self.user_answer_id_category = 0
        self.user_answer_id_food = 0


    def get_id_name_categories(self):
        """ use database for selected the name and id categories """
        # call Database method
        new_categories = model.Categories()
        all_id_name_categories = new_categories.all_id_name_categories
        return all_id_name_categories


    def get_id_name_foods(self):
        """ use database for selected the name and id foods """
        # call Database method
        new_foods = model.Foods()
        all_id_name_foods = new_foods.all_id_name_foods
        return all_id_name_foods


    def get_food_chooses_substitute(self, read_line_substitute):
        """ select the substituted food and this substitute """
        # call Database method
        result_food_chooses_and_substitute = self.new_database.select_substitute\
            (self.user_answer_id_category, self.user_answer_id_food, read_line_substitute)
        return result_food_chooses_and_substitute


    def save_favorite_food(self, name_substitute):
        """ save favorite food """
        # call Database method
        self.new_database.insert_favorite_food(self.user_answer_id_food, name_substitute)


    def get_favorite_foods_and_substitute(self):
        """ select the favorite foods and their substitutes """
        # call Database method
        all_id_name_substitute_and_substituted_food = self.new_database.select_favorite_foods()
        return all_id_name_substitute_and_substituted_food


    def get_detail_substitute(self, user_answer_choice_id_substitute):
        """ select the detail of the substitute chooses """
        # call Database method
        show_substitute = self.new_database.select_detail_substitute \
            (user_answer_choice_id_substitute)
        return show_substitute


    def delete_favorite_food(self, user_answer_choice_id_substitute):
        """ delete favorite food """
        # call Database method
        self.new_database.delete_favorite_food(user_answer_choice_id_substitute)


    def menu(self):
        """ menu """
        # creation of the text : first question to the user (menu)
        text = "\nRenseignez votre choix avant de valider : " \
                "\nchoix 1 > Quel aliment souhaitez-vous remplacer ?" \
                "\nchoix 2 > Retrouver mes aliments substitués" \
                "\nchoix 3 > Quitter"

        # call cli method to display the text and recovery of the user input
        user_answer = str(self.new_cli.question_answer(text))

        # conditions
        if user_answer == "1":
            self.propose_categories()
        elif user_answer == "2":
            self.show_food_and_substitute()
        elif user_answer == "3":
            message = "\nMerci pour votre visite et à bientôt !"
            self.new_cli.display_message(message)

        # if the answer does not exist
        else:
            message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3."
            self.new_cli.display_message(message)
            self.menu()


    def propose_categories(self):
        """ choice of category """
        # creation of the text which proposes the categories list
        text = "\nRenseignez le numéro de la catégorie choisie :\nchoix 0 > Retourner au menu"
        for id_categories, name_categories in self.get_id_name_categories():
            text_choices = "\nchoix {} > {}".format(id_categories, name_categories)
            text = text + text_choices

        # call cli method to display the text and recovery of the user input
        self.user_answer_id_category = int(self.new_cli.question_answer(text))

        try:
            # conditions
            if self.user_answer_id_category <= len(self.get_id_name_categories()) \
                    and self.user_answer_id_category != 0:
                self.propose_foods()
            elif self.user_answer_id_category == 0:
                self.menu()

            # if the answer does not exist
            else:
                message = "\nCE CHOIX N'EXISTE PAS.\nVeuillez taper un chiffre entre 0 et {}."\
                    .format(len(self.get_id_name_categories()))
                self.new_cli.display_message(message)
                self.propose_categories()

        except ValueError:
            message = "\nCE CHOIX N'EXISTE PAS.\nVeuillez taper un chiffre entre 0 et {}."\
                .format(len(self.get_id_name_categories()))
            self.new_cli.display_message(message)
            self.propose_categories()


    def propose_foods(self):
        """ choice of food """
        # creation of the text which proposes the foods list
        text = "\nRenseignez le numéro de l'aliment choisi :\nchoix 0 > Retourner aux catégories"

        dict_equivalence_i_id_food = {} # creation of a dictionary
        i = 0
        for id_foods, name_foods in self.get_id_name_foods():
            i += 1
            text_choices = "\nchoix {} > {}".format(i, name_foods)
            text = text + text_choices

            # addition of elements in the dictionary : choice number and food id
            dict_equivalence_i_id_food[i] = id_foods

        # call cli method to display the text and recovery of the user input
        user_answer_i_food = int(self.new_cli.question_answer(text))

        # recovery of the chosen food id
        self.user_answer_id_food = dict_equivalence_i_id_food.get(int(user_answer_i_food))

        try:
            # conditions
            if user_answer_i_food <= len(self.get_id_name_foods()) \
                    and user_answer_i_food != 0:
                self.propose_substitute(0)
            elif user_answer_i_food == 0:
                self.propose_categories()

            # if the answer does not exist
            else:
                message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et {}."\
                    .format(len(self.get_id_name_foods()))
                self.new_cli.display_message(message)
                self.propose_foods()

        except ValueError:
            message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et {}." \
                .format(len(self.get_id_name_foods()))
            self.new_cli.display_message(message)
            self.propose_foods()


    def propose_substitute(self, read_line_substitute):
        """ detail of the substitute and choice to save it """

        def order_letters(letter):
            """ indicates the location number of letters of the alphabet """
            return int(ord(letter) - ord('a') + 1)

        # call controller method. This list contains :
        # [0][0] name food chooses     [0][1] nutriscore of the food chooses
        # [0][2] name substitute       [0][3] nutriscore of the substitute
        # [0][4] description of the substitute
        # [0][5] shop or buy it        [0][6] internet link
        food_chooses_and_substitute = self.get_food_chooses_substitute(read_line_substitute)

        # if the food chosen does not have a substitute
        if order_letters(food_chooses_and_substitute[0][1]) \
                <= order_letters(food_chooses_and_substitute[0][3]):
            self.no_substitute(food_chooses_and_substitute[0][0])

        # if the food chosen have a substitute
        else:
            # creation of the message : detail of the substitute
            message = ""
            text_list = ["L'aliment", "Nutriscore", "Peut être remplacé par", "Nutriscore",
                         "Description", "Magasin(s) où le trouver", "Lien internet"]
            i = 0
            for elt in text_list:
                text_substitute = "\n {} : {}".format(elt, food_chooses_and_substitute[0][i])
                i += 1
                message = message + text_substitute

            # call cli method to display the message
            self.new_cli.display_message(message)

            # call controller method "save_substituted_food"
            self.save_substituted_food(food_chooses_and_substitute[0][2], read_line_substitute)


    def no_substitute(self, name_food_chooses):
        """ the food chosen does not have a substitute,
        propose a new search or return to the menu """
        # creation of the text which proposes new choices
        text = "\nL'aliment {}" \
                " n'a pas d'autres substituts possibles." \
                "\n\nSouhaitez-vous faire une nouvelle recherche ?" \
                "\nchoix 1 > oui" \
                "\nchoix 2 > non".format(name_food_chooses)

        # call cli method to display the text and recovery of the user input
        user_answer = self.new_cli.question_answer(text)

        # conditions
        if user_answer == "1":
            self.propose_categories()
        elif user_answer == "2":
            self.menu()

        # if the answer does not exist
        else:
            message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2."
            self.new_cli.display_message(message)
            self.no_substitute(name_food_chooses)


    def save_substituted_food(self, name_substitute, read_line_substitute):
        """ propose save or another substitute """
        # creation of the text which proposes new choices
        text = "\nSouhaitez-vous enregistrer l'aliment et son substitut ? " \
                "\nchoix 1 > oui " \
                "\nchoix 2 > non " \
                "\nchoix 3 > Je souhaite un autre substitut possible"

        # call cli method to display the text and recovery of the user input
        user_answer = self.new_cli.question_answer(text)

        try:
            # conditions
            if user_answer == "1":
                # save substituted food and his substitute
                self.save_favorite_food(name_substitute)
                message = "\nNous avons bien enregistré l'aliment et son substitut {}."\
                    .format(name_substitute)
                self.new_cli.display_message(message)
                self.menu()

            elif user_answer == "2":
                # no save substituted food and his substitute
                message = "\nEnregistrement non effectué."
                self.new_cli.display_message(message)
                self.menu()

            elif user_answer == "3":
                # propose a new substitute
                read_line_substitute += 1
                self.propose_substitute(0 + read_line_substitute)

            # if the answer does not exist or if the food is already registered
            else:
                message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3."
                self.new_cli.display_message(message)
                self.save_substituted_food(name_substitute, read_line_substitute)

        except ValueError:
            message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3."
            self.new_cli.display_message(message)
            self.save_substituted_food(name_substitute, read_line_substitute)

        except IntegrityError:
            message = "\nCet aliment et son substitut sont déjà enregistrés."
            self.new_cli.display_message(message)
            self.show_food_and_substitute()


    def show_food_and_substitute(self):
        """ show the favorite foods """
        # call Controller method : select the favorite foods and their substitutes
        all_id_name_substitute = self.get_favorite_foods_and_substitute()[0]
        all_substituted_food = self.get_favorite_foods_and_substitute()[1]

        # if not exist favorite foods
        if not all_id_name_substitute:
            message = "\nVous n'avez pas d'aliments substitués enregistrés."
            self.new_cli.display_message(message)
            self.menu()

        # if exist favorite foods
        else:
            # creation of the text which proposes the favorite foods list
            text = "\nVoici vos aliments et substituts enregistrés :" \
                   "\nchoix 0 > quitter mes aliments et substituts enregistrés"

            dict_equivalence_i_id_food_substitute = {}  # creation of a dictionary
            i = 0
            for id_name_substitute, name_substituted_food in zip(all_id_name_substitute,
                                                                 all_substituted_food):
                i += 1
                text_choices = "\nchoix {} > {} (substitué par {})"\
                    .format(i, name_substituted_food[0], id_name_substitute[1])
                text = text + text_choices

                # addition of elements in the dictionary : choice number and favorite food id
                dict_equivalence_i_id_food_substitute[i] = id_name_substitute[0]

            # call cli method to display the text and recovery of the user input
            text_input = "Tapez un choix pour avoir plus de détail sur le substitut " \
                         "ou le supprimer : "
            user_answer_choice_i_substitute = int(self.new_cli.question_answer(text, text_input))

            # recovery of the favorite food id
            user_answer_choice_id_substitute = dict_equivalence_i_id_food_substitute.get\
                (user_answer_choice_i_substitute)

            try:
                # conditions
                if user_answer_choice_i_substitute <= len(all_substituted_food) \
                        and user_answer_choice_i_substitute != 0:
                    self.detail_substitute(all_substituted_food, user_answer_choice_id_substitute)
                elif user_answer_choice_i_substitute == 0:
                    self.menu()

                # if the answer does not exist
                else:
                    message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et {}."\
                        .format(len(all_substituted_food))
                    self.new_cli.display_message(message)
                    self.show_food_and_substitute()

            except ValueError:
                message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et {}."\
                    .format(len(all_substituted_food))
                self.new_cli.display_message(message)
                self.show_food_and_substitute()


    def detail_substitute(self, all_substituted_food, user_answer_choice_id_substitute):
        """ display the detail of the substitute """
        # call Controller method : select the detail of the substitute
        show_substitute = self.get_detail_substitute(user_answer_choice_id_substitute)

        # creation of the message : detail of the favorite substitute
        text = ""
        text_list = ["Aliment", "Nutriscore", "Description", "Magasin(s) où le trouver",
                     "Lien internet"]
        i = 0
        for elt in text_list:
            text_substitute_favorite = "\n{} : {}".format(elt, (show_substitute[0])[i])
            i += 1
            text = text + text_substitute_favorite

        text_choices = "\n\nVous souhaitez : \nchoix 1 : supprimer cet aliment " \
                       "\nchoix 2 : chercher un autre aliment substitué enregistré" \
                       "\nchoix 3 : retourner au menu"
        text = text + text_choices

        # call cli method to display the text and recovery of the user input
        user_answer = self.new_cli.question_answer(text)

        # conditions
        if int(user_answer) == 1:
            self.delete_food_substitute(user_answer_choice_id_substitute)
        elif int(user_answer) == 2:
            self.show_food_and_substitute()
        elif int(user_answer) == 3:
            self.menu()

        # if the answer does not exist
        else:
            message = "\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2"
            self.new_cli.display_message(message)
            self.detail_substitute(all_substituted_food, user_answer_choice_id_substitute)


    def delete_food_substitute(self, user_answer_choice_id_substitute):
        """ deleted the favorite food and his substitute """
        # call Controller method to delete favorite food
        self.delete_favorite_food(user_answer_choice_id_substitute)

        # creation of the message : confirmation of deletion
        message = "\nL'aliment a bien été supprimé."

        # call cli method to display the message
        self.new_cli.display_message(message)

        # call Controller method "show_food_and_substitute"
        self.show_food_and_substitute()



# instantiate the class Controller and call "menu" method
NEW_CONTROLLER = Controller()
NEW_CONTROLLER.menu()
