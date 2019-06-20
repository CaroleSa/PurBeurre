#! /usr/bin/env python3
# coding: UTF-8

""" Class User """



# import file
import database as db



class User:
    """ Command line interface"""

    def __init__(self):
        # instantiate the class Database, use data_base attribute and creation cursor
        new_database = db.Database()
        self.data_base = new_database.data_base
        self.cursor = self.data_base.cursor()

        self.user_answer_category = 0
        self.user_answer_food = 0
        self.user_answer_choice_substitute = 0
        self.name_food_chooses = ""
        self.name_substitute = ""
        self.i = 0
        self.dict_food = {}

    def first_question(self):
        # first question at the user :
        print("\nRenseignez votre choix avant de valider : \nchoix 1 > Quel aliment souhaitez-vous remplacer ?"
                                "\nchoix 2 > Retrouver mes aliments substitués \nchoix 3 > Quitter")
        user_answer = input("Tapez votre choix : ")

        if str(user_answer) == "1":
            self.answer_choice_1_category()
        elif str(user_answer) == "2":
            self.answer_choice_2()
        elif str(user_answer) == "3":
            print("\nMerci pour votre visite et à bientôt !")
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2.")
            self.first_question()

    def answer_choice_1_category(self):
        # if the user chooses the option 1,
        # he chooses the category :
        print("\nRenseignez le numéro de la catégorie choisie :")

        # display of categories
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("SELECT id, categories FROM Category ORDER BY id;")
        result_categories = self.cursor.fetchall()
        print("choix 0 > Retourner au menu")
        for id, categories in result_categories:
            print("choix", id, ">", categories)

        # the user chooses one category
        self.user_answer_category = input("Votre choix : ")

        # if wrong answer
        try:
            if int(self.user_answer_category) <= len(result_categories) and int(self.user_answer_category) != 0:
                self.answer_choice_1_food()
            elif int(self.user_answer_category) == 0:
                self.first_question()
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(result_categories), ".")
                self.answer_choice_1_category()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(result_categories), ".")
            self.answer_choice_1_category()

    def answer_choice_1_food(self):
        # he chooses the food of the category :
        print("\nRenseignez le numéro de l'aliment choisi :")

        # display of foods
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT id, name_food 
                            FROM Food
                            WHERE category_id = {};""".format(self.user_answer_category))
        result_food = self.cursor.fetchall()

        print("choix 0 > Retourner aux catégories")
        i = 0
        for id, name_food in result_food:
            i += 1
            print("choix", i, ">", name_food)
            self.dict_food[i] = id

        # the user chooses one food
        self.user_answer_food = input("Votre choix : ")

        # if wrong answer
        try:
            if int(self.user_answer_food) <= len(result_food) and int(self.user_answer_food) != 0:
                self.proposed_substitute(0)
            elif int(self.user_answer_food) == 0:
                self.answer_choice_1_category()
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(result_food), ".")
                self.answer_choice_1_food()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(result_food), ".")
            self.answer_choice_1_food()

    def proposed_substitute(self, line):
        # Detail of the proposed food substitute and choice to save it
        self.cursor.execute("USE Purbeurre;")
        if line == 0:
            self.user_answer_food = self.dict_food.get(int(self.user_answer_food))

        select_substitute = """SELECT (SELECT name_food FROM Food WHERE id = {1}) as name_food_chooses, 
                            (SELECT nutriscore FROM Food WHERE id = {1}) as nutriscore_of_food_chooses, 
                            name_food, nutriscore, description, store, link
                            FROM Food
                            WHERE category_id = {0}
                            ORDER BY nutriscore
                            LIMIT {2},1;""".format(self.user_answer_category, self.user_answer_food, line)
        self.cursor.execute(select_substitute)

        result_substitute = self.cursor.fetchall()

        for self.name_food_chooses, nutriscore_of_food_chooses, self.name_substitute, nutriscore_substitute, \
            description_substitute, store_substitute, link_substitute in result_substitute:

            if self.order_letters(nutriscore_of_food_chooses) <= self.order_letters(nutriscore_substitute) :
                self.no_substitute()

            else:
                print("\nL'aliment", self.name_food_chooses, "(Nutriscore :", nutriscore_of_food_chooses,
                      ") peut être remplacé par", self.name_substitute, ":\nnutriscore :", nutriscore_substitute,
                      "\nDescription :", description_substitute, "\nMagasin(s) où le trouver :", store_substitute,
                      "\nLien internet :", link_substitute)
                self.save_substitute()

    def no_substitute(self):
        print("\nL'aliment", self.name_food_chooses, "n'a pas d'autres substituts possibles.\n"
              "Souhaitez-vous faire une nouvelle recherche ? \nchoix 1 > Oui \nchoix 2 > Non")
        user_answer_new_search = input("Votre choix : ")
        if user_answer_new_search == "1":
            self.answer_choice_1_category()
        elif user_answer_new_search == "2":
            self.first_question()
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2.")
            self.no_substitute()

    def save_substitute(self):
        # Confirmation of registration
        print("\nSouhaitez-vous enregistrer ce substitut ? \nchoix 1 > Oui \nchoix 2 > Non "
              "\nchoix 3 > Je souhaite un autre substitut possible")
        user_answer_save_food = input("Votre choix : ")

        try:
            if user_answer_save_food == "1":
                 save_favorite_substitute = """INSERT IGNORE INTO Favorite (id_food, id_substitute_chooses)
                                            VALUES({0}, (SELECT id FROM Food WHERE name_food = {1}));"""\
                                            .format(int(self.user_answer_food), "\'"+self.name_substitute+"\'")
                 self.cursor.execute(save_favorite_substitute)
                 self.data_base.commit()
                 print("\nNous avons bien enregistré le substitut", self.name_substitute+".")
                 self.first_question()
            elif user_answer_save_food == "2":
                print("\nEnregistrement non effectué pour le substitut", self.name_substitute+".")
                self.first_question()
            elif user_answer_save_food == "3":
                self.i += 1
                self.proposed_substitute(0 + self.i)
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3.")
                self.save_substitute()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3.")
            self.save_substitute()

    def answer_choice_2(self):
        # If the user chooses the option 2 :
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT Favorite.id, Food.name_food
                            FROM Food 
                            JOIN Favorite ON Food.id = Favorite.id_substitute_chooses 
                            WHERE Food.id = Favorite.id_substitute_chooses
                            ORDER BY Favorite.id;""")
        show_favorite_substitute = self.cursor.fetchall()

        self.cursor.execute("""SELECT Food.name_food 
                            FROM Food
                            JOIN Favorite ON Food.id = Favorite.id_food
                            WHERE Food.id = Favorite.id_food
                            ORDER BY Favorite.id;""")
        show_food_substitute = self.cursor.fetchall()

        if len(show_favorite_substitute) == 0:
            print("\nVous n'avez pas encore enregistré de substituts")
            self.first_question()
        else:
            print("\nVoici vos aliments substitués enregistrés :\nchoix 0 > quitter mes substituts enregistrés")
            for id_name_substitute, name_food_substitute in zip(show_favorite_substitute, show_food_substitute):
                print("choix", id_name_substitute[0], ">", id_name_substitute[1], "(substitut de", name_food_substitute[0]+")")

            self.user_answer_choice_substitute = input("Tapez un choix pour plus de détail : ")

            self.detail_substitute(show_food_substitute)

    def detail_substitute(self, data):
        # if wrong answer
        try:
            if int(self.user_answer_choice_substitute) <= len(data) \
                    and int(self.user_answer_choice_substitute) != 0:
                self.cursor.execute("""SELECT name_food, nutriscore, description, store, link
                                    FROM Food 
                                    WHERE id = (SELECT id_substitute_chooses FROM Favorite WHERE id = {});"""
                                    .format(int(self.user_answer_choice_substitute)))
                show_substitute = self.cursor.fetchall()

                for name_substitute, nutriscore_substitute, description_substitute, store_substitute, link_substitute \
                        in show_substitute :
                    print("\nAliment : ", name_substitute, "\nNutriscore : ", nutriscore_substitute,
                          "\nDescription : ", description_substitute, "\nMagasin(s) où le trouver : ", store_substitute,
                          "\nLien d'information : ", link_substitute, "\n\nVous souhaitez : "
                          "\nchoix 1 : retourner au menu \nchoix 2 : voir un autre substitut favorit")
                    user_answer_return_substitute_menu = input("Votre choix : ")

                    if int(user_answer_return_substitute_menu) == 1 :
                        self.first_question()
                    elif int(user_answer_return_substitute_menu) == 2 :
                        self.answer_choice_2()
                    else:
                        print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2")
                        self.detail_substitute()

            elif int(self.user_answer_choice_substitute) == 0:
                self.first_question()
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(show_food_substitute), ".")
                self.answer_choice_2()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(show_food_substitute), ".")
            self.answer_choice_2()

    def order_letters(self, letter):
        return int(ord(letter) - ord('a') + 1)

# instantiate the class User and call User() method
new_user = User()
new_user.first_question()

def main():
    """ use of class Database """
    db.Database()

if __name__ == "_main_":
    # execute only if run as a script
    main()






