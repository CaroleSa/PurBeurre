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

        # attributes
        self.user_answer_id_category = 0
        self.user_answer_i_food = 0
        self.dict_equivalence_i_id_food = {}

    def menu(self):
        # first question at the user :
        print("\nRenseignez votre choix avant de valider : \nchoix 1 > Quel aliment souhaitez-vous remplacer ?"
                                "\nchoix 2 > Retrouver mes aliments substitués \nchoix 3 > Quitter")
        user_answer_choice_menu = input("Tapez votre choix : ")

        if str(user_answer_choice_menu) == "1":
            self.proposed_category()
        elif str(user_answer_choice_menu) == "2":
            self.show_food_substitute()
        elif str(user_answer_choice_menu) == "3":
            print("\nMerci pour votre visite et à bientôt !")
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3.")
            self.menu()

    def proposed_category(self):
        # if the user chooses the option 1,
        # he chooses the category :
        print("\nRenseignez le numéro de la catégorie choisie :")

        # display of categories
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("SELECT id, categories FROM Category ORDER BY id;")
        all_id_name_categories = self.cursor.fetchall()
        print("choix 0 > Retourner au menu")
        for id, categories in all_id_name_categories:
            print("choix", id, ">", categories)

        # the user chooses one category
        self.user_answer_id_category = input("Votre choix : ")

        # if wrong answer
        try:
            if int(self.user_answer_id_category) <= len(all_id_name_categories) \
                    and int(self.user_answer_id_category) != 0:
                self.proposed_food()
            elif int(self.user_answer_id_category) == 0:
                self.menu()
            else:
                print("\nCE CHOIX N'EXISTE PAS. "
                      "\nVeuillez taper un chiffre entre 0 et", len(all_id_name_categories), ".")
                self.proposed_category()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. "
                  "\nVeuillez taper un chiffre entre 0 et", len(all_id_name_categories), ".")
            self.proposed_category()

    def proposed_food(self):
        # he chooses the food of the category :
        print("\nRenseignez le numéro de l'aliment choisi :")

        # display of foods
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT id, name_food 
                            FROM Food
                            WHERE category_id = {};""".format(self.user_answer_id_category))
        all_id_name_food = self.cursor.fetchall()

        print("choix 0 > Retourner aux catégories")
        i = 0
        for id, name_food in all_id_name_food:
            i += 1
            print("choix", i, ">", name_food)
            self.dict_equivalence_i_id_food[i] = id

        # the user chooses one food
        self.user_answer_i_food = input("Votre choix : ")

        # if wrong answer
        try:
            if int(self.user_answer_i_food) <= len(all_id_name_food) and int(self.user_answer_i_food) != 0:
                self.proposed_substitute(0)
            elif int(self.user_answer_i_food) == 0:
                self.proposed_category()
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(all_id_name_food), ".")
                self.proposed_food()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(all_id_name_food), ".")
            self.proposed_food()

    def proposed_substitute(self, read_line_substitute):
        # Detail of the proposed food substitute and choice to save it
        self.cursor.execute("USE Purbeurre;")

        user_answer_id_food = self.dict_equivalence_i_id_food.get(int(self.user_answer_i_food))

        select_substitute = """SELECT (SELECT name_food FROM Food WHERE id = {1}) as name_food_chooses, 
                            (SELECT nutriscore FROM Food WHERE id = {1}) as nutriscore_of_food_chooses, 
                            name_food, nutriscore, description, store, link
                            FROM Food
                            WHERE category_id = {0}
                            ORDER BY nutriscore LIMIT {2},1;"""\
                            .format(self.user_answer_id_category, user_answer_id_food, read_line_substitute)
        self.cursor.execute(select_substitute)

        result_food_chooses_and_substitute = self.cursor.fetchall()

        for name_food_chooses, nutriscore_of_food_chooses, name_substitute, nutriscore_substitute, \
            description_substitute, store_substitute, link_substitute in result_food_chooses_and_substitute:

            if self.order_letters(nutriscore_of_food_chooses) < self.order_letters(nutriscore_substitute) :
                self.no_substitute(name_food_chooses)

            else:
                print("\nL'aliment", name_food_chooses, "(Nutriscore :", nutriscore_of_food_chooses,
                      ") peut être remplacé par", name_substitute, ":\nnutriscore :", nutriscore_substitute,
                      "\nDescription :", description_substitute, "\nMagasin(s) où le trouver :", store_substitute,
                      "\nLien internet :", link_substitute)
                self.save_substitute(name_substitute, read_line_substitute, user_answer_id_food)

    def no_substitute(self, name_food):
        print("\nL'aliment", name_food, "n'a pas d'autres substituts possibles.\n"
              "Souhaitez-vous faire une nouvelle recherche ? \nchoix 1 > Oui \nchoix 2 > Non")
        user_answer_new_search = input("Votre choix : ")
        if user_answer_new_search == "1":
            self.proposed_category()
        elif user_answer_new_search == "2":
            self.menu()
        else:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2.")
            self.no_substitute(name_food)

    def save_substitute(self, name_substitute, read_line_substitute, user_answer_id_food):
        # Confirmation of registration
        print("\nSouhaitez-vous enregistrer l'aliment et son substitut ? \nchoix 1 > Oui \nchoix 2 > Non "
              "\nchoix 3 > Je souhaite un autre substitut possible")
        user_answer_save_food = input("Votre choix : ")

        try:
            if user_answer_save_food == "1":
                 save_favorite_food_substitute = """INSERT IGNORE INTO Favorite (id_food, id_substitute_chooses)
                                            VALUES({0}, (SELECT id FROM Food WHERE name_food = {1}));"""\
                                            .format(int(user_answer_id_food), "\'"+name_substitute+"\'")
                 self.cursor.execute(save_favorite_food_substitute)
                 self.data_base.commit()
                 print("\nNous avons bien enregistré l'aliment et son substitut", name_substitute+".")
                 self.menu()
            elif user_answer_save_food == "2":
                print("\nEnregistrement non effectué.")
                self.menu()
            elif user_answer_save_food == "3":
                read_line_substitute += 1
                self.proposed_substitute(0 + read_line_substitute)
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3.")
                self.save_substitute(name_substitute, read_line_substitute, user_answer_id_food)
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1, 2 ou 3.")
            self.save_substitute(name_substitute, read_line_substitute, user_answer_id_food)

    def show_food_substitute(self):
        # If the user chooses the option 2 :
        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""SELECT Favorite.id, Food.name_food
                            FROM Food 
                            JOIN Favorite ON Food.id = Favorite.id_substitute_chooses 
                            WHERE Food.id = Favorite.id_substitute_chooses
                            ORDER BY Favorite.id;""")
        all_id_name_substitute = self.cursor.fetchall()

        self.cursor.execute("""SELECT Food.name_food 
                            FROM Food
                            JOIN Favorite ON Food.id = Favorite.id_food
                            WHERE Food.id = Favorite.id_food
                            ORDER BY Favorite.id;""")
        all_food_substitute = self.cursor.fetchall()

        if len(all_id_name_substitute) == 0:
            print("\nVous n'avez pas encore enregistré de substituts")
            self.menu()
        else:
            print("\nVoici vos aliments et substitus enregistrés :\nchoix 0 > quitter mes substituts enregistrés")
            for id_name_substitute, name_food_substitute in zip(all_id_name_substitute, all_food_substitute):
                print("choix", id_name_substitute[0], ">", name_food_substitute[0],
                      "(substitué par", id_name_substitute[1]+")")

            user_answer_choice_id_substitute = input("Tapez un choix pour avoir plus de détail sur le substitut "
                                                     "ou le supprimer : ")

            self.detail_substitute(all_food_substitute, user_answer_choice_id_substitute)

    def detail_substitute(self, all_food_substitute, user_answer_choice_id_substitute):
        # if wrong answer
        try:
            if int(user_answer_choice_id_substitute) <= len(all_food_substitute) \
                    and int(user_answer_choice_id_substitute) != 0:
                self.cursor.execute("""SELECT name_food, nutriscore, description, store, link
                                    FROM Food 
                                    WHERE id = (SELECT id_substitute_chooses FROM Favorite WHERE id = {});"""
                                    .format(int(user_answer_choice_id_substitute)))
                show_substitute = self.cursor.fetchall()

                for name_substitute, nutriscore_substitute, description_substitute, store_substitute, link_substitute \
                        in show_substitute :
                    print("\nAliment : ", name_substitute, "\nNutriscore : ", nutriscore_substitute,
                          "\nDescription : ", description_substitute, "\nMagasin(s) où le trouver : ", store_substitute,
                          "\nLien d'information : ", link_substitute, "\n\nVous souhaitez : "
                          "\nchoix 1 : supprimer cet aliment\nchoix 2 : chercher un autre aliment substitué enregistré"
                          "\nchoix 3 : retourner au menu")
                    user_answer_return_delete_substitute_menu = input("Votre choix : ")

                    if int(user_answer_return_delete_substitute_menu) == 1 :
                        self.delete_food_substitute(user_answer_choice_id_substitute)
                    elif int(user_answer_return_delete_substitute_menu) == 2 :
                        self.show_food_substitute()
                    elif int(user_answer_return_delete_substitute_menu) == 3 :
                        self.menu()
                    else:
                        print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper 1 ou 2")
                        self.detail_substitute(all_food_substitute, user_answer_choice_id_substitute)

            elif int(user_answer_choice_id_substitute) == 0:
                self.menu()
            else:
                print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(all_food_substitute), ".")
                self.show_food_substitute()
        except ValueError:
            print("\nCE CHOIX N'EXISTE PAS. \nVeuillez taper un chiffre entre 0 et", len(all_food_substitute), ".")
            self.show_food_substitute()

    def delete_food_substitute(self, user_answer_choice_id_substitute):

        self.cursor.execute("USE Purbeurre;")
        self.cursor.execute("""DELETE FROM Favorite where id = {};""".format(int(user_answer_choice_id_substitute)))
        self.data_base.commit()
        print("L'aliment a bien été supprimé.")
        self.show_food_substitute()

    def order_letters(self, letter):
        return int(ord(letter) - ord('a') + 1)

# instantiate the class User and call User() method
new_user = User()
new_user.menu()

def main():
    """ use of class Database """
    db.Database()

if __name__ == "_main_":
    # execute only if run as a script
    main()






