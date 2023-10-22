"""Module containing functions."""
import sys
import os
import random
import curses
from .classes import Item, Store # pylint: disable=relative-beyond-top-level

def screen_controller(stdscr=curses.initscr()):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)
    stdscr.refresh()
    start_menu(stdscr)
    t = stdscr.getkey()
    stdscr.getch()
    
    """menu_win = curses.newwin(10,50,0,0)
    menu_win.addstr("For this game, type what is prompted and press\nenter to proceed. Every time"\
        " you purchase items\nmarks the end of the turn. You may only buy one\ntype of item and "\
        "up to 10 of that item each turn.")
    menu_win.addstr(5,10,"Are you ready to begin?")
    menu_win.addstr(7,18,"(Y)es")
    menu_win.addstr(9,18,"(N)o")
    #inventory_win = curses.newwin(1, 20, 10, 10)
    #inventory_win.clear()
    #inventory_win.addstr("Test")
    #inventory_win.refresh()
    menu_win.refresh()
    stdscr.getch()
    stdscr.getch()"""

def start_menu(parent, start_menu_win=curses.newwin(15, 50, 1, 3)):
    """
    Function used to contain the user inputs for game setup.
    
    Returns:
    --------
        - store (Store): An instance of the class Store(store_name = result of user input, 
        store_funds = 30)
    """
    start_menu_win.addstr(
        "For this game, press the key marked in parenthesesto proceed. Every time you"\
        " purchase items marks\nthe end of the turn. You may only buy one\ntype of item and "\
        "up to 10 of that item each turn.")
    start_menu_win.addstr(5, 10, "Are you ready to begin?")
    start_menu_win.addstr(7, 18, "(Y)es", curses.A_REVERSE)
    start_menu_win.addstr(9, 18, "(N)o")
    start_menu_win.refresh()
    start_num = 0
    def yes_sel():
        start_menu_win.addstr(7, 18, "(Y)es", curses.A_REVERSE)
        start_menu_win.addstr(9, 18, "(N)o")
        start_menu_win.refresh()
    def no_sel():
        start_menu_win.addstr(7, 18, "(Y)es")
        start_menu_win.addstr(9, 18, "(N)o", curses.A_REVERSE)
        start_menu_win.refresh()
    # TODO Modify y_input to contain a dynamic version of the following block of code.
    cont = False
    while not cont:
        start_input = parent.getkey()
        if start_input == "Y" or start_input == "y":
            cont = True
        elif start_input == "N" or start_input == "n":
            sys.exit()
        elif start_input == "KEY_UP":
            if start_num == 0:
                start_num = 1
                no_sel()
            elif start_num == 1:
                start_num = 0
                yes_sel()
        elif start_input == "KEY_DOWN":
            if start_num == 0:
                start_num = 1
                no_sel()
            elif start_num == 1:
                start_num = 0
                yes_sel()
        elif start_input == "\n":
            if start_num == 0:
                cont = True
            elif start_num == 1:
                sys.exit()
        else:
            start_menu_win.addstr(11, 12, "Please press 'Y'/'N'", curses.color_pair(1))
            start_menu_win.refresh()
    start_menu_win.clear()
    start_menu_win.refresh()
    del start_menu_win

    """sponge = Item("Sponge", 3.50, 2.20, 0)
    soap = Item("Soap", 4.38, 3.08, 0)
    brush = Item("Brush", 6.20, 4.90, 0)
    milk = Item("Milk", 8.10, 6.80, 0)

    yn_input("For this game, type what is prompted and press enter to proceed. Every time "\
        "you purchase items marks the end of the turn. \nYou may only buy one type of item and up "\
        "to 10 of that item each turn. Are you ready to begin?\nPress Y/N: ", "exit")
    confirmed = False
    while not confirmed:
        store_name = input("What would you like the name of your store to be?\n")
        confirmed = yn_input(f"Confirm store name '{store_name.capitalize()}'.\nY/N: ", "continue", True)


    store = Store(store_name.capitalize(), 30)
    for item in [sponge, soap, brush, milk]:
        store.inventory.update({item.name: item})

    return store"""

def main_menu(menu_win=curses.newwin(10, 50, 1, 3)):
    menu_win.addstr(0, 21, "Main Menu")

def _yn_input(initial_msg:str, n_action:str, return_wanted=False) -> bool:
    """
    Function that will only accept a 'Y', "y", "N" or "n". Will loop until a valid input is 
    provided.
    
    Args:
    -----
        - initial_msg (str): The message that will be displayed at the start of this func.
        - n_action (str): String of the desired action when "N"/"n" is entered. Valid args: \
            "continue" & "exit"
        - return_wanted (bool): Determines whether a bool value will be returned upon completion \
            of the function. Default: False
    """
    invalid_input_txt = "Did you mean to type Y/N? "
    input_txt = initial_msg
    valid_input = False
    # While valid_in == False
    while not valid_input:
        start_in = input(input_txt)
        # If start_in == Y
        if start_in == "Y" or start_in == "y":
            valid_input = True
            if return_wanted is True:
                return True
        elif start_in == "N" or start_in == "n":
            if n_action == "exit":
                sys.exit()
            if return_wanted is True:
                return False
            elif n_action == "continue":
                continue
        else:
            input_txt = invalid_input_txt

def next_turn(store:Store) -> None:
    """
    Function that starts the next turn. Currently adds a random number of customers between 0 and
    10 after emptying all customers from previous turn. TODO: Handle the customer purchases before
    removing them from the customers list.
    
    Args:
    -----
        - store (Store): Instance of the class Store, needed for accessing the store's customers.
    """
    store.customers = []
    for _ in range(random.randint(0, 10)):
        store.new_customer()


