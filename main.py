#! /usr/bin/env python3
# coding: UTF-8

""" Class CommandLineInterface """





import controller as ct
# pylint: disable=too-many-function-args



class CommandLineInterface:
    """ Command line interface"""

    def question_answer(self, text):
        """ displays the question and retrieves the user's answer """
        print(text)
        self.user_answer = input("Tapez votre choix : ")
        return self.user_answer

    def display_message(self, message):
        print(message)

def main():
    """ use of class Controller """
    ct

if __name__ == "main":
    # execute only if run as a script
    main()
