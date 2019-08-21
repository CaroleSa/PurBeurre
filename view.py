#! /usr/bin/env python3
# coding: UTF-8

""" Class CommandLineInterface """


# import
import controller as ct



class CommandLineInterface:
    """ Command line interface"""

    @classmethod
    def question_answer(cls, text, text_input="Tapez votre choix : "):
        """ displays the question and retrieves the user's answer """
        print(text)
        user_answer = input(text_input)
        return user_answer

    @classmethod
    def display_message(cls, message):
        """ displays the message """
        print(message)


def main():
    """ call class Controller """
    ct.Controller()

if __name__ == "main":
    # execute only if run as a script
    main()
