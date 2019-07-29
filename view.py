#! /usr/bin/env python3
# coding: UTF-8

""" Class CommandLineInterface """


# import
import controller as ct
# pylint: disable=too-many-function-args



class CommandLineInterface:
    """ Command line interface"""

    def question_answer(self, text, text_input="Tapez votre choix : "):
        """ displays the question and retrieves the user's answer """
        print(text)
        user_answer = input(text_input)
        return user_answer

    def display_message(self, message):
        print(message)


def main():
    """ use of class Controller """
    ct

if __name__ == "main":
    # execute only if run as a script
    main()
